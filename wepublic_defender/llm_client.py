"""
Provider-agnostic LLM client utilities for WePublicDefender.

This module reads `wepublic_defender/config/llm_providers.json` and exposes
helpers to:
- Resolve provider + model configuration by logical model key (e.g., "gpt-5")
- Create appropriate client for each provider (OpenAI Responses API, xAI native SDK)
- Execute chat completions with sensible timeouts and tracking
- Route to provider-specific implementations based on api_type

Architecture:
- chat_complete(): Router function that dispatches to provider-specific implementations
- _call_openai_responses(): OpenAI Responses API (for GPT-5 models)
- _call_xai_native(): xAI native SDK (for Grok models)
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple, Type

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - allow import to fail gracefully at runtime
    OpenAI = None  # type: ignore

try:
    from xai_sdk import Client as XAIClient
    from xai_sdk.chat import system, user, assistant
except Exception:  # pragma: no cover - allow import to fail gracefully at runtime
    XAIClient = None  # type: ignore
    system = None  # type: ignore
    user = None  # type: ignore
    assistant = None  # type: ignore

from .config import load_llm_providers
from .logging_utils import get_logger


class LLMConfigError(Exception):
    pass


def _get_configs(model_key: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Return (provider_cfg, model_cfg, root_cfg) for a logical model key.

    Args:
        model_key: Logical model identifier like 'gpt-5' or 'grok-4'

    Returns:
        Tuple of (provider_config, model_config, root_config)

    Raises:
        LLMConfigError: If model_key or provider not found in config

    Examples:
        >>> provider_cfg, model_cfg, root_cfg = _get_configs("gpt-5")
        >>> model_cfg["provider"]
        'openai'
        >>> "input_token_ppm" in model_cfg
        True
        >>> "base_url" in provider_cfg
        True

        >>> try:
        ...     _get_configs("nonexistent-model")
        ... except LLMConfigError as e:
        ...     "Unknown model key" in str(e)
        True
    """
    root = load_llm_providers()

    models = root.get("modelConfigurations", {})
    if model_key not in models:
        raise LLMConfigError(f"Unknown model key: {model_key}")
    model_cfg = models[model_key]

    providers = root.get("llm_providers", {})
    provider_name = model_cfg.get("provider")
    if provider_name not in providers:
        raise LLMConfigError(
            f"Provider '{provider_name}' not defined for model '{model_key}'"
        )
    provider_cfg = providers[provider_name]
    return provider_cfg, model_cfg, root


def _compute_timeout(
    root_cfg: Dict[str, Any],
    service_tier: str = "auto",
    model_cfg: Optional[Dict[str, Any]] = None,
    web_search: bool = False,
) -> float:
    """
    Compute a request timeout using the repo's timeoutConfig policy.

    Priority order:
    1. Model-specific timeout (timeouts.with_web_search if web_search else timeouts.default)
    2. Global default timeout
    3. Apply service tier multiplier
    4. Apply web_search multiplier if configured and web_search is True

    Args:
        root_cfg: Root configuration dict
        service_tier: Service tier (auto, flex, standard, priority)
        model_cfg: Optional model configuration dict with timeouts field
        web_search: Whether web search is enabled for this request

    Returns:
        Computed timeout in seconds, capped at maxTimeout
    """
    tcfg = root_cfg.get("timeoutConfig", {})

    # 1. Determine base timeout (model-specific or global default)
    if model_cfg and "timeouts" in model_cfg:
        model_timeouts = model_cfg["timeouts"]
        if web_search and "with_web_search" in model_timeouts:
            base = float(model_timeouts["with_web_search"])
        elif "default" in model_timeouts:
            base = float(model_timeouts["default"])
        else:
            base = float(tcfg.get("globalDefault", 120))
    else:
        base = float(tcfg.get("globalDefault", 120))

    # 2. Apply service tier multiplier
    mults = tcfg.get("multipliers", {})
    tier_mults = (mults.get("service_tier", {}) or {})
    tier_factor = float(tier_mults.get(service_tier, 1.0))
    timeout = base * tier_factor

    # 3. Apply web_search multiplier if configured (in addition to model-specific timeout)
    if web_search and "web_search" in mults:
        web_search_factor = float(mults.get("web_search", 1.0))
        timeout = timeout * web_search_factor

    # 4. Cap at maxTimeout
    max_timeout = float(tcfg.get("maxTimeout", 43200))
    return min(timeout, max_timeout)


def _create_client(provider_cfg: Dict[str, Any]) -> Optional[OpenAI]:
    """
    Create an OpenAI-compatible client for the given provider config.
    Returns None if api key not present or OpenAI SDK missing.
    """
    if OpenAI is None:
        return None

    api_key_env = provider_cfg.get("api_key_env_var")
    if not api_key_env:
        return None
    api_key = os.getenv(api_key_env)
    if not api_key:
        return None

    base_url = provider_cfg.get("base_url")
    params: Dict[str, Any] = {"api_key": api_key}
    if base_url:
        params["base_url"] = base_url

    try:
        return OpenAI(**params)
    except Exception:
        return None


def ensure_client_for_model(model_key: str) -> Tuple[Optional[OpenAI], Dict[str, Any], Dict[str, Any]]:
    """
    Resolve provider + model config and create a client.

    Returns (client_or_none, model_cfg, root_cfg).
    """
    provider_cfg, model_cfg, root_cfg = _get_configs(model_key)
    client = _create_client(provider_cfg)
    return client, model_cfg, root_cfg


def _call_openai_responses(
    client: OpenAI,
    model_cfg: Dict[str, Any],
    root_cfg: Dict[str, Any],
    messages: List[Dict[str, Any]],
    *,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    service_tier: str = "auto",
    effort: Optional[str] = None,
    web_search: bool = False,
    pydantic_model: Optional[Type] = None,
    model_key: str,
) -> Dict[str, Any]:
    """
    Call OpenAI Responses API (for GPT-5 models).

    Uses client.responses.create() with:
    - reasoning={"effort": "low"} for reasoning models
    - tools=[{"type": "web_search"}] for web search
    - response_format=pydantic_model for structured outputs
    """
    logger = get_logger()
    wire_model = model_cfg.get("model_name", model_key)
    temp = temperature if temperature is not None else model_cfg.get("temperature")
    max_tokens = max_output_tokens or model_cfg.get("max_output_tokens")

    # Timeout policy
    timeout = _compute_timeout(
        root_cfg,
        service_tier=service_tier,
        model_cfg=model_cfg,
        web_search=web_search
    )
    started = time.time()
    req_client = client.with_options(timeout=timeout)

    # Build request kwargs
    request_kwargs: Dict[str, Any] = {
        "model": wire_model,
        "input": messages,  # Responses API uses 'input' instead of 'messages'
    }

    # Temperature support (GPT-5 family typically doesn't support temperature)
    supports_temp_cfg = model_cfg.get("supports_temperature", False)
    if supports_temp_cfg and temp is not None:
        request_kwargs["temperature"] = temp

    # Token limit (Responses API uses max_output_tokens)
    if max_tokens is not None:
        request_kwargs["max_output_tokens"] = max_tokens
    tokens_param = "max_output_tokens"  # For logging

    # Reasoning effort (native Responses API format)
    supports_reasoning = bool(model_cfg.get("supported_features", {}).get("reasoning", False))
    effort_applied = False
    if supports_reasoning and effort in {"minimal", "low", "medium", "high"}:
        request_kwargs["reasoning"] = {"effort": effort}
        effort_applied = True

    # Web search
    if web_search:
        request_kwargs["tools"] = [{"type": "web_search"}]

    # Log request
    try:
        logger.debug(
            "OpenAI Responses API request | model_key=%s | wire_model=%s | tokens_param=%s | max_tokens=%s | temp=%s | tier=%s | effort=%s | web_search=%s | pydantic=%s | msgs=%s",
            model_key,
            wire_model,
            tokens_param,
            max_tokens,
            temp,
            service_tier,
            effort if effort_applied else None,
            web_search,
            pydantic_model.__name__ if pydantic_model else None,
            [(m.get('role'), len(str(m.get('content','')))) for m in messages],
        )
    except Exception:
        pass

    # Make the API call - use parse() for structured outputs, create() for plain text
    if pydantic_model is not None:
        # Use responses.parse() with text_format for structured outputs
        request_kwargs["text_format"] = pydantic_model
        resp = req_client.responses.parse(**request_kwargs)
    else:
        # Use responses.create() for plain text
        resp = req_client.responses.create(**request_kwargs)

    duration = time.time() - started

    # Extract text from response
    if pydantic_model is not None:
        # For structured outputs, get the parsed Pydantic object from output_parsed
        # Don't serialize to JSON here - return the object and let core.py handle it
        parsed_obj = getattr(resp, "output_parsed", None)
        if parsed_obj:
            # Serialize to JSON for the text field (for logging/compatibility)
            text = parsed_obj.model_dump_json(indent=2)
        else:
            text = ""
    else:
        # For plain text, use output_text
        text = getattr(resp, "output_text", "") or ""

    # Extract usage information (Responses API uses input_tokens/output_tokens)
    usage = getattr(resp, "usage", None)
    in_tok = getattr(usage, "input_tokens", 0) if usage else 0
    out_tok = getattr(usage, "output_tokens", 0) if usage else 0

    # Check for cached tokens in input_tokens_details
    input_details = getattr(usage, "input_tokens_details", None) if usage else None
    if input_details and isinstance(input_details, dict):
        cached_tok = int(input_details.get("cached_tokens", 0))
    else:
        cached_tok = 0

    # Log response
    try:
        logger.info(
            "OpenAI Responses API response | model_key=%s | wire_model=%s | in=%s | out=%s | cached=%s | dur=%.2fs | effort=%s | tier=%s",
            model_key,
            wire_model,
            int(in_tok or 0),
            int(out_tok or 0),
            int(cached_tok or 0),
            duration,
            effort if effort_applied else None,
            service_tier,
        )
    except Exception:
        pass

    return {
        "text": text,
        "usage": {
            "input": int(in_tok or 0),
            "output": int(out_tok or 0),
            "cached": int(cached_tok or 0),
            "duration": duration,
            "service_tier": service_tier,
            "model": model_key,
            "effort": effort if effort_applied else None,
            "effort_requested": effort,
        },
        "meta": {
            "wire_model": wire_model,
            "tokens_param": tokens_param,
            "max_tokens": max_tokens,
            "temperature": temp,
            "supports_temperature": supports_temp_cfg,
            "reasoning_supported": supports_reasoning,
            "api_type": "openai_responses",
        },
        "raw": resp,
    }


def _call_xai_native(
    provider_cfg: Dict[str, Any],
    model_cfg: Dict[str, Any],
    root_cfg: Dict[str, Any],
    messages: List[Dict[str, Any]],
    *,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    service_tier: str = "auto",
    effort: Optional[str] = None,
    web_search: bool = False,
    pydantic_model: Optional[Type] = None,
    model_key: str,
) -> Dict[str, Any]:
    """
    Call xAI native SDK (for Grok models).

    Uses xai_sdk.Client().chat.create() with builder pattern:
    - chat.append() for messages
    - chat.sample(search=True) for web search
    - Native Pydantic support via response_format
    """
    logger = get_logger()

    if XAIClient is None:
        raise RuntimeError(
            "xai_sdk not available. Install with: pip install xai-sdk"
        )

    # Get API key
    api_key_env = provider_cfg.get("api_key_env_var")
    api_key = os.getenv(api_key_env) if api_key_env else None
    if not api_key:
        raise RuntimeError(f"xAI API key not found in environment variable: {api_key_env}")

    wire_model = model_cfg.get("model_name", model_key)
    temp = temperature if temperature is not None else model_cfg.get("temperature")
    max_tokens = max_output_tokens or model_cfg.get("max_output_tokens")

    # Timeout policy
    timeout = _compute_timeout(
        root_cfg,
        service_tier=service_tier,
        model_cfg=model_cfg,
        web_search=web_search
    )
    started = time.time()

    # Create xAI client
    xai_client = XAIClient(api_key=api_key)

    # Build create kwargs - all parameters go here, not in sample()
    create_kwargs: Dict[str, Any] = {}

    # Temperature
    supports_temp_cfg = model_cfg.get("supports_temperature", True)
    if supports_temp_cfg and temp is not None:
        create_kwargs["temperature"] = temp

    # Token limit (xAI uses "max_tokens" not "max_output_tokens")
    if max_tokens is not None:
        create_kwargs["max_tokens"] = max_tokens

    # Reasoning effort (xAI uses "reasoning_effort" with string value, not dict)
    # NOTE: grok-4 models do NOT support reasoning_effort parameter
    # Only grok-3-mini supports it according to xAI docs
    supports_reasoning = bool(model_cfg.get("supported_features", {}).get("reasoning", False))
    effort_applied = False
    if supports_reasoning and effort in {"low", "high"}:
        # Only send reasoning_effort for grok-3 models, not grok-4
        if "grok-3" in wire_model.lower() and "mini" in wire_model.lower():
            # xAI only supports "low" and "high", map medium/minimal to these
            if effort in {"medium", "high"}:
                create_kwargs["reasoning_effort"] = "high"
            else:  # low or minimal
                create_kwargs["reasoning_effort"] = "low"
            effort_applied = True

    # Web search (use search_parameters for now, may need to import SearchParameters)
    if web_search:
        # For now, use None which should enable default web search
        # TODO: Use SearchParameters for more control
        try:
            from xai_sdk.search import SearchParameters
            create_kwargs["search_parameters"] = SearchParameters()
        except:
            pass  # Skip web search if SearchParameters not available

    # Build chat with all parameters (DO NOT pass response_format here)
    chat = xai_client.chat.create(model=wire_model, **create_kwargs)

    # Add messages using xAI SDK helper functions
    for msg in messages:
        role_str = msg.get("role", "user")
        content = msg.get("content", "")
        if role_str == "system":
            chat.append(system(content))
        elif role_str == "user":
            chat.append(user(content))
        elif role_str == "assistant":
            chat.append(assistant(content))

    # Log request
    try:
        logger.debug(
            "xAI native SDK request | model_key=%s | wire_model=%s | max_tokens=%s | temp=%s | tier=%s | effort=%s | web_search=%s | pydantic=%s | msgs=%s",
            model_key,
            wire_model,
            max_tokens,
            temp,
            service_tier,
            effort if effort_applied else None,
            web_search,
            pydantic_model.__name__ if pydantic_model else None,
            [(m.get('role'), len(str(m.get('content','')))) for m in messages],
        )
    except Exception:
        pass

    # Make the API call
    # xAI SDK uses chat.parse(Model) for structured outputs, not response_format
    if pydantic_model is not None:
        # Use parse() for structured outputs
        resp, parsed_obj = chat.parse(pydantic_model)
        duration = time.time() - started
        # Serialize the Pydantic object to JSON for the text field
        text = parsed_obj.model_dump_json(indent=2) if parsed_obj else ""
    else:
        # Use sample() for plain text
        resp = chat.sample()
        duration = time.time() - started
        # Extract text from response
        text = getattr(resp, "content", "") or getattr(resp, "text", "")

    # Extract usage information (xAI uses different field names than OpenAI)
    usage = getattr(resp, "usage", None)
    # xAI uses prompt_tokens/completion_tokens instead of input_tokens/output_tokens
    in_tok = getattr(usage, "prompt_tokens", 0) if usage else 0
    out_tok = getattr(usage, "completion_tokens", 0) if usage else 0
    # Check for cached tokens in prompt_tokens_details
    prompt_details = getattr(usage, "prompt_tokens_details", None) if usage else None
    if prompt_details:
        cached_tok = getattr(prompt_details, "cached_tokens", 0)
    else:
        cached_tok = 0

    # Log response
    try:
        logger.info(
            "xAI native SDK response | model_key=%s | wire_model=%s | in=%s | out=%s | cached=%s | dur=%.2fs | effort=%s | tier=%s",
            model_key,
            wire_model,
            int(in_tok or 0),
            int(out_tok or 0),
            int(cached_tok or 0),
            duration,
            effort if effort_applied else None,
            service_tier,
        )
    except Exception:
        pass

    return {
        "text": text,
        "usage": {
            "input": int(in_tok or 0),
            "output": int(out_tok or 0),
            "cached": int(cached_tok or 0),
            "duration": duration,
            "service_tier": service_tier,
            "model": model_key,
            "effort": effort if effort_applied else None,
            "effort_requested": effort,
        },
        "meta": {
            "wire_model": wire_model,
            "max_tokens": max_tokens,
            "temperature": temp,
            "supports_temperature": supports_temp_cfg,
            "reasoning_supported": supports_reasoning,
            "api_type": "xai_native",
        },
        "raw": resp,
    }


def chat_complete(
    model_key: str,
    messages: List[Dict[str, Any]],
    *,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    service_tier: str = "auto",
    effort: Optional[str] = None,
    web_search: bool = False,
    pydantic_model: Optional[Type] = None,
) -> Dict[str, Any]:
    """
    Router function for chat completions - dispatches to provider-specific implementations.

    This function reads the api_type from model config and routes to the appropriate
    provider-specific implementation:
    - "openai_responses" -> _call_openai_responses() for GPT models
    - "xai_native" -> _call_xai_native() for Grok models

    Args:
        model_key: Logical model identifier (e.g., "gpt-5", "grok-4")
        messages: List of message dicts with "role" and "content"
        temperature: Sampling temperature (if supported by model)
        max_output_tokens: Maximum tokens to generate
        service_tier: Service tier for OpenAI ("auto", "flex", "standard", "priority")
        effort: Reasoning effort level ("minimal", "low", "medium", "high")
        web_search: Enable web search (if supported by model)
        pydantic_model: Pydantic model class for structured outputs

    Returns:
        Dict with keys: "text", "usage", "meta", "raw"

    Raises:
        LLMConfigError: If model_key or api_type is invalid
        RuntimeError: If required SDK or API key is missing
    """
    logger = get_logger()

    # Get configuration
    provider_cfg, model_cfg, root_cfg = _get_configs(model_key)

    # Get api_type to determine which implementation to use
    api_type = model_cfg.get("api_type")
    if not api_type:
        raise LLMConfigError(
            f"Model '{model_key}' has no api_type specified in config. "
            "Add 'api_type' field to model configuration."
        )

    logger.debug(
        "Router dispatch | model_key=%s | api_type=%s | effort=%s | web_search=%s",
        model_key, api_type, effort, web_search
    )

    # Route to appropriate implementation
    if api_type == "openai_responses":
        # OpenAI Responses API (for GPT models)
        client = _create_client(provider_cfg)
        if client is None:
            raise RuntimeError(
                f"OpenAI client not available or API key not set for provider '{provider_cfg.get('name')}'"
            )
        return _call_openai_responses(
            client=client,
            model_cfg=model_cfg,
            root_cfg=root_cfg,
            messages=messages,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            service_tier=service_tier,
            effort=effort,
            web_search=web_search,
            pydantic_model=pydantic_model,
            model_key=model_key,
        )

    elif api_type == "xai_native":
        # xAI native SDK (for Grok models)
        return _call_xai_native(
            provider_cfg=provider_cfg,
            model_cfg=model_cfg,
            root_cfg=root_cfg,
            messages=messages,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            service_tier=service_tier,
            effort=effort,
            web_search=web_search,
            pydantic_model=pydantic_model,
            model_key=model_key,
        )

    else:
        raise LLMConfigError(
            f"Unknown api_type '{api_type}' for model '{model_key}'. "
            f"Supported types: 'openai_responses', 'xai_native'"
        )

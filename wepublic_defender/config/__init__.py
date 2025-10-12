"""
Configuration utilities for wepublic_defender.

Functions to load/save provider and review settings, prefer per‑case
overrides when available, and update agent/jurisdiction preferences
programmatically (for Claude or CLI flows).
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

from ..logging_utils import get_logger


CASE_SETTINGS_DIRNAME = ".wepublic_defender"


def _case_settings_dir() -> Optional[Path]:
    """Return per‑case settings directory if available.

    Resolution order:
    1) WPD_SETTINGS_DIR env var, if exists
    2) Current working directory /.wepublic_defender if exists
    """
    # 1) Explicit env var
    env_dir = os.getenv("WPD_SETTINGS_DIR")
    if env_dir and Path(env_dir).exists():
        return Path(env_dir)
    # 2) CWD/.wepublic_defender
    cwd_dir = Path.cwd() / CASE_SETTINGS_DIRNAME
    if cwd_dir.exists():
        return cwd_dir
    return None


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries, with override taking precedence.

    Preserves nested maps and only overwrites leaf values present in override.
    """
    out: Dict[str, Any] = {}
    for k in base.keys() | override.keys():
        if k in base and k in override and isinstance(base[k], dict) and isinstance(override[k], dict):
            out[k] = _deep_merge(base[k], override[k])
        elif k in override:
            out[k] = override[k]
        else:
            out[k] = base[k]
    return out


REDUNDANT_TOPLEVEL = {
    "max_iterations",
    "default_effort",
    "providerPolicy",
    "consensus_threshold",
    "parallel_execution",
}


def _clean_review_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Remove unused/redundant keys and normalize agent configs.

    - Drop workflowConfig keys not used by tools (max_iterations, default_effort,
      providerPolicy, consensus_threshold, parallel_execution)
    - For each agent: remove 'model', 'notes', 'search_sources'; ensure 'models' list
    """
    out = dict(settings)
    rac: Dict[str, Any] = out.get("reviewAgentConfig", {}) or {}

    # Normalize agents
    for ak, acfg in list(rac.items()):
        if not isinstance(acfg, dict):
            continue
        # Promote single model to list if needed
        if "models" not in acfg:
            m = acfg.get("model")
            if isinstance(m, str) and m:
                acfg["models"] = [m]
        # Remove redundant keys
        for k in ("model", "notes", "search_sources"):
            if k in acfg:
                acfg.pop(k, None)
        rac[ak] = acfg
    out["reviewAgentConfig"] = rac

    # Clean workflowConfig
    wf: Dict[str, Any] = out.get("workflowConfig", {}) or {}
    for k in list(wf.keys()):
        if k in REDUNDANT_TOPLEVEL:
            wf.pop(k, None)
    out["workflowConfig"] = wf
    return out


def load_llm_providers() -> Dict[str, Any]:
    """
    Load LLM provider configurations including pricing and capabilities.

    Returns:
        Dictionary containing llm_providers, timeoutConfig, and modelConfigurations

    Example:
        >>> config = load_llm_providers()
        >>> gpt5_config = config['modelConfigurations']['gpt-5']
        >>> print(gpt5_config['input_token_ppm'])
        1.25
    """
    # Prefer per‑case override if present
    case_dir = _case_settings_dir()
    case_override = case_dir / "llm_providers.json" if case_dir else None
    pkg_path = Path(__file__).parent / "llm_providers.json"
    with open(pkg_path, 'r', encoding='utf-8') as f:
        pkg = json.load(f)
    if case_override and case_override.exists():
        with open(case_override, 'r', encoding='utf-8') as f:
            case_cfg = json.load(f)
        # Merge package defaults → case overrides (case wins)
        merged = _deep_merge(pkg, case_cfg)
        return merged
    return pkg


def load_review_settings() -> Dict[str, Any]:
    """
    Load legal review settings including agent configurations.

    Returns:
        Dictionary containing loggingLevel, reviewAgentConfig, and workflowConfig

    Example:
        >>> settings = load_review_settings()
        >>> strategy_agent = settings['reviewAgentConfig']['strategy_agent']
        >>> print(strategy_agent['model'])
        'gpt-5'
    """
    logger = get_logger()
    # Prefer per‑case settings if present
    case_dir = _case_settings_dir()
    # Load packaged defaults
    pkg_path = Path(__file__).parent / "legal_review_settings.json"
    with open(pkg_path, 'r', encoding='utf-8') as f:
        pkg = json.load(f)

    # Merge with per-case overrides if present; write back to keep keys up to date
    case_path = (case_dir / "legal_review_settings.json") if case_dir else None
    if case_path and case_path.exists():
        with open(case_path, 'r', encoding='utf-8') as f:
            case_cfg = json.load(f)
        merged = _deep_merge(pkg, case_cfg)
        cleaned = _clean_review_settings(merged)
        try:
            logger.info("Loaded review settings | source=per-case | path=%s", case_path)
            # Save cleaned + merged config back to per-case to keep keys consistent
            save_review_settings(cleaned)
        except Exception:
            pass
        return cleaned
    logger.info("Loaded review settings | source=package | path=%s", pkg_path)
    return _clean_review_settings(pkg)


def get_review_settings_path() -> Path:
    """Return the active path to legal review settings JSON (case or package)."""
    case_dir = _case_settings_dir()
    if case_dir:
        return case_dir / "legal_review_settings.json"
    return Path(__file__).parent / "legal_review_settings.json"


def save_review_settings(settings: Dict[str, Any]) -> None:
    """Persist settings to per‑case directory when possible."""
    case_dir = _case_settings_dir()
    if not case_dir:
        # Create case settings dir at CWD by default
        case_dir = Path.cwd() / CASE_SETTINGS_DIRNAME
        case_dir.mkdir(parents=True, exist_ok=True)
    target = case_dir / "legal_review_settings.json"
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def update_agent_preference(
    agent_name: str,
    *,
    models: Optional[List[str]] = None,
    effort: Optional[str] = None,
    web_search: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Update per-agent preferences (models, effort, web_search) and save.

    Returns the updated settings dict.
    """
    settings = load_review_settings()
    agents = settings.get("reviewAgentConfig", {})
    if agent_name not in agents:
        raise KeyError(f"Agent not found: {agent_name}")

    agent_cfg = agents[agent_name]

    # Migrate single model -> list if needed
    if models is not None:
        agent_cfg["models"] = list(models)

    if effort is not None:
        agent_cfg["effort"] = effort

    if web_search is not None:
        agent_cfg["web_search"] = bool(web_search)

    agents[agent_name] = agent_cfg
    settings["reviewAgentConfig"] = agents
    save_review_settings(settings)
    return settings


def update_jurisdiction_config(
    *,
    jurisdiction: Optional[str] = None,
    court: Optional[str] = None,
    circuit: Optional[str] = None,
    preferred_authority_order: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Update workflowConfig.jurisdictionConfig and save."""
    settings = load_review_settings()
    wf = settings.setdefault("workflowConfig", {})
    jcfg = wf.setdefault("jurisdictionConfig", {})

    if jurisdiction is not None:
        jcfg["jurisdiction"] = jurisdiction
    if court is not None:
        jcfg["court"] = court
    if circuit is not None:
        jcfg["circuit"] = circuit
    if preferred_authority_order is not None:
        jcfg["preferred_authority_order"] = list(preferred_authority_order)

    wf["jurisdictionConfig"] = jcfg
    settings["workflowConfig"] = wf
    save_review_settings(settings)
    return settings


def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific model.

    Args:
        model_name: Name of the model (e.g., 'gpt-5', 'grok-4')

    Returns:
        Model configuration dictionary

    Raises:
        KeyError: If model not found

    Example:
        >>> gpt5 = get_model_config('gpt-5')
        >>> print(gpt5['input_token_ppm'])
        1.25
    """
    providers = load_llm_providers()
    return providers['modelConfigurations'][model_name]


def get_provider_config(provider_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific LLM provider.

    Args:
        provider_name: Name of the provider (e.g., 'openai', 'xai')

    Returns:
        Provider configuration dictionary

    Raises:
        KeyError: If provider not found

    Example:
        >>> openai = get_provider_config('openai')
        >>> print(openai['base_url'])
        'https://api.openai.com/v1'
    """
    providers = load_llm_providers()
    return providers['llm_providers'][provider_name]


def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific review agent.

    Args:
        agent_name: Name of the agent (e.g., 'strategy_agent', 'citation_verifier_agent')

    Returns:
        Agent configuration dictionary

    Raises:
        KeyError: If agent not found

    Example:
        >>> strategy = get_agent_config('strategy_agent')
        >>> print(strategy['model'])
        'gpt-5'
        >>> print(strategy['web_search'])
        True
    """
    settings = load_review_settings()
    return settings['reviewAgentConfig'][agent_name]


__all__ = [
    'load_llm_providers',
    'load_review_settings',
    'save_review_settings',
    'get_review_settings_path',
    'update_agent_preference',
    'update_jurisdiction_config',
    'get_model_config',
    'get_provider_config',
    'get_agent_config',
]

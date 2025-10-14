"""
WePublicDefender - Adversarial Legal Review System

Main class for performing AI-powered legal document review with multiple
providers (OpenAI GPT-5, xAI Grok 4) for redundancy and adversarial testing.
"""

import os
import json
import re
import asyncio
from typing import Dict, List, Optional, Tuple, Literal, Any, Type
from pathlib import Path

try:
    from openai import OpenAI, AsyncOpenAI
except ImportError:
    print("Warning: OpenAI library not installed. Run: pip install openai")
    OpenAI = None
    AsyncOpenAI = None

from .models.settings_manager import SettingsManager
from .models.token_tracker import TokenTracker, TokenUsage
from .config import load_llm_providers, load_review_settings
from .llm_client import chat_complete
from .document_handlers import convert_markdown_to_word, DocumentFormatConfig
from pydantic import BaseModel, ValidationError
from .models.legal_responses import (
    CitationVerificationResult,
    OpposingCounselReview,
    DocumentReviewResult,
    LegalResearchResult,
    StrategyRecommendation,
)
from .research_log import log_citation_verifications
from .logging_utils import get_logger


class WePublicDefender:
    """
    Adversarial legal review system using multiple AI providers.

    Features:
    - Multi-AI review (OpenAI GPT-5 + xAI Grok 4)
    - Adversarial testing (opposing counsel mode)
    - Iterative refinement loops
    - Comprehensive cost tracking
    - Web search integration for legal research
    """

    def __init__(self):
        """
        Initialize WePublicDefender system.

        Loads configurations from package config files:
        - llm_providers.json: Provider configs, pricing, capabilities
        - legal_review_settings.json: Agent and workflow configs
        """
        # Load .env if present (supports system env vars by default)
        try:
            from dotenv import load_dotenv, find_dotenv
            load_dotenv(find_dotenv(usecwd=True), override=False)
        except Exception:
            pass
        # Load configurations from package
        self.llm_config = load_llm_providers()
        self.review_settings = load_review_settings()

        # Initialize clients
        self.openai_client = self._create_openai_client()
        self.grok_client = self._create_grok_client()

        # Initialize token tracker with model configurations
        models_config = self.llm_config["modelConfigurations"]
        self.token_tracker = TokenTracker(models_config)

        # Store markdown format instructions
        self.markdown_format_instructions = """
RETURN FORMAT: Markdown with proper structure
# Document Title
## Major Sections (ALL CAPS for court documents)
### Subsections
#### Sub-subsections

Use **bold** for emphasis, *italic* for case names (e.g., *Smith v. Jones*)
Use > for blockquotes
Use - for bullet lists

This format will be automatically converted to Word when ready for filing.
"""

        self.logger = get_logger()
        self.logger.info("WePublicDefender initialized")
        try:
            self.logger.info(
                "Providers: %s | Models: %s",
                list(self.llm_config['llm_providers'].keys()),
                list(models_config.keys()),
            )
        except Exception:
            pass

    def _build_jurisdiction_context(
        self,
        *,
        jurisdiction: Optional[str] = None,
        court: Optional[str] = None,
        circuit: Optional[str] = None,
        preferred_authority_order: Optional[List[str]] = None,
    ) -> Optional[str]:
        """Create a jurisdiction context string for prompts based on settings + overrides."""
        wf = self.review_settings.get("workflowConfig", {})
        jcfg = dict(wf.get("jurisdictionConfig", {}) or {})

        # Apply overrides if provided
        if jurisdiction is not None:
            jcfg["jurisdiction"] = jurisdiction
        if court is not None:
            jcfg["court"] = court
        if circuit is not None:
            jcfg["circuit"] = circuit
        if preferred_authority_order is not None:
            jcfg["preferred_authority_order"] = preferred_authority_order

        # If we have nothing, return None
        if not any(jcfg.get(k) for k in ("jurisdiction", "court", "circuit", "preferred_authority_order")):
            return None

        lines = ["JURISDICTION CONTEXT:"]
        if jcfg.get("jurisdiction"):
            lines.append(f"- Jurisdiction: {jcfg['jurisdiction']}")
        if jcfg.get("court"):
            lines.append(f"- Court: {jcfg['court']}")
        if jcfg.get("circuit"):
            lines.append(f"- Circuit: {jcfg['circuit']}")
        pao = jcfg.get("preferred_authority_order") or []
        if pao:
            lines.append("- Preferred Authority Order: " + ", ".join(pao))
        lines.append(
            "Use this context to prioritize controlling authorities and applicable procedural rules."
        )
        return "\n".join(lines)

    def _resolve_agent_key(self, agent_type: str) -> str:
        """Map user-friendly agent_type to the settings key name."""
        candidates = [f"{agent_type}_agent"]
        # Handle known alias for citation agent
        if agent_type == "citation_verify":
            candidates.insert(0, "citation_verifier_agent")
        rac = self.review_settings.get("reviewAgentConfig", {})
        for key in candidates:
            if key in rac:
                return key
        raise ValueError(
            f"Unknown agent type: {agent_type}. Available: {list(rac.keys())}"
        )

    def _agent_model(self, agent_type: str) -> Tuple[Optional[Type[BaseModel]], bool]:
        """Return (pydantic_model, expects_list) for agent_type."""
        mapping: Dict[str, Tuple[Optional[Type[BaseModel]], bool]] = {
            "strategy": (StrategyRecommendation, False),
            "drafter": (None, False),  # free-form text for drafter
            "self_review": (DocumentReviewResult, False),
            "citation_verify": (CitationVerificationResult, True),  # may return list
            "opposing_counsel": (OpposingCounselReview, False),
            "final_review": (DocumentReviewResult, False),
            "research": (LegalResearchResult, False),
        }
        return mapping.get(agent_type, (None, False))

    def _schema_block(self, model_cls: Type[BaseModel]) -> str:
        schema = model_cls.model_json_schema()
        return (
            "You MUST return ONLY JSON matching this JSON schema (no extra text):\n"
            + json.dumps(schema, indent=2)
        )

    def _parse_json_payload(self, text: str) -> Any:
        """Attempt to parse JSON from text; try to extract JSON substring if needed."""
        try:
            return json.loads(text)
        except Exception:
            # Try to extract JSON object or array heuristically
            obj_match = re.search(r"\{[\s\S]*\}", text)
            arr_match = re.search(r"\[[\s\S]*\]", text)
            snippet = None
            if arr_match:
                snippet = arr_match.group(0)
            elif obj_match:
                snippet = obj_match.group(0)
            if snippet:
                return json.loads(snippet)
            raise

    def _generate_claude_prompt(self, agent_type: str, parsed: Any) -> Optional[str]:
        """
        Generate intelligent claude_prompt based on agent type and results.

        This prompt tells Claude Code what to do next based on the agent's findings.
        Agents have domain knowledge and can guide the orchestration workflow.

        Args:
            agent_type: Type of agent that ran
            parsed: Parsed structured result (may be single object or list)

        Returns:
            String prompt for Claude Code, or None if no guidance needed
        """
        if parsed is None:
            return None

        try:
            # Handle list results (like citation_verify)
            items = parsed if isinstance(parsed, list) else [parsed]

            if agent_type == "self_review" or agent_type == "final_review":
                # DocumentReviewResult
                data = items[0] if items else None
                if not data:
                    return None

                crit = getattr(data, 'critical_issues', [])
                major = getattr(data, 'major_issues', [])
                minor = getattr(data, 'minor_issues', [])
                ready = getattr(data, 'ready_to_file', False)

                if ready:
                    return f"Review passed! Document is ready to file (0 critical, {len(major)} major, {len(minor)} minor issues). Summarize the {len(major)} major issues for the user and ask if they want to address them before filing or proceed as-is."
                elif crit:
                    return f"Found {len(crit)} CRITICAL issues that must be fixed before filing: {'; '.join(crit[:2])}{'...' if len(crit) > 2 else ''}. Also {len(major)} major and {len(minor)} minor issues. Present the critical issues as a bulleted list and ask if I should research solutions or if the user wants to review the full output first."
                elif major:
                    return f"Found {len(major)} major issues (no critical): {'; '.join(major[:2])}{'...' if len(major) > 2 else ''}. Also {len(minor)} minor issues. Document needs revision. Present the major issues as a bulleted list and ask user if they want me to draft fixes or if they prefer to revise manually."
                else:
                    return f"Only {len(minor)} minor issues found. Document is in good shape. List the minor improvements and ask if the user wants to address them or proceed with filing."

            elif agent_type == "citation_verify":
                # CitationVerificationResult (list)
                bad_law = [item for item in items if not getattr(item, 'still_good_law', True)]
                unsupported = [item for item in items if getattr(item, 'supports_position', None) == False]
                issues = [item for item in items if getattr(item, 'issues_found', None)]

                total = len(items)

                if bad_law:
                    # Build summary outside f-string to avoid nested f-string syntax error
                    bad_law_summary = '; '.join([
                        "{} ({})".format(
                            getattr(item, 'case_name', 'Unknown'),
                            ', '.join(getattr(item, 'issues_found', []))
                        )
                        for item in bad_law[:2]
                    ])
                    return f"WARNING: {len(bad_law)} of {total} citations are NO LONGER GOOD LAW: {bad_law_summary}. List these citations with their issues and strongly recommend immediate replacement. Also note {len(unsupported)} citations don't support our position."
                elif unsupported:
                    unsupported_names = '; '.join([getattr(item, 'case_name', 'Unknown') for item in unsupported[:2]])
                    return f"Found {len(unsupported)} citations that DON'T SUPPORT our position: {unsupported_names}. List these with explanations of why they don't support us and recommend replacement or removal. {total - len(unsupported)} citations verified as good."
                elif issues:
                    issues_names = '; '.join([getattr(item, 'case_name', 'Unknown') for item in issues[:2]])
                    return f"{len(issues)} citations have potential issues (but still good law): {issues_names}. Summarize the issues and ask if user wants to address them. {total - len(issues)} citations verified clean."
                else:
                    return f"All {total} citations verified as good law and supporting our position. Briefly confirm this success and ask if user wants to proceed with next review step (opposing_counsel)."

            elif agent_type == "opposing_counsel":
                # OpposingCounselReview
                data = items[0] if items else None
                if not data:
                    return None

                weaknesses = getattr(data, 'weaknesses_found', [])
                critical_weaknesses = [w for w in weaknesses if getattr(w, 'severity', None) == "critical"]
                major_weaknesses = [w for w in weaknesses if getattr(w, 'severity', None) == "major"]
                strength = getattr(data, 'overall_strength', 'unknown')

                if critical_weaknesses:
                    critical_issues = '; '.join([getattr(w, 'issue', 'Unknown') for w in critical_weaknesses[:2]])
                    return f"Opposing counsel found {len(critical_weaknesses)} CRITICAL weaknesses that could get the document dismissed: {critical_issues}. Overall assessment: {strength}. Present the critical weaknesses as a numbered list with their exploitation strategies and recommend immediate revision before filing."
                elif major_weaknesses:
                    major_issues = '; '.join([getattr(w, 'issue', 'Unknown') for w in major_weaknesses[:2]])
                    return f"Opposing counsel found {len(major_weaknesses)} major weaknesses (no critical): {major_issues}. Overall assessment: {strength}. Present the major weaknesses and ask if user wants me to draft strengthening revisions or if they want to address them manually."
                else:
                    return f"Opposing counsel found only minor weaknesses. Overall assessment: {strength}. Briefly summarize the document's strengths and minor areas for improvement, then ask if user wants to proceed with final_review."

            elif agent_type == "strategy":
                # StrategyRecommendation
                data = items[0] if items else None
                if not data:
                    return None

                next_actions = getattr(data, 'next_actions', [])
                high_priority = [a for a in next_actions if getattr(a, 'priority', '').upper() == "HIGH"]
                proc_concerns = getattr(data, 'procedural_concerns', [])

                if high_priority:
                    high_priority_actions = '; '.join([getattr(a, 'action', 'Unknown') for a in high_priority[:2]])
                    return f"Strategy analysis complete. {len(high_priority)} HIGH priority actions: {high_priority_actions}. Present the high-priority actions with their deadlines and rationales as a numbered list, then ask user which action they want to tackle first."
                elif next_actions:
                    return f"Strategy analysis complete. {len(next_actions)} recommended actions, {len(proc_concerns)} procedural concerns. Present the top 3-4 actions with priorities and deadlines, then ask user for their preferred approach."
                else:
                    return "Strategy analysis complete but no specific actions recommended. Summarize the strategic situation and ask user what they want to focus on."

            elif agent_type == "research":
                # LegalResearchResult
                data = items[0] if items else None
                if not data:
                    return None

                cases = getattr(data, 'cases', [])
                statutes = getattr(data, 'statutes', [])
                contrary = getattr(data, 'contrary_authority', [])

                if contrary:
                    contrary_summary = '; '.join(contrary[:2])
                    return f"Research found {len(cases)} relevant cases and {len(statutes)} statutes, BUT also found {len(contrary)} pieces of CONTRARY AUTHORITY: {contrary_summary}. Present the key findings including the contrary authority prominently, then discuss strategy for addressing unfavorable precedent."
                elif cases or statutes:
                    return f"Research found {len(cases)} relevant cases and {len(statutes)} applicable statutes. Summarize the 3-4 most important findings with their holdings/provisions, then ask user if they want me to draft language incorporating these authorities."
                else:
                    return "Research complete but found limited directly applicable authority. Summarize what was found and suggest either broader research or alternative legal theories."

            elif agent_type == "drafter":
                # Drafter returns free-form text, no structured data
                return "Draft complete. Present a brief summary of the document structure (main sections/arguments), then ask user if they want me to run self_review to check for issues or if they prefer to review it manually first."

            else:
                return None

        except Exception as e:
            self.logger.warning(f"Failed to generate claude_prompt for {agent_type}: {e}")
            return None

    def _create_openai_client(self):
        """Create OpenAI client from environment."""
        if OpenAI is None:
            raise ImportError("OpenAI library not installed")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set in environment")
            return None

        return OpenAI(api_key=api_key)

    def _create_grok_client(self):
        """Create Grok client (OpenAI-compatible) from environment."""
        if OpenAI is None:
            raise ImportError("OpenAI library not installed")

        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            print("Warning: XAI_API_KEY not set in environment")
            return None

        return OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    async def call_agent(
        self,
        agent_type: str,
        document: str,
        mode: Literal["guidance", "external-llm"] = "guidance",
        web_search: Optional[bool] = None,
        override_model: Optional[str] = None,
        override_effort: Optional[str] = None,
        override_service_tier: Optional[str] = None,
        override_jurisdiction: Optional[str] = None,
        override_court: Optional[str] = None,
        override_circuit: Optional[str] = None,
        override_preferred_authority: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """
        Call a specific review agent in one of two modes.

        Modes:
            - guidance: Returns prompt template for Claude Code (FREE - no API costs)
            - external-llm: Calls external LLM(s) configured in settings (COSTS MONEY)
                - If settings has one model: calls that model
                - If settings has multiple models: calls ALL in parallel for adversarial redundancy
                - Use --model flag to override and run specific model only
                - Use --run-both flag to force running both models

        Args:
            agent_type: One of [strategy, drafter, self_review, citation_verify,
                        opposing_counsel, final_review, organize, research]
            document: Document content to review
            mode: Agent mode - guidance or external-llm (default: guidance)
            web_search: Override web search setting
            override_model: Run single specific model (bypasses multi-model)
            **kwargs: Additional context for prompt

        Returns:
            For guidance mode:
            {
                "mode": "guidance",
                "agent": "drafter",
                "prompt": "...",  # Guidance text for Claude Code
                "context": {...},
            }

            For external-llm mode:
            {
                "mode": "external-llm",
                "model": "gpt-5",
                "text": "...",
                "usage": {...},
                "multi_model": true,  # If multiple models ran
                "alternate_results": [...]  # If multiple models ran
            }

        Example:
            >>> defender = WePublicDefender()
            >>> # Guidance mode (free)
            >>> result = await defender.call_agent("drafter", doc, mode="guidance")
            >>> # External LLM mode (costs money)
            >>> result = await defender.call_agent("drafter", doc, mode="external-llm")
        """
        # Special case: organize agent ONLY operates in guidance mode
        if agent_type == "organize":
            if mode != "guidance":
                self.logger.warning(
                    "organize agent only supports guidance mode; forcing mode=guidance"
                )
            return self._load_guidance(agent_type, document, **kwargs)

        # Route based on mode
        if mode == "guidance":
            return self._load_guidance(agent_type, document, **kwargs)

        # For external-llm mode, proceed with API calls
        # Get agent config from review settings
        agent_key = self._resolve_agent_key(agent_type)
        agent_config = self.review_settings.get("reviewAgentConfig", {}).get(agent_key)

        # Determine candidate models (support list or single key)
        candidates = []
        if isinstance(agent_config.get("models"), list):
            candidates = [m for m in agent_config["models"] if isinstance(m, str) and m]
        elif agent_config.get("model"):
            candidates = [agent_config["model"]]

        # Multi-model logic: run all models in parallel if 2+ configured and no override
        if len(candidates) > 1 and not override_model:
            try:
                self.logger.info(
                    "Running %d models in parallel | agent=%s | models=%s",
                    len(candidates),
                    agent_type,
                    candidates,
                )
            except Exception:
                pass

            # Run all models in parallel
            tasks = [
                self._run_single_model(
                    agent_type=agent_type,
                    model=model,
                    document=document,
                    web_search=web_search,
                    override_effort=override_effort,
                    override_service_tier=override_service_tier,
                    override_jurisdiction=override_jurisdiction,
                    override_court=override_court,
                    override_circuit=override_circuit,
                    override_preferred_authority=override_preferred_authority,
                )
                for model in candidates
            ]
            results = await asyncio.gather(*tasks)

            # Primary result is first model, others are alternates
            primary = results[0]
            primary["multi_model"] = True
            primary["alternate_results"] = results[1:]

            return primary

        # Single model mode
        if override_model:
            model = override_model
        else:
            model = candidates[0] if candidates else None

        if not model:
            raise ValueError(f"No model configured for agent {agent_type}")

        return await self._run_single_model(
            agent_type=agent_type,
            model=model,
            document=document,
            web_search=web_search,
            override_effort=override_effort,
            override_service_tier=override_service_tier,
            override_jurisdiction=override_jurisdiction,
            override_court=override_court,
            override_circuit=override_circuit,
            override_preferred_authority=override_preferred_authority,
        )

    async def _run_single_model(
        self,
        agent_type: str,
        model: str,
        document: str,
        web_search: Optional[bool],
        override_effort: Optional[str],
        override_service_tier: Optional[str],
        override_jurisdiction: Optional[str],
        override_court: Optional[str],
        override_circuit: Optional[str],
        override_preferred_authority: Optional[List[str]],
    ) -> Dict:
        """Run agent with single model. Extracted for parallel execution support."""
        # Get agent config
        agent_key = self._resolve_agent_key(agent_type)
        agent_config = self.review_settings.get("reviewAgentConfig", {}).get(agent_key)
        use_web_search = web_search if web_search is not None else agent_config.get("web_search", False)

        # Build a minimal role/system prompt per agent
        role_map = {
            "strategy": "You are a senior litigator providing strategic case guidance.",
            "drafter": "You are an expert legal drafter. Produce clear, well-cited text.",
            "self_review": "You are a senior attorney reviewing a legal document for sufficiency.",
            "citation_verify": "You verify citations and whether cases are still good law.",
            "opposing_counsel": "You are opposing counsel attacking weaknesses and counter-arguing.",
            "final_review": "You perform a final pre-filing compliance and quality review.",
            "research": "You are a legal research specialist using web search and synthesizing findings.",
        }
        base_role = role_map.get(agent_type, "You are a helpful legal assistant.")

        # Prepare messages for OpenAI-compatible chat
        sys_content = f"{base_role}\n\n{self.markdown_format_instructions}".strip()
        jctx = self._build_jurisdiction_context(
            jurisdiction=override_jurisdiction,
            court=override_court,
            circuit=override_circuit,
            preferred_authority_order=override_preferred_authority,
        )
        if jctx:
            sys_content = f"{sys_content}\n\n{jctx}"

        # Determine if we expect structured JSON output
        model_cls, expects_list = self._agent_model(agent_type)

        if model_cls is not None:
            extra_rules = [self._schema_block(model_cls)]
            if agent_type == "citation_verify":
                extra_rules.append(
                    "If multiple citations are present, return a JSON array of objects, one per citation."
                )
            sys_content = f"{sys_content}\n\n" + "\n".join(extra_rules)

        messages = [
            {"role": "system", "content": sys_content},
            {"role": "user", "content": document},
        ]

        # Execute against configured model via provider-agnostic client
        try:
            try:
                self.logger.info(
                    "Agent start | agent=%s | model=%s | web_search=%s",
                    agent_type,
                    model,
                    use_web_search,
                )
            except Exception:
                pass
            # Resolve effort and service tier preferences
            default_effort = self.review_settings.get("workflowConfig", {}).get("default_effort")

            # Get effort from agent config first, then fall back to default
            agent_effort = agent_config.get("effort") if agent_config else None
            effort = override_effort if override_effort is not None else (agent_effort or default_effort)

            # Debug logging
            try:
                self.logger.debug(
                    "Effort resolution | agent=%s | override_effort=%s | agent_effort=%s | default_effort=%s | final_effort=%s",
                    agent_type,
                    override_effort,
                    agent_effort,
                    default_effort,
                    effort,
                )
            except Exception:
                pass

            service_tier = override_service_tier or self.review_settings.get("workflowConfig", {}).get("service_tier", "auto")

            # Run sync chat_complete in thread pool for true parallel execution
            result = await asyncio.to_thread(
                chat_complete,
                model_key=model,
                messages=messages,
                temperature=self.llm_config["modelConfigurations"].get(model, {}).get("temperature", 0.01),
                max_output_tokens=self.llm_config["modelConfigurations"].get(model, {}).get("max_output_tokens"),
                service_tier=service_tier,
                effort=effort,
                web_search=use_web_search,
                pydantic_model=model_cls,
            )
        except Exception as e:
            # Surface minimal context; keep raw exception text
            try:
                self.logger.exception(
                    "LLM call failed | agent=%s | model=%s | web_search=%s",
                    agent_type,
                    model,
                    use_web_search,
                )
            except Exception:
                pass
            return {
                "model": model,
                "web_search": use_web_search,
                "error": str(e),
                "note": "LLM call failed; check API keys and provider availability",
            }

        # Track token usage
        u = result.get("usage", {})
        self.token_tracker.add(
            model=model,
            inp=int(u.get("input", 0)),
            out=int(u.get("output", 0)),
            cache=int(u.get("cached", 0)),
            effort=u.get("effort", None),
            notes=f"agent:{agent_type}",
            service_tier=str(u.get("service_tier", "auto")),
            duration=float(u.get("duration", 0.0)),
        )
        # Log meta parameters used for the call
        try:
            meta = result.get("meta", {})
            self.logger.info(
                "Agent meta | tokens_param=%s | max_tokens=%s | temp=%s | temp_supported=%s | reasoning_supported=%s",
                meta.get("tokens_param"),
                meta.get("max_tokens"),
                meta.get("temperature"),
                meta.get("supports_temperature"),
                meta.get("reasoning_supported"),
            )
        except Exception:
            pass
        try:
            self.logger.info(
                "Agent done | agent=%s | model=%s | effort=%s (requested=%s) | tier=%s | web_search=%s | in=%s | out=%s | cache=%s | dur=%.2fs",
                agent_type,
                model,
                u.get("effort"),
                u.get("effort_requested"),
                u.get("service_tier"),
                use_web_search,
                u.get("input"),
                u.get("output"),
                u.get("cached"),
                float(u.get("duration", 0.0)),
            )
        except Exception:
            pass

        # Attempt structured parse if a schema was provided
        parsed = None
        raw_json = None
        if model_cls is not None:
            text = result.get("text", "")

            # Check if the provider already returned a parsed object (xAI native SDK does this)
            meta = result.get("meta", {})
            if meta.get("api_type") == "xai_native" and text:
                # xAI already validated and serialized the Pydantic object
                # Just parse the JSON without re-validation since it's already valid
                try:
                    payload = self._parse_json_payload(text)
                    raw_json = payload
                    # Trust xAI's validation - don't re-validate
                    if expects_list and isinstance(payload, list):
                        parsed = [model_cls.model_validate(p) for p in payload]
                    elif expects_list and isinstance(payload, dict):
                        parsed = [model_cls.model_validate(payload)]
                    elif not expects_list and isinstance(payload, dict):
                        parsed = model_cls.model_validate(payload)
                except Exception as e:
                    # xAI native SDK should never fail here since it already validated
                    self.logger.warning("xAI parse returned invalid JSON despite native validation: %s", str(e))
                    parsed = None
            else:
                # OpenAI or other providers - need to validate
                try:
                    payload = self._parse_json_payload(text)
                    raw_json = payload
                    if expects_list and isinstance(payload, list):
                        parsed = [model_cls.model_validate(p) for p in payload]
                    elif expects_list and isinstance(payload, dict):
                        # Single object returned when list expected – accept singleton
                        parsed = [model_cls.model_validate(payload)]
                    elif not expects_list and isinstance(payload, dict):
                        parsed = model_cls.model_validate(payload)
                    else:
                        # Unexpected shape – retry once with explicit correction
                        raise ValidationError("Unexpected JSON shape", model_cls)
                except Exception as e:
                    self.logger.warning("Initial parse failed for %s: %s", model, str(e))
                    # Only retry for non-xAI providers (OpenAI might need retry)
                    # Retry once: ask for JSON only
                    retry_messages = messages + [
                        {
                            "role": "system",
                            "content": "Your previous output was not valid JSON per schema. Return ONLY valid JSON now.",
                        }
                    ]
                    # Run retry in thread pool for parallel execution
                    retry = await asyncio.to_thread(
                        chat_complete,
                        model_key=model,
                        messages=retry_messages,
                        temperature=self.llm_config["modelConfigurations"].get(model, {}).get("temperature", 0.01),
                        max_output_tokens=self.llm_config["modelConfigurations"].get(model, {}).get("max_output_tokens"),
                        service_tier=self.review_settings.get("workflowConfig", {}).get("service_tier", "auto"),
                        effort=effort,
                        web_search=use_web_search,
                        pydantic_model=model_cls,
                    )
                    # Track retry tokens
                    uu = retry.get("usage", {})
                    self.token_tracker.add(
                        model=model,
                        inp=int(uu.get("input", 0)),
                        out=int(uu.get("output", 0)),
                        cache=int(uu.get("cached", 0)),
                        effort=uu.get("effort", None),
                        notes=f"agent:{agent_type}:retry",
                        service_tier=str(uu.get("service_tier", "auto")),
                        duration=float(uu.get("duration", 0.0)),
                    )
                    try:
                        payload = self._parse_json_payload(retry.get("text", ""))
                        raw_json = payload
                        if expects_list and isinstance(payload, list):
                            parsed = [model_cls.model_validate(p) for p in payload]
                        elif expects_list and isinstance(payload, dict):
                            parsed = [model_cls.model_validate(payload)]
                        elif not expects_list and isinstance(payload, dict):
                            parsed = model_cls.model_validate(payload)
                    except Exception:
                        parsed = None

        # If we have citation results, optionally log them to research log
        log_path = None
        if agent_type == "citation_verify" and parsed:
            items = parsed if isinstance(parsed, list) else [parsed]
            try:
                log_path = log_citation_verifications(items)
                try:
                    self.logger.info("Citations logged to %s", log_path)
                except Exception:
                    pass
            except Exception:
                log_path = None

        out: Dict[str, Any] = {
            "model": model,
            "web_search": use_web_search,
            "agent": agent_type,
            "text": result.get("text", ""),
            "usage": u,
        }
        if parsed is not None:
            if isinstance(parsed, list):
                out["structured"] = [p.model_dump() for p in parsed]
            else:
                out["structured"] = parsed.model_dump()
            out["raw_json"] = raw_json
        if log_path:
            out["citation_log"] = log_path

        # Generate claude_prompt for Claude Code orchestration
        # This tells Claude what to do next based on agent findings
        claude_prompt = self._generate_claude_prompt(agent_type, parsed)
        if claude_prompt:
            out["claude_prompt"] = claude_prompt

        # Log usage to CSV
        try:
            from .usage_logger import log_agent_call
            # Calculate cost for this call using ppm (price per million) rates
            model_cfg = self.llm_config["modelConfigurations"].get(model, {})
            input_cost = (int(u.get("input", 0)) / 1_000_000) * model_cfg.get("input_token_ppm", 0)
            output_cost = (int(u.get("output", 0)) / 1_000_000) * model_cfg.get("output_token_ppm", 0)
            cached_cost = (int(u.get("cached", 0)) / 1_000_000) * model_cfg.get("input_token_cached_ppm", 0)
            total_cost = input_cost + output_cost + cached_cost

            log_agent_call(
                agent=agent_type,
                model=model,
                file_or_text="text" if len(document) < 100 else document[:100] + "...",
                input_tokens=int(u.get("input", 0)),
                output_tokens=int(u.get("output", 0)),
                cached_tokens=int(u.get("cached", 0)),
                cost=total_cost,
                duration=float(u.get("duration", 0.0)),
                status="success",
            )
        except Exception as e:
            try:
                self.logger.warning("Failed to log usage to CSV: %s", str(e))
            except Exception:
                pass

        return out

    def _load_guidance(
        self,
        agent_type: str,
        document: str,
        **kwargs
    ) -> Dict:
        """
        Load and process guidance prompt template for Claude Code.

        Args:
            agent_type: Agent to get guidance for
            document: Document content to inject into template
            **kwargs: Additional context variables for template

        Returns:
            Dict with guidance prompt and metadata
        """
        # Map agent type to guidance file
        guidance_file = f"{agent_type}_guidance.md"

        # Get package guidance_prompts directory
        package_dir = Path(__file__).parent
        guidance_path = package_dir / "guidance_prompts" / guidance_file

        if not guidance_path.exists():
            raise FileNotFoundError(
                f"Guidance file not found: {guidance_path}\n"
                f"Available agents: strategy, drafter, self_review, citation_verify, "
                f"opposing_counsel, final_review, organize, research"
            )

        # Load guidance template
        try:
            guidance_text = guidance_path.read_text(encoding="utf-8")
        except Exception as e:
            raise IOError(f"Failed to read guidance file {guidance_path}: {e}")

        # Build context for template variables
        context = {}

        # Get jurisdiction context from settings
        wf = self.review_settings.get("workflowConfig", {})
        jcfg = wf.get("jurisdictionConfig", {}) or {}

        context["jurisdiction"] = kwargs.get("jurisdiction") or jcfg.get("jurisdiction", "South Carolina")
        context["court"] = kwargs.get("court") or jcfg.get("court", "United States District Court")
        context["circuit"] = kwargs.get("circuit") or jcfg.get("circuit", "Fourth Circuit")

        # Document content
        context["document_content"] = document

        # Agent-specific context
        context["document_type"] = kwargs.get("document_type", "Legal Document")
        context["deadline"] = kwargs.get("deadline", "[Deadline not specified]")
        context["case_name"] = kwargs.get("case_name", "[Case name not specified]")
        context["opposing_party"] = kwargs.get("opposing_party", "Opposing Party")
        context["our_claims"] = kwargs.get("our_claims", "[Claims not specified]")
        context["their_likely_defenses"] = kwargs.get("their_likely_defenses", "[Defenses not specified]")

        # Organize-specific context
        context["inbox_files"] = kwargs.get("inbox_files", "[No files listed]")
        context["existing_structure"] = kwargs.get("existing_structure", "[Structure not provided]")

        # Process template variables
        try:
            processed_text = guidance_text.format(**context)
        except KeyError as e:
            # Template variable missing from context - provide helpful error
            self.logger.warning(
                f"Template variable {e} not provided for {agent_type} guidance. "
                f"Returning unprocessed template."
            )
            processed_text = guidance_text

        return {
            "mode": "guidance",
            "agent": agent_type,
            "prompt": processed_text,
            "context": context,
            "guidance_file": str(guidance_path),
        }

    async def review_document(
        self,
        document_path: str,
        document_type: str = "Legal Document",
        max_iterations: int = 3
    ) -> Dict:
        """
        Run full adversarial review workflow on a document.

        Args:
            document_path: Path to document file
            document_type: Type of document (e.g., "Motion for Summary Judgment")
            max_iterations: Maximum review/refinement iterations

        Returns:
            Dict with review results, issues found, and final assessment

        Example:
            >>> defender = WePublicDefender()
            >>> result = await defender.review_document(
            ...     "07_DRAFTS_AND_WORK_PRODUCT/MOTION_TO_DISMISS.docx",
            ...     document_type="Motion to Dismiss",
            ...     max_iterations=3
            ... )
            >>> print(f"Ready to file: {result['ready_to_file']}")
        """
        # TODO: Implement full review workflow
        # 1. Load document
        # 2. Run iterative review loop
        # 3. Parallel reviews (Self + Citation)
        # 4. Opposing counsel attack
        # 5. Check consensus
        # 6. Refine if needed
        # 7. Final review

        raise NotImplementedError("Document review workflow not yet implemented")

    async def research(
        self,
        topic: str,
        jurisdiction: str = "South Carolina",
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Perform legal research using web search.

        Args:
            topic: Research topic
            jurisdiction: Jurisdiction to focus on
            save_to: Optional path to save research markdown

        Returns:
            Dict with research findings, cases, and analysis

        Example:
            >>> defender = WePublicDefender()
            >>> result = await defender.research(
            ...     "statute of limitations breach of contract",
            ...     jurisdiction="South Carolina",
            ...     save_to="06_RESEARCH/sol_breach_contract.md"
            ... )
        """
        # TODO: Implement research workflow
        # - Use Grok 4 with web search
        # - Search legal databases
        # - Collect cases and statutes
        # - Analyze and summarize
        # - Save to markdown file

        raise NotImplementedError("Research function not yet implemented")

    async def strategy_review(
        self,
        case_summary: str,
        current_documents: List[str],
        gameplan_path: Optional[str] = None
    ) -> Dict:
        """
        Generate strategic recommendations for case.

        Args:
            case_summary: Brief case description
            current_documents: List of documents already filed
            gameplan_path: Optional path to GAMEPLAN.md to update

        Returns:
            Dict with next actions, deadlines, and strategic advice

        Example:
            >>> defender = WePublicDefender()
            >>> strategy = await defender.strategy_review(
            ...     case_summary="Breach of contract against Capital One",
            ...     current_documents=["Complaint", "Answer"],
            ...     gameplan_path="GAMEPLAN.md"
            ... )
        """
        # TODO: Implement strategy workflow
        # - Use GPT-5 with web search
        # - Analyze case status
        # - Research procedural requirements
        # - Generate prioritized action items
        # - Update GAMEPLAN.md

        raise NotImplementedError("Strategy review not yet implemented")

    def get_cost_report(self) -> str:
        """
        Get summary cost report for all API calls.

        Returns:
            Formatted cost report string
        """
        return self.token_tracker.report()

    def get_detailed_cost_report(self, sort_by: str = "time") -> str:
        """
        Get detailed line-by-line cost report.

        Args:
            sort_by: Sort by "time" or "cost"

        Returns:
            Detailed formatted cost report
        """
        return self.token_tracker.report_detail(sort_by=sort_by)

    def reset_costs(self):
        """Reset cost tracking for new session."""
        self.token_tracker.clear()

    def convert_to_word(
        self,
        md_file: str,
        output_file: Optional[str] = None,
        court_config: Optional[Dict] = None
    ) -> str:
        """
        Convert markdown legal document to properly formatted Word document.

        Args:
            md_file: Path to markdown file
            output_file: Path for output Word file (optional, defaults to same name with .docx)
            court_config: Dictionary of court configuration values (optional)
                Expected keys: court_name, court_district, court_division, case_number,
                plaintiff_name, plaintiff_label, defendant_name, defendant_label

        Returns:
            Path to created Word document

        Example:
            >>> defender = WePublicDefender()
            >>> word_file = defender.convert_to_word(
            ...     "motion.md",
            ...     court_config={
            ...         "court_district": "FOR THE DISTRICT OF SOUTH CAROLINA",
            ...         "case_number": "C/A No. 3:25-12345-ABC",
            ...         "plaintiff_name": "JOHN DOE",
            ...         "defendant_name": "ABC CORPORATION"
            ...     }
            ... )
            >>> print(f"Created: {word_file}")
        """
        return convert_markdown_to_word(md_file, output_file, court_config)


# TODO: Add DocumentHandler class for PDF/DOCX processing
# TODO: Add ReviewWorkflow class for iterative review loops
# TODO: Add prompt templates for each agent type
# TODO: Implement web search integration for Grok
# TODO: Add consensus checking logic
# TODO: Implement document refinement based on feedback


if __name__ == "__main__":
    print("WePublicDefender - Adversarial Legal Review System")
    print("=" * 60)
    print("\nThis is a stub implementation.")
    print("Full implementation coming soon.\n")
    print("Features to be implemented:")
    print("  - Multi-AI document review (GPT-5 + Grok 4)")
    print("  - Adversarial testing (opposing counsel mode)")
    print("  - Citation verification with web search")
    print("  - Iterative refinement loops")
    print("  - Comprehensive cost tracking")
    print("  - Legal research with web search")
    print("  - Strategic recommendations")
    print("\nSee WE_PUBLIC_DEFENDER_DESIGN.md for complete specification.")

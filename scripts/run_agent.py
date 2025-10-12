#!/usr/bin/env python
"""
Simple CLI to run a single agent against input text or a file.

Usage:
  python scripts/run_agent.py --agent self_review --file path/to/doc.md
  python scripts/run_agent.py --agent opposing_counsel --text "..."

Environment:
  OPENAI_API_KEY / XAI_API_KEY as configured in config/llm_providers.json
"""

import argparse
import asyncio
import sys
import io
from pathlib import Path
import sys

from wepublic_defender.core import WePublicDefender
from wepublic_defender.config import (
    load_review_settings,
    update_agent_preference,
    update_jurisdiction_config,
)


def read_text(file: str | None, text: str | None) -> str:
    if text:
        return text
    if file:
        p = Path(file)
        return p.read_text(encoding="utf-8")
    data = sys.stdin.read()
    if not data:
        raise SystemExit("No input provided. Use --file, --text, or pipe stdin.")
    return data


async def main() -> int:
    # Ensure UTF-8 stdout/stderr to avoid Windows cp1252 encode errors
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")  # type: ignore
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, help="Agent type: strategy|drafter|self_review|citation_verify|opposing_counsel|final_review")
    ap.add_argument("--file", help="Path to input file (markdown/text)")
    ap.add_argument("--text", help="Raw input text")
    ap.add_argument("--web-search", action="store_true", help="Force-enable web search if supported")
    ap.add_argument("--model", help="Override model key (e.g., gpt-5, gpt-4o, grok-4, grok-4-fast)")
    ap.add_argument("--run-both", action="store_true", help="Run twice using the configured model and a reasonable alternate provider model")
    ap.add_argument("--effort", choices=["minimal", "low", "medium", "high"], help="Override reasoning effort (if supported)")
    ap.add_argument("--service-tier", choices=["auto", "flex", "standard", "priority"], help="Override service tier for this run")
    ap.add_argument("--save-choice", action="store_true", help="Persist overrides (model/effort/web_search) into legal_review_settings.json for this agent")
    ap.add_argument("--jurisdiction", help="Jurisdiction override (e.g., 'South Carolina', 'Federal')")
    ap.add_argument("--court", help="Court override (e.g., 'D.S.C.', 'Richland County')")
    ap.add_argument("--circuit", help="Circuit override (e.g., 'Fourth Circuit')")
    ap.add_argument("--prefer-authority", help="Comma-separated preferred authority order (e.g., 'US Supreme Court,Fourth Circuit,South Carolina Supreme Court')")
    args = ap.parse_args()

    content = read_text(args.file, args.text)
    wpd = WePublicDefender()

    def print_result(tag: str, res: dict) -> None:
        print(f"=== Agent Output ({tag}) ===")
        print(res.get("text", ""))
        print()

    try:
        if args.run_both:
            # First run: configured or overridden model
            primary = await wpd.call_agent(
                args.agent,
                content,
                web_search=args.web_search,
                override_model=args.model,
                override_effort=args.effort,
                override_service_tier=args.service_tier,
                override_jurisdiction=args.jurisdiction,
                override_court=args.court,
                override_circuit=args.circuit,
                override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
            )
            print_result("primary", primary)

            # Alternate model selection from settings list (fallback to heuristic)
            settings = load_review_settings()
            agent_key = f"{args.agent}_agent" if not args.agent.endswith("_agent") else args.agent
            agent_cfg = settings.get("reviewAgentConfig", {}).get(agent_key, {})
            models = agent_cfg.get("models") or ([agent_cfg.get("model")] if agent_cfg.get("model") else [])
            configured_model = args.model or (models[0] if models else primary.get("model"))
            alt_model = None
            if models and len(models) > 1:
                # Choose the next configured model as alternate
                for m in models:
                    if m != configured_model:
                        alt_model = m
                        break
            else:
                # Heuristic fallback
                if configured_model and configured_model.startswith("gpt-"):
                    alt_model = "grok-4-fast" if args.agent == "citation_verify" else "grok-4"
                elif configured_model and configured_model.startswith("grok-"):
                    alt_model = "gpt-5"

            if alt_model == configured_model:
                alt_model = None

            if alt_model:
                secondary = await wpd.call_agent(
                    args.agent,
                    content,
                    web_search=args.web_search,
                    override_model=alt_model,
                    override_effort=args.effort,
                    override_service_tier=args.service_tier,
                    override_jurisdiction=args.jurisdiction,
                    override_court=args.court,
                    override_circuit=args.circuit,
                    override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
                )
                print_result("alternate", secondary)
            else:
                print("[info] No suitable alternate model determined; skipped second run.")
        else:
            result = await wpd.call_agent(
                args.agent,
                content,
                web_search=args.web_search,
                override_model=args.model,
                override_effort=args.effort,
                override_service_tier=args.service_tier,
                override_jurisdiction=args.jurisdiction,
                override_court=args.court,
                override_circuit=args.circuit,
                override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
            )
            print_result("single", result)
    except Exception as e:
        print(f"[error] {e}")
        return 1

    # Persist preferences if requested
    if args.save_choice:
        try:
            agent_key = f"{args.agent}_agent" if not args.agent.endswith("_agent") else args.agent
            update_agent_preference(
                agent_key,
                models=[args.model] if args.model else None,
                effort=args.effort,
                web_search=True if args.web_search else None,
            )
            if any([args.jurisdiction, args.court, args.circuit, args.prefer_authority]):
                update_jurisdiction_config(
                    jurisdiction=args.jurisdiction,
                    court=args.court,
                    circuit=args.circuit,
                    preferred_authority_order=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
                )
            print("[info] Saved preference to legal_review_settings.json")
        except Exception as e:
            print(f"[warn] Failed to save preference: {e}")

    print("=== Usage Summary ===")
    print(wpd.get_cost_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

import argparse
import asyncio
import sys
import io
import os
from pathlib import Path

from wepublic_defender.core import WePublicDefender
from wepublic_defender.config import load_review_settings, update_agent_preference
from wepublic_defender.logging_utils import enable_console_logging, get_logger
from wepublic_defender.usage_logger import log_agent_call


def _read_text(file: str | None, text: str | None) -> str:
    if text:
        return text
    if file:
        return Path(file).read_text(encoding="utf-8")
    raise SystemExit("No input provided. Use --file or --text.")


async def _amain(args: argparse.Namespace) -> int:
    logger = get_logger()

    try:
        content = _read_text(args.file, args.text)
    except FileNotFoundError:
        print(f"[error] input file not found: {args.file}")
        return 2
    except Exception as e:
        print(f"[error] failed to read input: {e}")
        return 2
    # Enable console logging for progress if requested
    if args.verbose or args.debug:
        enable_console_logging()

    wpd = WePublicDefender()

    def _print_result(tag: str, res: dict) -> None:
        # Handle guidance mode output differently
        if res.get("mode") == "guidance":
            print(f"=== Guidance Prompt ({tag}) ===", flush=True)
            print("This agent returned guidance for Claude Code to execute.\n", flush=True)
            print(res.get("prompt", ""), flush=True)
            print(flush=True)
        else:
            print(f"=== Agent Output ({tag}) ===", flush=True)
            print(res.get("text", ""), flush=True)
            print(flush=True)

    # Pre-compute planned model and effort for progress display
    settings = load_review_settings()
    agent_key = f"{args.agent}_agent" if not args.agent.endswith("_agent") else args.agent
    agent_cfg = settings.get("reviewAgentConfig", {}).get(agent_key, {})
    models = agent_cfg.get("models") or ([])
    planned_model = args.model or (models[0] if models else None)
    planned_effort = args.effort or agent_cfg.get("effort")
    planned_ws = args.web_search or agent_cfg.get("web_search", False)

    # Heartbeat interval (seconds)
    hb_env = os.getenv("WPD_HEARTBEAT_SEC")
    try:
        hb_sec = int(args.heartbeat) if hasattr(args, "heartbeat") and args.heartbeat else int(hb_env) if hb_env else 15
    except Exception:
        hb_sec = 15

    # Log agent invocation
    try:
        logger.info(
            "Agent run started | agent=%s | mode=%s | file=%s | model=%s | effort=%s | web_search=%s | tier=%s | run_both=%s",
            args.agent,
            args.mode,
            args.file or "text",
            planned_model or "auto",
            planned_effort or "auto",
            bool(planned_ws),
            args.service_tier or "auto",
            args.run_both,
        )
    except Exception:
        pass

    # Handle guidance mode (no API calls, just return prompt)
    if args.mode == "guidance":
        try:
            result = await wpd.call_agent(
                args.agent,
                content,
                mode="guidance",
                jurisdiction=args.jurisdiction,
                court=args.court,
                circuit=args.circuit,
            )
            if args.verbose:
                print(f"[status] Generated guidance prompt for {args.agent}", flush=True)
            _print_result("guidance", result)
            print("\n[info] Guidance mode used - no API costs incurred", flush=True)
            return 0
        except Exception as e:
            print(f"[error] Failed to load guidance: {e}", flush=True)
            return 1

    # Heartbeat task prints periodic progress
    async def _heartbeat_loop(label: str, interval: int = 15):
        t = 0
        while True:
            await asyncio.sleep(interval)
            t += interval
            print(f"[progress] {label} still running... t={t}s", flush=True)

    try:
        if args.verbose:
            print(
                f"[status] Preparing to run agent '{args.agent}'",
                flush=True,
            )
            print(
                f"[status] Running {args.agent} | model={planned_model or 'auto'} | effort={planned_effort or 'auto'} | web_search={bool(planned_ws)} | tier={args.service_tier or 'auto'}",
                flush=True,
            )
            print(
                f"[hint] Live progress every {hb_sec}s; detailed logs: .wepublic_defender/logs/wpd.log",
                flush=True,
            )
        if args.run_both:
            # Determine alternate model upfront
            settings = load_review_settings()
            agent_key = f"{args.agent}_agent" if not args.agent.endswith("_agent") else args.agent
            agent_cfg = settings.get("reviewAgentConfig", {}).get(agent_key, {})
            models = agent_cfg.get("models") or ([agent_cfg.get("model")] if agent_cfg.get("model") else [])
            configured_model = args.model or (models[0] if models else None)
            alt_model = None
            if models and len(models) > 1:
                for m in models:
                    if m != configured_model:
                        alt_model = m
                        break
            else:
                if configured_model and configured_model.startswith("gpt-"):
                    alt_model = "grok-4-fast" if args.agent == "citation_verify" else "grok-4"
                elif configured_model and configured_model.startswith("grok-"):
                    alt_model = "gpt-5"

            if not alt_model:
                print("[info] No suitable alternate model determined; skipped second run.")
            else:
                if args.verbose:
                    print(f"[status] Running both {configured_model or 'auto'} and {alt_model} IN PARALLEL", flush=True)

                # Start both heartbeats
                hb1 = asyncio.create_task(_heartbeat_loop(f"{args.agent}/{configured_model or 'auto'}", hb_sec))
                hb2 = asyncio.create_task(_heartbeat_loop(f"{args.agent}/{alt_model}", hb_sec))

                try:
                    # Run BOTH models in parallel using asyncio.gather
                    primary, secondary = await asyncio.gather(
                        wpd.call_agent(
                            args.agent,
                            content,
                            mode=args.mode,
                            web_search=args.web_search,
                            override_model=args.model,
                            override_effort=args.effort,
                            override_service_tier=args.service_tier,
                            override_jurisdiction=args.jurisdiction,
                            override_court=args.court,
                            override_circuit=args.circuit,
                            override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
                        ),
                        wpd.call_agent(
                            args.agent,
                            content,
                            mode=args.mode,
                            web_search=args.web_search,
                            override_model=alt_model,
                            override_effort=args.effort,
                            override_service_tier=args.service_tier,
                            override_jurisdiction=args.jurisdiction,
                            override_court=args.court,
                            override_circuit=args.circuit,
                            override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
                        )
                    )
                finally:
                    hb1.cancel()
                    hb2.cancel()

                # Log primary completion
                u = primary.get("usage", {})
                err = primary.get("error")
                try:
                    if err:
                        logger.error("Agent run failed | agent=%s | error=%s", args.agent, err)
                        log_agent_call(
                            agent=args.agent,
                            model=primary.get("model", "unknown"),
                            file_or_text=args.file or "text",
                            input_tokens=0,
                            output_tokens=0,
                            cached_tokens=0,
                            cost=0.0,
                            duration=0.0,
                            status="error",
                            error=str(err),
                        )
                    else:
                        logger.info(
                            "Agent run completed | agent=%s | model=%s | in=%s | out=%s | cached=%s | dur=%.2fs",
                            args.agent,
                            primary.get("model"),
                            u.get("input", 0),
                            u.get("output", 0),
                            u.get("cached", 0),
                            u.get("duration", 0),
                        )
                        # Calculate cost for this call using ppm (price per million) rates
                        model_cfg = wpd.llm_config["modelConfigurations"].get(primary.get("model", ""), {})
                        input_cost = (int(u.get("input", 0)) / 1_000_000) * model_cfg.get("input_token_ppm", 0)
                        output_cost = (int(u.get("output", 0)) / 1_000_000) * model_cfg.get("output_token_ppm", 0)
                        cached_cost = (int(u.get("cached", 0)) / 1_000_000) * model_cfg.get("input_token_cached_ppm", 0)
                        total_cost = input_cost + output_cost + cached_cost

                        log_agent_call(
                            agent=args.agent,
                            model=primary.get("model", "unknown"),
                            file_or_text=args.file or "text",
                            input_tokens=int(u.get("input", 0)),
                            output_tokens=int(u.get("output", 0)),
                            cached_tokens=int(u.get("cached", 0)),
                            cost=total_cost,
                            duration=float(u.get("duration", 0)),
                            status="success",
                        )
                except Exception:
                    pass

                if args.verbose:
                    if err:
                        print(f"[error] {args.agent} failed: {err}", flush=True)
                    else:
                        print(
                            f"[status] Completed {args.agent} | model={primary.get('model')} | in={u.get('input',0)} out={u.get('output',0)} cache={u.get('cached',0)} dur={u.get('duration',0):.1f}s",
                            flush=True,
                        )
                _print_result("primary", primary)

                # Log alternate completion
                u2 = secondary.get("usage", {})
                err2 = secondary.get("error")
                try:
                    if err2:
                        logger.error("Alternate agent run failed | agent=%s | model=%s | error=%s", args.agent, alt_model, err2)
                        log_agent_call(
                            agent=args.agent,
                            model=secondary.get("model", alt_model),
                            file_or_text=args.file or "text",
                            input_tokens=0,
                            output_tokens=0,
                            cached_tokens=0,
                            cost=0.0,
                            duration=0.0,
                            status="error",
                            error=str(err2),
                        )
                    else:
                        logger.info(
                            "Alternate agent run completed | agent=%s | model=%s | in=%s | out=%s | cached=%s | dur=%.2fs",
                            args.agent,
                            secondary.get("model"),
                            u2.get("input", 0),
                            u2.get("output", 0),
                            u2.get("cached", 0),
                            u2.get("duration", 0),
                        )
                        # Calculate cost for this call using ppm (price per million) rates
                        model_cfg = wpd.llm_config["modelConfigurations"].get(secondary.get("model", ""), {})
                        input_cost = (int(u2.get("input", 0)) / 1_000_000) * model_cfg.get("input_token_ppm", 0)
                        output_cost = (int(u2.get("output", 0)) / 1_000_000) * model_cfg.get("output_token_ppm", 0)
                        cached_cost = (int(u2.get("cached", 0)) / 1_000_000) * model_cfg.get("input_token_cached_ppm", 0)
                        total_cost = input_cost + output_cost + cached_cost

                        log_agent_call(
                            agent=args.agent,
                            model=secondary.get("model", alt_model),
                            file_or_text=args.file or "text",
                            input_tokens=int(u2.get("input", 0)),
                            output_tokens=int(u2.get("output", 0)),
                            cached_tokens=int(u2.get("cached", 0)),
                            cost=total_cost,
                            duration=float(u2.get("duration", 0)),
                            status="success",
                        )
                except Exception:
                    pass

                if args.verbose:
                    if err2:
                        print(f"[error] alternate {alt_model} failed: {err2}", flush=True)
                    else:
                        print(
                            f"[status] Completed alternate | model={secondary.get('model')} | in={u2.get('input',0)} out={u2.get('output',0)} cache={u2.get('cached',0)} dur={u2.get('duration',0):.1f}s",
                            flush=True,
                        )
                _print_result("alternate", secondary)
        else:
            hb = asyncio.create_task(_heartbeat_loop(f"{args.agent}/{planned_model or 'auto'}", hb_sec))
            try:
                result = await wpd.call_agent(
                    args.agent,
                    content,
                    mode=args.mode,
                    web_search=args.web_search,
                    override_model=args.model,
                    override_effort=args.effort,
                    override_service_tier=args.service_tier,
                    override_jurisdiction=args.jurisdiction,
                    override_court=args.court,
                    override_circuit=args.circuit,
                    override_preferred_authority=[s.strip() for s in args.prefer_authority.split(',')] if args.prefer_authority else None,
                )
            finally:
                hb.cancel()

            # Log single-run completion
            u = result.get("usage", {})
            err = result.get("error")
            try:
                if err:
                    logger.error("Agent run failed | agent=%s | error=%s", args.agent, err)
                    log_agent_call(
                        agent=args.agent,
                        model=result.get("model", "unknown"),
                        file_or_text=args.file or "text",
                        input_tokens=0,
                        output_tokens=0,
                        cached_tokens=0,
                        cost=0.0,
                        duration=0.0,
                        status="error",
                        error=str(err),
                    )
                else:
                    logger.info(
                        "Agent run completed | agent=%s | model=%s | in=%s | out=%s | cached=%s | dur=%.2fs",
                        args.agent,
                        result.get("model"),
                        u.get("input", 0),
                        u.get("output", 0),
                        u.get("cached", 0),
                        u.get("duration", 0),
                    )
                    # Calculate cost for this call using ppm (price per million) rates
                    model_cfg = wpd.llm_config["modelConfigurations"].get(result.get("model", ""), {})
                    input_cost = (int(u.get("input", 0)) / 1_000_000) * model_cfg.get("input_token_ppm", 0)
                    output_cost = (int(u.get("output", 0)) / 1_000_000) * model_cfg.get("output_token_ppm", 0)
                    cached_cost = (int(u.get("cached", 0)) / 1_000_000) * model_cfg.get("input_token_cached_ppm", 0)
                    total_cost = input_cost + output_cost + cached_cost

                    log_agent_call(
                        agent=args.agent,
                        model=result.get("model", "unknown"),
                        file_or_text=args.file or "text",
                        input_tokens=int(u.get("input", 0)),
                        output_tokens=int(u.get("output", 0)),
                        cached_tokens=int(u.get("cached", 0)),
                        cost=total_cost,
                        duration=float(u.get("duration", 0)),
                        status="success",
                    )
            except Exception:
                pass

            if args.verbose:
                if err:
                    print(f"[error] {args.agent} failed: {err}", flush=True)
                else:
                    print(
                        f"[status] Completed {args.agent} | model={result.get('model')} | in={u.get('input',0)} out={u.get('output',0)} cache={u.get('cached',0)} dur={u.get('duration',0):.1f}s",
                        flush=True,
                    )
            _print_result("single", result)
    except Exception as e:
        print(f"[error] {e}")
        return 1

    if args.save_choice:
        try:
            agent_key = f"{args.agent}_agent" if not args.agent.endswith("_agent") else args.agent
            update_agent_preference(
                agent_key,
                models=[args.model] if args.model else None,
                effort=args.effort,
                web_search=True if args.web_search else None,
            )
            try:
                logger.info(
                    "Agent preference saved | agent=%s | model=%s | effort=%s | web_search=%s",
                    agent_key,
                    args.model,
                    args.effort,
                    args.web_search,
                )
            except Exception:
                pass
            print("[info] Saved preference to per-case settings")
        except Exception as e:
            try:
                logger.warning("Failed to save agent preference | agent=%s | error=%s", agent_key, str(e))
            except Exception:
                pass
            print(f"[warn] Failed to save preference: {e}")

    print("=== Usage Summary ===")
    print(wpd.get_cost_report())
    return 0


def main() -> int:
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
    ap = argparse.ArgumentParser(prog="wpd-run-agent", description="Run a WePublicDefender agent")
    ap.add_argument("--agent", required=True, help="Agent type: strategy|drafter|self_review|citation_verify|opposing_counsel|final_review|organize|research")
    ap.add_argument("--file", help="Path to input file (markdown/text)")
    ap.add_argument("--text", help="Raw input text")
    ap.add_argument("--mode", choices=["guidance", "external-llm"], default="guidance", help="Agent mode: guidance (FREE - returns prompt for Claude Code) or external-llm (COSTS MONEY - calls LLM(s) from settings)")
    ap.add_argument("--web-search", action="store_true", help="Force-enable web search if supported")
    ap.add_argument("--model", help="Override model key (e.g., gpt-5, gpt-4o, grok-4, grok-4-fast)")
    ap.add_argument("--run-both", action="store_true", help="Run twice using the configured model and a reasonable alternate provider model")
    ap.add_argument("--effort", choices=["minimal", "low", "medium", "high"], help="Override reasoning effort (if supported)")
    ap.add_argument("--service-tier", choices=["auto", "flex", "standard", "priority"], help="Override service tier for this run")
    ap.add_argument("--save-choice", action="store_true", help="Persist overrides (model/effort/web_search) into per-case settings for this agent")
    ap.add_argument("--jurisdiction", help="Jurisdiction override (e.g., 'South Carolina', 'Federal')")
    ap.add_argument("--court", help="Court override (e.g., 'D.S.C.', 'Richland County')")
    ap.add_argument("--circuit", help="Circuit override (e.g., 'Fourth Circuit')")
    ap.add_argument("--prefer-authority", help="Comma-separated preferred authority order (e.g., 'US Supreme Court,Fourth Circuit,South Carolina Supreme Court')")
    ap.add_argument("--verbose", action="store_true", help="Print extra info; detailed logs always go to .wepublic_defender/logs/wpd.log")
    ap.add_argument("--debug", action="store_true", help="Enable DEBUG logging (same as setting WPD_DEBUG=1)")
    ap.add_argument("--heartbeat", help="Heartbeat interval seconds (default 15; or set WPD_HEARTBEAT_SEC)")

    args = ap.parse_args()
    if args.debug:
        os.environ["WPD_DEBUG"] = "1"
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    sys.exit(main())

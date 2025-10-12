import argparse
import asyncio
import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from wepublic_defender.core import WePublicDefender
from wepublic_defender.logging_utils import enable_console_logging, get_logger
from wepublic_defender.config import load_review_settings


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _pick_alt_model(agent_key: str, primary: Optional[str]) -> Optional[str]:
    s = load_review_settings()
    cfg = s.get("reviewAgentConfig", {}).get(agent_key, {})
    models = cfg.get("models") or []
    for m in models:
        if m and m != primary:
            return m
    return None


async def _heartbeat(label: str, interval: int) -> None:
    t = 0
    while True:
        await asyncio.sleep(interval)
        t += interval
        print(f"[progress] {label} running... t={t}s", flush=True)


def _counts_from_self_review(sr: Dict[str, Any]) -> Tuple[int, int, int]:
    crit = len(sr.get("critical_issues", []))
    maj = len(sr.get("major_issues", []))
    minr = len(sr.get("minor_issues", []))
    return crit, maj, minr


def _has_critical_opposition(oc: Dict[str, Any]) -> bool:
    for w in oc.get("weaknesses_found", []) or []:
        if (w.get("severity") or "").lower() == "critical":
            return True
    return False


def _ready_by_threshold(sr: Optional[Dict[str, Any]], fr: Optional[Dict[str, Any]], max_maj: int) -> bool:
    # Prefer final review result if present
    if fr:
        crit, maj, _ = _counts_from_self_review(fr)
        return crit == 0 and maj <= max_maj
    if sr:
        crit, maj, _ = _counts_from_self_review(sr)
        return crit == 0 and maj <= max_maj
    return False


async def _run_agent(
    wpd: WePublicDefender,
    agent: str,
    text: str,
    *,
    model: Optional[str],
    web_search: Optional[bool],
    effort: Optional[str],
    service_tier: Optional[str],
    heartbeat_sec: int,
) -> Dict[str, Any]:
    hb = asyncio.create_task(_heartbeat(f"{agent}/{model or 'auto'}", heartbeat_sec))
    try:
        return await wpd.call_agent(
            agent,
            text,
            web_search=web_search,
            override_model=model,
            override_effort=effort,
            override_service_tier=service_tier,
        )
    finally:
        hb.cancel()


def _save_single_agent_output(
    doc_path: Path,
    iteration: int,
    agent_name: str,
    result: Dict[str, Any],
) -> Path:
    """Save a single agent's output immediately after completion."""
    case_root = Path.cwd()
    reviews_dir = case_root / ".wepublic_defender" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_stem = doc_path.stem
    base_name = f"{doc_stem}_{timestamp}_iter{iteration}"

    json_path = reviews_dir / f"{base_name}_{agent_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)

    print(f"[saved] {agent_name} output to {json_path.relative_to(case_root)}", flush=True)
    return json_path


def _save_review_outputs(
    doc_path: Path,
    iteration: int,
    self_res: Dict[str, Any],
    cite_res: Dict[str, Any],
    opp_res: Dict[str, Any],
    final_res: Dict[str, Any],
    sr: Optional[Dict[str, Any]],
    fr: Optional[Dict[str, Any]],
    oc: Optional[Dict[str, Any]],
    crit_sr: int,
    maj_sr: int,
    crit_fr: int,
    maj_fr: int,
    has_crit_opp: bool,
) -> None:
    """Save markdown summary of all review outputs (individual JSONs already saved)."""
    # Create reviews directory in .wepublic_defender
    case_root = Path.cwd()
    reviews_dir = case_root / ".wepublic_defender" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_stem = doc_path.stem
    base_name = f"{doc_stem}_{timestamp}_iter{iteration}"

    # Create human-readable markdown summary
    md_lines = [
        f"# Review Summary: {doc_path.name}",
        f"**Iteration:** {iteration}",
        f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Document:** {doc_path}",
        "",
        "## Summary Counts",
        f"- **Self Review:** Critical={crit_sr}, Major={maj_sr}",
        f"- **Final Review:** Critical={crit_fr}, Major={maj_fr}",
        f"- **Opposing Counsel:** Critical Issues Found={has_crit_opp}",
        "",
    ]

    # Add self review details
    if sr:
        md_lines.extend([
            "## Self Review Issues",
            "",
        ])
        if sr.get("critical_issues"):
            md_lines.append("### Critical Issues")
            for issue in sr.get("critical_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")
        if sr.get("major_issues"):
            md_lines.append("### Major Issues")
            for issue in sr.get("major_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")
        if sr.get("minor_issues"):
            md_lines.append("### Minor Issues")
            for issue in sr.get("minor_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")

    # Add citation verification details
    cite_text = cite_res.get("text", "")
    if cite_text:
        md_lines.extend([
            "## Citation Verification",
            "",
            cite_text,
            "",
        ])

    # Add opposing counsel details
    if oc and oc.get("weaknesses_found"):
        md_lines.extend([
            "## Opposing Counsel Weaknesses Found",
            "",
        ])
        for weakness in oc.get("weaknesses_found", []):
            severity = weakness.get("severity", "Unknown")
            issue = weakness.get("issue", "")
            explanation = weakness.get("explanation", "")
            md_lines.append(f"### {severity}: {issue}")
            if explanation:
                md_lines.append(f"{explanation}")
            md_lines.append("")

    # Add final review details
    if fr:
        md_lines.extend([
            "## Final Review Assessment",
            "",
        ])
        if fr.get("critical_issues"):
            md_lines.append("### Critical Issues")
            for issue in fr.get("critical_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")
        if fr.get("major_issues"):
            md_lines.append("### Major Issues")
            for issue in fr.get("major_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")
        if fr.get("minor_issues"):
            md_lines.append("### Minor Issues")
            for issue in fr.get("minor_issues", []):
                md_lines.append(f"- {issue}")
            md_lines.append("")

        # Add recommendations if available
        if fr.get("recommendations"):
            md_lines.extend([
                "### Recommendations",
                "",
            ])
            for rec in fr.get("recommendations", []):
                md_lines.append(f"- {rec}")
            md_lines.append("")

    # Save markdown summary
    md_path = reviews_dir / f"{base_name}_SUMMARY.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"[saved] Review summary to {md_path.relative_to(case_root)}", flush=True)


async def main() -> int:
    logger = get_logger()

    # UTF-8 stdout/stderr to avoid Windows cp1252
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")  # type: ignore
    except Exception:
        pass

    ap = argparse.ArgumentParser(prog="wpd-review-pipeline", description="Run multi-step review pipeline with recursion")
    ap.add_argument("--file", required=True, help="Path to input markdown/text file")
    ap.add_argument("--max-iters", type=int, default=2, help="Max refinement iterations (default 2)")
    ap.add_argument("--max-major", type=int, default=2, help="Allowable major issues threshold (default 2)")
    ap.add_argument("--model", help="Override model for all agents")
    ap.add_argument("--effort", choices=["minimal", "low", "medium", "high"], help="Override reasoning effort if supported")
    ap.add_argument("--service-tier", choices=["auto", "flex", "standard", "priority"], help="Override service tier")
    ap.add_argument("--parallel", action="store_true", help="Run self_review and citation_verify in parallel")
    ap.add_argument("--run-both", action="store_true", help="Attempt to run alternate provider second and aggregate")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--heartbeat", type=int, default=int(os.getenv("WPD_HEARTBEAT_SEC", 15)), help="Heartbeat seconds (default 15)")
    ap.add_argument("--plan-only", action="store_true", help="Print the planned sequence of commands and exit (Claude can run them)")
    args = ap.parse_args()

    if args.verbose or args.debug:
        enable_console_logging()
    if args.debug:
        os.environ["WPD_DEBUG"] = "1"

    path = Path(args.file)
    if not path.exists():
        print(f"[error] file not found: {path}")
        return 2

    text = _read_text(path)
    wpd = WePublicDefender()

    # Load per-agent defaults
    s = load_review_settings()
    rac = s.get("reviewAgentConfig", {})
    def _agent_defaults(key: str) -> Tuple[Optional[str], bool]:
        cfg = rac.get(key, {})
        models = cfg.get("models") or []
        ws = bool(cfg.get("web_search", False))
        return (models[0] if models else None, ws)

    model_self, ws_self = _agent_defaults("self_review_agent")
    model_cite, ws_cite = _agent_defaults("citation_verifier_agent")
    model_opp, ws_opp = _agent_defaults("opposing_counsel_agent")
    model_final, ws_final = _agent_defaults("final_review_agent")

    # Apply global overrides
    gm = args.model
    effort = args.effort
    tier = args.service_tier

    print(f"[plan] pipeline start | file={path.name} | iters={args.max_iters} | max_major={args.max_major} | parallel={args.parallel}", flush=True)

    # Log pipeline start
    try:
        logger.info(
            "Review pipeline started | file=%s | max_iters=%s | max_major=%s | parallel=%s | model=%s | effort=%s | tier=%s",
            path.name,
            args.max_iters,
            args.max_major,
            args.parallel,
            gm or "per-agent",
            effort or "per-agent",
            tier or "auto",
        )
    except Exception:
        pass

    if args.plan_only:
        # Emit a command plan Claude can run step-by-step
        cmds: List[str] = []
        for i in range(1, args.max_iters + 1):
            pre = "wpd-run-agent"
            hb = f" --verbose --heartbeat {args.heartbeat}"
            # Model override string
            mo = f" --model {args.model}" if args.model else ""
            # Self + Citations
            if args.parallel:
                cmds.append(f"{pre} --agent self_review --file {path} {mo}{hb}")
                cmds.append(f"{pre} --agent citation_verify --file {path} --web-search {mo}{hb}")
                cmds.append("# Wait for both to finish, then:")
            else:
                cmds.append(f"{pre} --agent self_review --file {path} {mo}{hb}")
                cmds.append(f"{pre} --agent citation_verify --file {path} --web-search {mo}{hb}")
            # Opposing counsel and final
            cmds.append(f"{pre} --agent opposing_counsel --file {path} --web-search {mo}{hb}")
            cmds.append(f"{pre} --agent final_review --file {path} {mo}{hb}")
            cmds.append("# If thresholds not met or critical issues remain, revise the draft, then repeat:")
            cmds.append(f"{pre} --agent drafter --file {path} {mo}{hb}")
        print("[commands]")
        for c in cmds:
            print(c)
        print("[note] Execute commands in order. After each iteration, check issue counts and decide whether to continue.")
        print("=== Plan Only ===", flush=True)
        print("[hint] To execute automatically, run this pipeline without --plan-only.", flush=True)
        print("=== Usage Summary ===", flush=True)
        print(wpd.get_cost_report(), flush=True)
        return 0

    current_text = text
    for i in range(1, args.max_iters + 1):
        print(f"[step] iteration {i}", flush=True)

        # Log iteration start
        try:
            logger.info("Pipeline iteration started | iter=%s | max_iters=%s", i, args.max_iters)
        except Exception:
            pass

        # Self review and citation verify
        if args.parallel:
            self_task = asyncio.create_task(
                _run_agent(wpd, "self_review", current_text, model=gm or model_self, web_search=ws_self, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
            )
            cite_task = asyncio.create_task(
                _run_agent(wpd, "citation_verify", current_text, model=gm or model_cite, web_search=ws_cite, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
            )
            self_res, cite_res = await asyncio.gather(self_task, cite_task)
            # Save immediately after parallel completion
            _save_single_agent_output(path, i, "self_review", self_res)
            _save_single_agent_output(path, i, "citation_verify", cite_res)
        else:
            self_res = await _run_agent(wpd, "self_review", current_text, model=gm or model_self, web_search=ws_self, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
            _save_single_agent_output(path, i, "self_review", self_res)
            cite_res = await _run_agent(wpd, "citation_verify", current_text, model=gm or model_cite, web_search=ws_cite, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
            _save_single_agent_output(path, i, "citation_verify", cite_res)

        # Opposing counsel
        opp_res = await _run_agent(wpd, "opposing_counsel", current_text, model=gm or model_opp, web_search=ws_opp, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
        _save_single_agent_output(path, i, "opposing_counsel", opp_res)

        # Final review
        final_res = await _run_agent(wpd, "final_review", current_text, model=gm or model_final, web_search=ws_final, effort=effort, service_tier=tier, heartbeat_sec=args.heartbeat)
        _save_single_agent_output(path, i, "final_review", final_res)

        # Extract structured
        sr = (self_res.get("structured") or {}) if isinstance(self_res.get("structured"), dict) else None
        fr = (final_res.get("structured") or {}) if isinstance(final_res.get("structured"), dict) else None
        oc = (opp_res.get("structured") or {}) if isinstance(opp_res.get("structured"), dict) else None

        # Evaluate
        crit_sr, maj_sr, _ = _counts_from_self_review(sr or {})
        crit_fr, maj_fr, _ = _counts_from_self_review(fr or {})
        has_crit_opp = _has_critical_opposition(oc or {})

        print(
            f"[summary] iter={i} | self: crit={crit_sr} maj={maj_sr} | final: crit={crit_fr} maj={maj_fr} | opp_critical={has_crit_opp}",
            flush=True,
        )

        # Log iteration results
        try:
            logger.info(
                "Pipeline iteration results | iter=%s | self_crit=%s | self_maj=%s | final_crit=%s | final_maj=%s | opp_critical=%s",
                i,
                crit_sr,
                maj_sr,
                crit_fr,
                maj_fr,
                has_crit_opp,
            )
        except Exception:
            pass

        # Save review outputs to disk
        _save_review_outputs(
            doc_path=path,
            iteration=i,
            self_res=self_res,
            cite_res=cite_res,
            opp_res=opp_res,
            final_res=final_res,
            sr=sr,
            fr=fr,
            oc=oc,
            crit_sr=crit_sr,
            maj_sr=maj_sr,
            crit_fr=crit_fr,
            maj_fr=maj_fr,
            has_crit_opp=has_crit_opp,
        )

        if _ready_by_threshold(sr, fr, args.max_major) and not has_crit_opp:
            print("[result] Document meets thresholds. Pipeline complete.", flush=True)
            try:
                logger.info("Pipeline completed successfully | iter=%s | thresholds_met=True", i)
            except Exception:
                pass
            break

        # Otherwise try to refine draft with drafter
        print("[action] Refining draft based on findings...", flush=True)

        # Log refinement decision
        try:
            logger.info("Pipeline refining draft | iter=%s | crit_issues=%s | maj_issues=%s", i, crit_fr or crit_sr, maj_fr or maj_sr)
        except Exception:
            pass

        # Build a brief summary for drafter
        summary = []
        if sr:
            summary.append(f"Self Review: Critical={crit_sr}, Major={maj_sr}")
            if sr.get("critical_issues"):
                summary.append("Critical: " + "; ".join(sr.get("critical_issues", [])[:5]))
            if sr.get("major_issues"):
                summary.append("Major: " + "; ".join(sr.get("major_issues", [])[:5]))
        if oc:
            wk = oc.get("weaknesses_found", [])
            crit_w = [w.get("issue") for w in wk if (w.get("severity") or '').lower() == 'critical']
            maj_w = [w.get("issue") for w in wk if (w.get("severity") or '').lower() == 'major']
            if crit_w:
                summary.append("Opposing (critical): " + "; ".join(crit_w[:5]))
            if maj_w:
                summary.append("Opposing (major): " + "; ".join(maj_w[:5]))
        brief = "\n".join(summary)
        drafter_prompt = (
            "Revise the following markdown draft to address the issues found. Prioritize fixing CRITICAL then MAJOR items.\n"
            "Preserve headings, citations, and add key quotes + pin cites from verified authorities where relevant.\n"
            f"Issues summary:\n{brief}\n\n"
            "Return ONLY the revised markdown in the output."
        )
        drafter_input = f"{drafter_prompt}\n\n---\n\n{current_text}"
        drafter_res = await _run_agent(
            wpd,
            "drafter",
            drafter_input,
            model=gm or (load_review_settings().get("reviewAgentConfig", {}).get("drafter_agent", {}).get("models", [None])[0]),
            web_search=False,
            effort=effort,
            service_tier=tier,
            heartbeat_sec=args.heartbeat,
        )
        new_text = drafter_res.get("text") or current_text
        # Save iteration output next to original
        out_path = path.with_name(f"{path.stem}.rev{i}{path.suffix}")
        out_path.write_text(new_text, encoding="utf-8")
        print(f"[write] {out_path.name}", flush=True)

        # Log draft revision write
        try:
            logger.info("Pipeline draft revised | iter=%s | output=%s", i, out_path.name)
        except Exception:
            pass

        current_text = new_text

    # Final cost summary
    print("=== Usage Summary ===", flush=True)
    print(wpd.get_cost_report(), flush=True)

    # Log pipeline completion
    try:
        logger.info("Review pipeline finished | file=%s | total_iters=%s", path.name, args.max_iters)
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

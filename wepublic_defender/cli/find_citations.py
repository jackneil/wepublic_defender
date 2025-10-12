import argparse
import io
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from wepublic_defender.providers.courtlistener_client import search_opinions
from wepublic_defender.config import load_review_settings
from wepublic_defender.logging_utils import enable_console_logging, get_logger


def _ensure_utf8():
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")  # type: ignore
    except Exception:
        pass


def _load_props(args: argparse.Namespace) -> List[str]:
    if args.text:
        return [args.text.strip()]
    if args.props_file:
        p = Path(args.props_file)
        if not p.exists():
            raise FileNotFoundError(str(p))
        if p.suffix.lower() in (".json", ".json5"):
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return [str(x) for x in data]
            raise ValueError("props_file JSON must be a list of strings")
        # plain text: one proposition per line
        return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    raise SystemExit("Provide --text or --props-file")


def _juris_defaults() -> Dict[str, Optional[str]]:
    s = load_review_settings()
    j = (s.get("workflowConfig", {}).get("jurisdictionConfig", {}) or {})
    return {
        "jurisdiction": j.get("jurisdiction"),
        "court": j.get("court"),
        "circuit": j.get("circuit"),
    }


def main() -> int:
    logger = get_logger()
    _ensure_utf8()

    ap = argparse.ArgumentParser(prog="wpd-find-citations", description="Find candidate citations via CourtListener search")
    ap.add_argument("--text", help="Single proposition text")
    ap.add_argument("--props-file", help="Path to file with propositions (json list or newline-delimited)")
    ap.add_argument("--limit", type=int, default=10, help="Max results per proposition (default 10)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    if args.verbose or args.debug:
        enable_console_logging()
    if args.debug:
        os.environ["WPD_DEBUG"] = "1"

    # Token UX
    if not os.getenv("COURTLISTENER_TOKEN"):
        print("[warn] COURTLISTENER_TOKEN not set. Some endpoints may rate-limit or block.")
        print("[hint] Get a token from https://www.courtlistener.com/api/ and add COURTLISTENER_TOKEN=... to your .env at case root.")

    props = _load_props(args)
    juris = _juris_defaults()

    # Log citation search start
    try:
        logger.info("Citation search started | propositions=%s | limit=%s", len(props), args.limit)
    except Exception:
        pass

    out_json: List[Dict[str, Any]] = []
    out_md_lines: List[str] = ["# Citation Candidates\n"]

    for p in props:
        print(f"[status] Searching CourtListener for: {p}", flush=True)
        # Basic query; Claude can refine queries upstream if needed
        res = search_opinions(p, page_size=args.limit, jurisdiction=None, court=None)
        hits = res.get("results") or res.get("results", []) or res.get("results", [])
        # Some APIs return 'results', others 'results' field with objects — we will tolerate either
        items = res.get("results") or res.get("results") or res.get("results")
        # Many CourtListener responses put data in 'results'
        results = res.get("results") or []
        # Normalize
        entries = []
        for r in results:
            entries.append({
                "score": r.get("score"),
                "caseName": r.get("caseName"),
                "citation": r.get("citation"),
                "court": r.get("court"),
                "dateFiled": r.get("dateFiled"),
                "absolute_url": r.get("absolute_url") or r.get("cluster_url") or r.get("opinion_url"),
                "raw": r,
            })
        out_json.append({"proposition": p, "results": entries})

        out_md_lines.append(f"\n## Proposition\n{p}\n")
        if not entries:
            out_md_lines.append("- No results found.")
        else:
            for e in entries[: args.limit]:
                url = e.get("absolute_url") or ""
                out_md_lines.append(f"- {e.get('caseName')} ({e.get('citation')}) — {e.get('court')} — {e.get('dateFiled')}\n  {url}")

    # Write outputs
    out_dir = Path("06_RESEARCH")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "citation_candidates.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False), encoding="utf-8")
    (out_dir / "citation_candidates.md").write_text("\n".join(out_md_lines), encoding="utf-8")
    print("[write] 06_RESEARCH/citation_candidates.json", flush=True)
    print("[write] 06_RESEARCH/citation_candidates.md", flush=True)

    # Log completion
    total_results = sum(len(p.get("results", [])) for p in out_json)
    try:
        logger.info(
            "Citation search completed | propositions=%s | total_results=%s | output=06_RESEARCH/citation_candidates.*",
            len(props),
            total_results,
        )
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


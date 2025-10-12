import argparse
import asyncio
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from wepublic_defender.providers.courtlistener_client import get_opinion_by_citation
from wepublic_defender.logging_utils import enable_console_logging, get_logger
from wepublic_defender.research_log import log_citation_verifications
from wepublic_defender.core import WePublicDefender


CITE_RE = re.compile(r"\b\d{1,3}\s+[A-Z][A-Za-z\.\d]*\s+\d+\b.*?\(.*?\)")


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


def _read_citations(args: argparse.Namespace) -> List[str]:
    if args.text:
        return [args.text.strip()]
    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise FileNotFoundError(str(p))
        txt = p.read_text(encoding="utf-8")
        cites = CITE_RE.findall(txt)
        return list(dict.fromkeys([c.strip() for c in cites]))
    raise SystemExit("Provide --text or --file")


def main() -> int:
    logger = get_logger()
    _ensure_utf8()

    ap = argparse.ArgumentParser(prog="wpd-verify-citation", description="Verify citations using CourtListener and log results")
    ap.add_argument("--file", help="File to scan for citations (markdown/text)")
    ap.add_argument("--text", help="Single citation string to verify")
    ap.add_argument("--limit", type=int, default=1, help="Results to consider per citation (default 1)")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    if args.verbose or args.debug:
        enable_console_logging()
    if args.debug:
        os.environ["WPD_DEBUG"] = "1"

    if not os.getenv("COURTLISTENER_TOKEN"):
        print("[warn] COURTLISTENER_TOKEN not set. Some endpoints may rate-limit or block.")
        print("[hint] Get a token from https://www.courtlistener.com/api/ and add COURTLISTENER_TOKEN=... to your .env at case root.")

    cites = _read_citations(args)
    if not cites:
        print("[info] No citations found.")
        return 0

    # Log citation verification start
    try:
        logger.info("Citation verification started | citations=%s | source=%s", len(cites), args.file or "text")
    except Exception:
        pass

    # Use the citation_verifier agent to produce structured results once we resolve via CourtListener
    wpd = WePublicDefender()
    verified: List[Dict[str, Any]] = []
    for c in cites:
        print(f"[status] Resolving citation: {c}", flush=True)
        res = get_opinion_by_citation(c)
        # We trust the top hit; Claude can refine logic if needed
        results = res.get("results") or []
        if not results:
            print(f"[warn] No CourtListener matches for: {c}")
            continue
        top = results[0]
        # Build a verification prompt: include citation, case_name, court, date and URL
        summary = {
            "case_name": top.get("caseName"),
            "citation": c,
            "court": top.get("court"),
            "date_filed": top.get("dateFiled"),
            "url": top.get("absolute_url") or top.get("cluster_url") or top.get("opinion_url"),
        }
        text = (
            "Verify whether the following citation is accurate, still good law, and supports the proposition in our draft.\n"
            f"Citation: {c}\n"
            f"Metadata: {json.dumps(summary, ensure_ascii=False)}\n"
            "Return structured JSON only."
        )
        result = asyncio.run(wpd.call_agent("citation_verify", text))  # type: ignore
        if result.get("structured"):
            items = result["structured"] if isinstance(result["structured"], list) else [result["structured"]]
            verified.extend(items)
    if verified:
        log_path = log_citation_verifications(verified)  # type: ignore
        print(f"[write] {log_path}", flush=True)

    # Log verification completion
    try:
        logger.info(
            "Citation verification completed | citations=%s | verified=%s | output=06_RESEARCH/CITATIONS_LOG.md",
            len(cites),
            len(verified),
        )
    except Exception:
        pass

    print("=== Usage Summary ===", flush=True)
    print(wpd.get_cost_report(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


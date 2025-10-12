"""
Utilities to persist agent outputs (especially citation verification) into
Markdown logs to avoid re-checking and to provide an auditable trail.

Default log path: 06_RESEARCH/CITATIONS_LOG.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from .models.legal_responses import CitationVerificationResult
from .logging_utils import get_logger


DEFAULT_LOG = Path("06_RESEARCH") / "CITATIONS_LOG.md"


def _format_citation_header(r: CitationVerificationResult) -> str:
    """
    Format citation as markdown header.

    Args:
        r: Citation verification result

    Returns:
        Markdown header string

    Examples:
        >>> from datetime import date
        >>> from wepublic_defender.models.legal_responses import CitationVerificationResult
        >>> r = CitationVerificationResult(
        ...     case_name="Smith v. Jones",
        ...     citation="123 S.E.2d 456",
        ...     still_good_law=True,
        ...     verified_date=date(2025, 10, 12),
        ...     confidence=95
        ... )
        >>> _format_citation_header(r)
        '## Smith v. Jones, 123 S.E.2d 456'
    """
    title = f"{r.case_name}, {r.citation}"
    return f"## {title}".strip()


def _format_citation_block(r: CitationVerificationResult) -> str:
    lines: list[str] = []
    lines.append(_format_citation_header(r))
    lines.append("")
    lines.append(f"Verified: {r.verified_date}")
    lines.append(f"Still good law: {'Yes' if r.still_good_law else 'No'}")
    if r.supports_position is not None:
        lines.append(f"Supports our position: {'Yes' if r.supports_position else 'No'}")
    if r.confidence is not None:
        lines.append(f"Confidence: {r.confidence}")
    if r.jurisdiction or r.court or r.year:
        parts = [p for p in [r.jurisdiction, r.court, str(r.year) if r.year else None] if p]
        if parts:
            lines.append("Jurisdiction/Court/Year: " + ", ".join(parts))
    if r.holding:
        lines.append("")
        lines.append("Holding:")
        lines.append(r.holding.strip())
    if r.supported_propositions:
        lines.append("")
        lines.append("Propositions Supported:")
        for p in r.supported_propositions:
            lines.append(f"- {p}")
    if r.contrary_authority:
        lines.append("")
        lines.append("Contrary/Distinguishing Points:")
        for p in r.contrary_authority:
            lines.append(f"- {p}")
    if r.key_passages:
        lines.append("")
        lines.append("Key Passages:")
        for i, q in enumerate(r.key_passages):
            pin = f" ({r.pin_cites[i]})" if i < len(r.pin_cites) else ""
            lines.append(f"> {q.strip()}{pin}")
    if r.applies_to_sections:
        lines.append("")
        lines.append("Applies to Sections:")
        for s in r.applies_to_sections:
            lines.append(f"- {s}")
    if r.issues_found:
        lines.append("")
        lines.append("Issues Found:")
        for i in r.issues_found:
            lines.append(f"- {i}")
    if r.relevance:
        lines.append("")
        lines.append("Relevance:")
        lines.append(r.relevance.strip())
    if r.notes:
        lines.append("")
        lines.append("Notes:")
        lines.append(r.notes.strip())
    lines.append("")
    return "\n".join(lines)


def _upsert_section(md: str, header: str, body: str) -> str:
    """
    Insert or replace a section beginning with `header` (a line) in md text.

    Args:
        md: Existing markdown content
        header: Section header to find/replace (e.g., "## Smith v. Jones")
        body: New content for the section

    Returns:
        Updated markdown with section upserted

    Examples:
        >>> # Test appending new section
        >>> md = "# Log\\n\\n## Case 1\\nContent 1"
        >>> result = _upsert_section(md, "## Case 2", "## Case 2\\nContent 2")
        >>> "Case 2" in result
        True
        >>> "Content 2" in result
        True

        >>> # Test replacing existing section
        >>> md = "# Log\\n\\n## Case 1\\nOld content\\n\\n## Case 2\\nContent 2"
        >>> result = _upsert_section(md, "## Case 1", "## Case 1\\nNew content")
        >>> "New content" in result
        True
        >>> "Old content" not in result
        True
    """
    lines = md.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == header.strip():
            start = i
            break
    if start is None:
        # append with spacer
        return (md + ("\n\n" if md.strip() else "")) + body.strip() + "\n"
    # find end: next line that starts with '## '
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    new_lines = lines[:start] + body.strip().splitlines() + lines[end:]
    return "\n".join(new_lines) + ("\n" if not new_lines[-1].endswith("\n") else "")


def log_citation_verifications(
    results: Iterable[CitationVerificationResult],
    log_path: Optional[str] = None,
) -> str:
    """
    Upsert citation verification results into a Markdown log.

    Returns the path of the log file written.
    """
    logger = get_logger()
    path = Path(log_path) if log_path else DEFAULT_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Citation Verification Log\n\n"

    results_list = list(results)
    count = len(results_list)

    for r in results_list:
        header = _format_citation_header(r)
        block = _format_citation_block(r)
        current = _upsert_section(current, header, block)

    path.write_text(current, encoding="utf-8")

    try:
        logger.info(
            "Citations logged | count=%s | path=%s",
            count,
            path,
        )
    except Exception:
        pass

    return str(path)


__all__ = ["log_citation_verifications"]


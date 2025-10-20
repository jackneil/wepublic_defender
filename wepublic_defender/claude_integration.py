"""
Claude Code Integration Module

Helpers for Claude Code to save its review results in the same format
as external LLM agents, enabling comparison and synthesis.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib


def save_claude_review(
    agent_type: str,
    results: Dict[str, Any],
    file_path: Optional[str] = None,
    case_root: Optional[Path] = None
) -> Path:
    """
    Save Claude Code's review results in standard WePublicDefender format.

    Args:
        agent_type: Type of agent (self_review, citation_verify, etc.)
        results: Review results matching agent's expected schema
        file_path: Optional document that was reviewed
        case_root: Case root directory (defaults to current directory)

    Returns:
        Path to saved JSON file

    Example:
        >>> results = {
        ...     "critical_issues": ["Missing jurisdiction"],
        ...     "major_issues": ["Weak causation"],
        ...     "minor_issues": ["Typos"],
        ...     "ready_to_file": False
        ... }
        >>> save_claude_review("self_review", results)
    """
    if case_root is None:
        case_root = Path.cwd()
    else:
        case_root = Path(case_root)

    # Ensure reviews directory exists
    review_dir = case_root / ".wepublic_defender" / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_type}_claude_code_{timestamp}.json"
    filepath = review_dir / filename

    # Add metadata
    enhanced_results = {
        "agent": agent_type,
        "model": "claude-code",
        "timestamp": datetime.now().isoformat(),
        "file_reviewed": file_path,
        **results  # Include all the actual review results
    }

    # Add hash for comparison
    if file_path and Path(file_path).exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            enhanced_results["file_hash"] = hashlib.md5(content.encode()).hexdigest()

    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(enhanced_results, f, indent=2, ensure_ascii=False)

    return filepath


def load_all_reviews(
    agent_type: str,
    case_root: Optional[Path] = None,
    include_claude: bool = True
) -> Dict[str, Any]:
    """
    Load all reviews for a specific agent type.

    Args:
        agent_type: Type of agent to load reviews for
        case_root: Case root directory
        include_claude: Whether to include Claude Code's reviews

    Returns:
        Dictionary mapping model names to their review results
    """
    if case_root is None:
        case_root = Path.cwd()
    else:
        case_root = Path(case_root)

    review_dir = case_root / ".wepublic_defender" / "reviews"
    if not review_dir.exists():
        return {}

    # Find all matching review files
    pattern = f"{agent_type}_*.json"
    reviews = {}

    for file in review_dir.glob(pattern):
        # Skip Claude's reviews if not wanted
        if not include_claude and "claude_code" in file.name:
            continue

        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                model = data.get("model", "unknown")
                # Keep latest review per model
                if model not in reviews or data.get("timestamp", "") > reviews[model].get("timestamp", ""):
                    reviews[model] = data
        except Exception as e:
            print(f"Warning: Failed to load {file}: {e}")

    return reviews


def compare_reviews(
    agent_type: str,
    case_root: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Compare all reviews for an agent and identify consensus/disputes.

    Args:
        agent_type: Type of agent to compare reviews for
        case_root: Case root directory

    Returns:
        Comparison analysis with consensus and disputed findings
    """
    reviews = load_all_reviews(agent_type, case_root)

    if not reviews:
        return {"error": "No reviews found", "agent": agent_type}

    comparison = {
        "agent": agent_type,
        "models_reviewed": list(reviews.keys()),
        "total_models": len(reviews),
        "timestamp": datetime.now().isoformat(),
    }

    # For citation_verify, handle list results
    if agent_type == "citation_verify":
        comparison["citations_analyzed"] = _compare_citations(reviews)
    else:
        # For other agents, compare issues
        comparison["consensus"] = _find_consensus(reviews)
        comparison["disputes"] = _find_disputes(reviews)
        comparison["unique_findings"] = _find_unique(reviews)

    # Overall assessment comparison
    comparison["readiness"] = _compare_readiness(reviews)

    return comparison


def _find_consensus(reviews: Dict[str, Any]) -> Dict[str, List[str]]:
    """Find issues that all models agree on."""
    consensus = {
        "critical": [],
        "major": [],
        "minor": []
    }

    for severity in ["critical_issues", "major_issues", "minor_issues"]:
        # Collect all issues by severity
        all_issues = {}
        for model, review in reviews.items():
            for issue in review.get(severity, []):
                # Normalize issue text for comparison
                normalized = issue.lower().strip()
                if normalized not in all_issues:
                    all_issues[normalized] = {"text": issue, "models": []}
                all_issues[normalized]["models"].append(model)

        # Find consensus (all models agree)
        severity_key = severity.replace("_issues", "")
        for normalized, info in all_issues.items():
            if len(info["models"]) == len(reviews):
                consensus[severity_key].append(info["text"])

    return consensus


def _find_disputes(reviews: Dict[str, Any]) -> Dict[str, List[Dict]]:
    """Find issues that some but not all models identified."""
    disputes = {
        "critical": [],
        "major": [],
        "minor": []
    }

    for severity in ["critical_issues", "major_issues", "minor_issues"]:
        all_issues = {}
        for model, review in reviews.items():
            for issue in review.get(severity, []):
                normalized = issue.lower().strip()
                if normalized not in all_issues:
                    all_issues[normalized] = {"text": issue, "models": []}
                all_issues[normalized]["models"].append(model)

        severity_key = severity.replace("_issues", "")
        for normalized, info in all_issues.items():
            if 1 < len(info["models"]) < len(reviews):
                disputes[severity_key].append({
                    "issue": info["text"],
                    "flagged_by": info["models"],
                    "missed_by": [m for m in reviews.keys() if m not in info["models"]]
                })

    return disputes


def _find_unique(reviews: Dict[str, Any]) -> Dict[str, Dict]:
    """Find issues unique to each model."""
    unique = {}

    for model in reviews.keys():
        unique[model] = {
            "critical": [],
            "major": [],
            "minor": []
        }

    for severity in ["critical_issues", "major_issues", "minor_issues"]:
        all_issues = {}
        for model, review in reviews.items():
            for issue in review.get(severity, []):
                normalized = issue.lower().strip()
                if normalized not in all_issues:
                    all_issues[normalized] = {"text": issue, "models": []}
                all_issues[normalized]["models"].append(model)

        severity_key = severity.replace("_issues", "")
        for normalized, info in all_issues.items():
            if len(info["models"]) == 1:
                model = info["models"][0]
                unique[model][severity_key].append(info["text"])

    # Remove models with no unique findings
    unique = {k: v for k, v in unique.items()
              if any(v[sev] for sev in ["critical", "major", "minor"])}

    return unique


def _compare_readiness(reviews: Dict[str, Any]) -> Dict[str, Any]:
    """Compare ready_to_file assessments."""
    readiness = {
        "ready": [],
        "not_ready": [],
        "consensus": None
    }

    for model, review in reviews.items():
        if review.get("ready_to_file", False):
            readiness["ready"].append(model)
        else:
            readiness["not_ready"].append(model)

    if len(readiness["ready"]) == len(reviews):
        readiness["consensus"] = "READY TO FILE"
    elif len(readiness["not_ready"]) == len(reviews):
        readiness["consensus"] = "NOT READY"
    else:
        readiness["consensus"] = "DISPUTED"

    return readiness


def _compare_citations(reviews: Dict[str, Any]) -> Dict[str, Any]:
    """Special comparison for citation verification results."""
    all_citations = {}

    for model, review in reviews.items():
        # Handle both structured and text results
        citations = review.get("structured", [])
        if not citations and "citations" in review:
            citations = review["citations"]

        for cite in citations:
            case_name = cite.get("case_name", "Unknown")
            if case_name not in all_citations:
                all_citations[case_name] = {
                    "case_name": case_name,
                    "citation": cite.get("citation", ""),
                    "good_law": {},
                    "supports": {},
                    "issues": {}
                }

            all_citations[case_name]["good_law"][model] = cite.get("still_good_law", None)
            all_citations[case_name]["supports"][model] = cite.get("supports_position", None)
            all_citations[case_name]["issues"][model] = cite.get("issues_found", [])

    return all_citations


def synthesize_reviews(
    agent_type: str,
    case_root: Optional[Path] = None
) -> str:
    """
    Generate a human-readable synthesis of all reviews.

    Args:
        agent_type: Type of agent to synthesize reviews for
        case_root: Case root directory

    Returns:
        Formatted synthesis report
    """
    comparison = compare_reviews(agent_type, case_root)

    if "error" in comparison:
        return f"No reviews found for {agent_type}"

    report = []
    report.append(f"# Review Synthesis: {agent_type}")
    report.append(f"Models reviewed: {', '.join(comparison['models_reviewed'])}")
    report.append("")

    # Readiness
    readiness = comparison.get("readiness", {})
    report.append(f"## Filing Readiness: {readiness.get('consensus', 'UNKNOWN')}")
    if readiness.get("ready"):
        report.append(f"- Ready: {', '.join(readiness['ready'])}")
    if readiness.get("not_ready"):
        report.append(f"- Not Ready: {', '.join(readiness['not_ready'])}")
    report.append("")

    # Consensus findings
    consensus = comparison.get("consensus", {})
    if any(consensus.values()):
        report.append("## Consensus Findings (All Models Agree)")
        for severity in ["critical", "major", "minor"]:
            if consensus.get(severity):
                report.append(f"\n### {severity.title()} Issues")
                for issue in consensus[severity]:
                    report.append(f"- {issue}")
        report.append("")

    # Disputed findings
    disputes = comparison.get("disputes", {})
    if any(disputes.values()):
        report.append("## Disputed Findings (Partial Agreement)")
        for severity in ["critical", "major", "minor"]:
            if disputes.get(severity):
                report.append(f"\n### {severity.title()} Issues")
                for dispute in disputes[severity]:
                    report.append(f"- {dispute['issue']}")
                    report.append(f"  - Flagged by: {', '.join(dispute['flagged_by'])}")
                    report.append(f"  - Missed by: {', '.join(dispute['missed_by'])}")
        report.append("")

    # Unique findings
    unique = comparison.get("unique_findings", {})
    if unique:
        report.append("## Unique Findings by Model")
        for model, findings in unique.items():
            if any(findings.values()):
                report.append(f"\n### {model}")
                for severity in ["critical", "major", "minor"]:
                    if findings.get(severity):
                        report.append(f"#### {severity.title()}")
                        for issue in findings[severity]:
                            report.append(f"- {issue}")
        report.append("")

    return "\n".join(report)


# Convenience function for Claude Code to use directly
def claude_review_and_save(
    agent_type: str,
    document_path: str,
    findings: Dict[str, List[str]],
    overall_assessment: str,
    ready_to_file: bool = False
) -> Path:
    """
    Simplified interface for Claude Code to save review results.

    Args:
        agent_type: Agent type (self_review, citation_verify, etc.)
        document_path: Path to document reviewed
        findings: Dict with 'critical', 'major', 'minor' lists
        overall_assessment: Text assessment
        ready_to_file: Whether document is ready

    Returns:
        Path to saved review file

    Example:
        >>> claude_review_and_save(
        ...     "self_review",
        ...     "draft.md",
        ...     {
        ...         "critical": ["Missing jurisdiction"],
        ...         "major": ["Weak causation"],
        ...         "minor": ["Typos"]
        ...     },
        ...     "Needs significant revision",
        ...     ready_to_file=False
        ... )
    """
    results = {
        "critical_issues": findings.get("critical", []),
        "major_issues": findings.get("major", []),
        "minor_issues": findings.get("minor", []),
        "overall_assessment": overall_assessment,
        "ready_to_file": ready_to_file
    }

    return save_claude_review(agent_type, results, document_path)
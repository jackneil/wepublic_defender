"""
Generate comprehensive prompts for Claude.ai Deep Research mode.

This module analyzes current case state and creates specialized prompts
for conducting deep legal research using Claude.ai's Deep Research feature.
The prompts are tailored to the case stage and current research needs.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _detect_case_stage(base_path: Path) -> str:
    """
    Detect current stage of the case based on directory contents.

    Returns:
        Stage identifier: 'new_case', 'planning', 'filed', 'discovery', 'motions', 'trial_prep'

    Examples:
        >>> base = Path('.')
        >>> stage = _detect_case_stage(base)
        >>> stage in ['new_case', 'planning', 'filed', 'discovery', 'motions', 'trial_prep']
        True
    """
    pleadings = base_path / "02_PLEADINGS"
    discovery = base_path / "03_DISCOVERY"

    # Check if complaint filed
    has_complaint = False
    if pleadings.exists():
        complaint_dirs = list((pleadings / "01_Complaint").glob("*")) if (pleadings / "01_Complaint").exists() else []
        has_complaint = len(complaint_dirs) > 0

    # Check if discovery started
    has_discovery = False
    if discovery.exists():
        discovery_files = list(discovery.rglob("*"))
        has_discovery = len([f for f in discovery_files if f.is_file()]) > 0

    # Check if any motions filed
    has_motions = False
    if pleadings.exists():
        motion_dirs = list((pleadings / "03_Motions").glob("*")) if (pleadings / "03_Motions").exists() else []
        has_motions = len(motion_dirs) > 0

    # Determine stage
    if not has_complaint:
        # No complaint filed - check if we have case overview
        case_overview = base_path / "01_CASE_OVERVIEW"
        has_overview = case_overview.exists() and len(list(case_overview.glob("*.md"))) > 0
        return "planning" if has_overview else "new_case"
    elif has_motions:
        return "motions"
    elif has_discovery:
        return "discovery"
    else:
        return "filed"


def _read_gameplan(base_path: Path) -> Optional[str]:
    """
    Read GAMEPLAN.md if it exists.

    Examples:
        >>> base = Path('.')
        >>> gameplan = _read_gameplan(base)
        >>> gameplan is None or isinstance(gameplan, str)
        True
    """
    gameplan_path = base_path / "GAMEPLAN.md"
    if gameplan_path.exists():
        return gameplan_path.read_text(encoding="utf-8")
    return None


def _read_case_overview(base_path: Path) -> Dict[str, str]:
    """
    Read case overview documents.

    Returns:
        Dict mapping filename to content

    Examples:
        >>> base = Path('.')
        >>> overview = _read_case_overview(base)
        >>> isinstance(overview, dict)
        True
    """
    overview_dir = base_path / "01_CASE_OVERVIEW"
    result = {}

    if overview_dir.exists():
        for md_file in overview_dir.glob("*.md"):
            if md_file.name != "README.md":
                try:
                    result[md_file.stem] = md_file.read_text(encoding="utf-8")
                except Exception:
                    pass

    return result


def _get_filed_documents(base_path: Path) -> List[str]:
    """
    Get list of filed documents from pleadings directory.

    Examples:
        >>> base = Path('.')
        >>> docs = _get_filed_documents(base)
        >>> isinstance(docs, list)
        True
    """
    pleadings = base_path / "02_PLEADINGS"
    docs = []

    if pleadings.exists():
        for subdir in pleadings.iterdir():
            if subdir.is_dir():
                for doc in subdir.glob("*"):
                    if doc.is_file():
                        docs.append(f"{subdir.name}/{doc.name}")

    return docs


def _get_research_done(base_path: Path) -> List[str]:
    """
    Get list of research already completed.

    Examples:
        >>> base = Path('.')
        >>> research = _get_research_done(base)
        >>> isinstance(research, list)
        True
    """
    research_dir = base_path / "06_RESEARCH"
    topics = []

    if research_dir.exists():
        for md_file in research_dir.rglob("*.md"):
            if md_file.name not in ["README.md", "CITATIONS_LOG.md"]:
                topics.append(md_file.stem.replace("_", " ").title())

    return topics


def _load_jurisdiction_config(base_path: Path) -> Dict:
    """
    Load jurisdiction configuration from settings.

    Examples:
        >>> base = Path('.')
        >>> config = _load_jurisdiction_config(base)
        >>> isinstance(config, dict)
        True
    """
    settings_path = base_path / ".wepublic_defender" / "legal_review_settings.json"

    if settings_path.exists():
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get("workflowConfig", {}).get("jurisdictionConfig", {})
        except Exception:
            pass

    return {}


def _generate_new_case_prompt(
    case_overview: Dict[str, str],
    jurisdiction: Dict,
    focus: Optional[str] = None
) -> str:
    """
    Generate prompt for new case assessment.

    Examples:
        >>> prompt = _generate_new_case_prompt({}, {})
        >>> "Deep Legal Research" in prompt
        True
    """
    # Extract case summary if available
    case_summary = case_overview.get("case_summary", "")

    # Build jurisdiction context
    jur_text = jurisdiction.get("jurisdiction", "Federal")
    court_text = jurisdiction.get("court", "")

    prompt = f"""# Deep Legal Research: New Case Assessment

## My Situation

{case_summary if case_summary else "[Please describe your situation: what happened, who's involved, what harm occurred]"}

## Jurisdiction
- **Primary**: {jur_text}
- **Court**: {court_text if court_text else "[To be determined]"}

## What I Need from Deep Research

### 1. Legal Claims Analysis
- What legal claims/causes of action apply to my situation?
- Elements I need to prove for each potential claim
- Burden of proof and evidentiary requirements
- Likelihood of success based on similar cases in {jur_text}

### 2. Damages Assessment
- Types of damages available (compensatory, punitive, statutory, treble)
- How courts in {jur_text} calculate damages in similar cases
- Evidence and documentation needed to support damage claims
- Potential damage ranges based on comparable cases

### 3. Venue & Jurisdiction Analysis
- Proper court (federal vs. state, which district)
- Personal jurisdiction and minimum contacts requirements
- Venue considerations and forum selection strategy
- Any mandatory arbitration or ADR provisions to consider

### 4. Defense Strategy Prediction
- Most likely defenses the defendant will raise
- How to proactively counter those defenses in the complaint
- Procedural challenges to expect (12(b)(6) motion, arbitration, etc.)
- Affirmative defenses and how to negate them

### 5. Procedural Requirements
- Statute of limitations and filing deadlines
- Pre-litigation requirements (demand letters, statutory notice, exhaustion)
- Service of process requirements and challenges
- Initial disclosures and early case management considerations

### 6. Strategic Considerations
- Settlement leverage points based on case strength
- Cost-benefit analysis (litigation costs vs. potential recovery)
- Risks and challenges specific to this type of case
- Alternative dispute resolution options and likelihood of success

### 7. Case Timeline & Cost Estimate
- Typical timeline from filing to resolution for this type of case
- Discovery scope and duration estimates
- Estimated litigation costs (if proceeding pro se with AI assistance)
- Key milestones and decision points

{f'''
### 8. Focused Deep Dive: {focus}
Please provide extra depth on: {focus}
''' if focus else ''}

## Output Format

Please provide a comprehensive markdown document with:

1. **Executive Summary** (1-2 pages)
   - Case strength rating (Strong/Moderate/Weak)
   - Recommended claims with brief rationale
   - Key risks and challenges
   - Go/No-Go recommendation

2. **Detailed Analysis** for each section above
   - Relevant case law with citations and holdings
   - Statutory framework with specific code sections
   - Practical considerations and pitfalls
   - Strategic recommendations

3. **Action Plan**
   - Immediate next steps
   - Research still needed
   - Documents to gather
   - Timeline for filing

4. **Appendix**
   - Key cases with full citations and relevant quotes
   - Statutory text
   - Form pleading considerations
   - Pro se resources and considerations

## Special Instructions

- Focus on {jur_text} law, but include controlling federal precedent where applicable
- Include recent cases (last 5 years) showing current trends
- Flag any circuit splits or unsettled legal questions
- Be realistic about pro se challenges and considerations
- Provide specific pin cites for quoted material
- Highlight any procedural traps or common mistakes to avoid

---

**Note**: This research will inform whether to proceed with litigation and how to structure the case. Please be thorough and candid about both strengths and weaknesses.
"""

    return prompt


def _generate_active_litigation_prompt(
    stage: str,
    case_overview: Dict[str, str],
    gameplan: Optional[str],
    filed_docs: List[str],
    research_done: List[str],
    jurisdiction: Dict,
    focus: Optional[str] = None
) -> str:
    """
    Generate prompt for active litigation research needs.

    Examples:
        >>> prompt = _generate_active_litigation_prompt('discovery', {}, None, [], [], {})
        >>> "Deep Legal Research" in prompt
        True
    """
    # Extract relevant context
    case_summary = case_overview.get("case_summary", "")

    # Build jurisdiction context
    jur_text = jurisdiction.get("jurisdiction", "Federal")
    court_text = jurisdiction.get("court", "")
    circuit_text = jurisdiction.get("circuit", "")

    # Stage-specific focus
    stage_guidance = {
        "filed": "Initial case strategy and discovery planning",
        "discovery": "Discovery strategy, compelling production, and evidence analysis",
        "motions": "Motion practice, legal standards, and persuasive arguments",
        "trial_prep": "Trial strategy, evidence admissibility, and jury instructions"
    }

    stage_focus = stage_guidance.get(stage, "General litigation strategy")

    # Extract next steps from gameplan
    next_steps = "[See GAMEPLAN.md for current action items]"
    if gameplan:
        # Try to extract immediate next steps section
        if "Immediate Next Steps" in gameplan or "Next Actions" in gameplan:
            lines = gameplan.split("\n")
            in_section = False
            steps = []
            for line in lines:
                if "Next Steps" in line or "Next Actions" in line:
                    in_section = True
                elif line.startswith("#") and in_section:
                    break
                elif in_section and line.strip():
                    steps.append(line.strip())
            if steps:
                next_steps = "\n".join(steps)

    prompt = f"""# Deep Legal Research: {stage.replace('_', ' ').title()} Stage

## Case Context

**Case**: {case_overview.get("case_name", "[Case Name]")}
**Court**: {court_text if court_text else jur_text}
**Circuit**: {circuit_text if circuit_text else "[Applicable Circuit]"}
**Stage**: {stage.replace('_', ' ').title()}

### Case Summary
{case_summary if case_summary else "[Brief case summary]"}

### Documents Filed
{chr(10).join(f"- {doc}" for doc in filed_docs) if filed_docs else "- [No documents filed yet]"}

### Research Completed
{chr(10).join(f"- {topic}" for topic in research_done) if research_done else "- [No research completed yet]"}

## Current Focus: {stage_focus}

### Immediate Priorities
{next_steps}

## Research Objectives

{f'''
### Primary Focus: {focus}

Please provide comprehensive research on: {focus}

Include:
- Controlling case law from {circuit_text if circuit_text else jur_text}
- Applicable statutes and rules
- Procedural requirements and deadlines
- Strategic considerations
- Sample language and precedent

''' if focus else '''
### General Research Needs

Based on the current case stage, please research:

1. **Legal Standards**
   - Key legal standards applicable to our current stage
   - Burden of proof and evidentiary requirements
   - Recent trends in {jur_text} and {circuit_text if circuit_text else "federal"} courts

2. **Procedural Requirements**
   - Specific rule requirements (FRCP, local rules)
   - Timing and deadlines
   - Common procedural pitfalls to avoid

3. **Strategic Considerations**
   - Best practices for this stage
   - Common mistakes to avoid
   - Tactical advantages to leverage

4. **Opposition Analysis**
   - Likely arguments from opposing counsel
   - How to counter and distinguish their authorities
   - Weaknesses in our position and how to shore them up
'''}

## Jurisdiction Focus

**Controlling Authority** (in order of precedence):
{chr(10).join(f"- {auth}" for auth in jurisdiction.get("preferred_authority_order", ["U.S. Supreme Court", jur_text])) if jurisdiction else f"- {jur_text}"}

## Specific Questions

1. What are the key cases in {circuit_text or jur_text} on [primary issue]?
2. What procedural requirements must we meet at this stage?
3. What are the strongest arguments we can make?
4. What are the weaknesses in our position and how do we address them?
5. What evidence do we need to gather/preserve?
6. What are the strategic considerations for next steps?

{'''
## Additional Context from GAMEPLAN

''' + gameplan if gameplan else ''}

## Output Format

Please provide a comprehensive legal research memorandum with:

1. **Executive Summary**
   - Key findings
   - Recommended approach
   - Critical deadlines
   - Risk assessment

2. **Legal Analysis**
   - Controlling case law with full citations
   - Statutory framework
   - Procedural requirements
   - Standard of review

3. **Strategic Recommendations**
   - Strongest arguments
   - How to address weaknesses
   - Evidence needed
   - Tactical considerations

4. **Counter-Argument Analysis**
   - Likely opposing arguments
   - How to distinguish their cases
   - Affirmative counters

5. **Procedural Checklist**
   - Specific requirements
   - Deadlines
   - Filing requirements
   - Common mistakes to avoid

6. **Draft Language** (where applicable)
   - Sample motion/brief language
   - Key quotes from cases with pin cites
   - Statutory text

## Special Instructions

- Prioritize {circuit_text or jur_text} authority
- Include recent cases (especially last 3 years)
- Flag any circuit splits or evolving doctrine
- Be realistic about strengths and weaknesses
- Provide specific pin cites for all quoted material
- Include practical tips for pro se litigants where relevant

---

**Note**: This research will directly inform our next court filing or strategic decision. Please be thorough and include specific, actionable guidance.
"""

    return prompt


def _save_prompt(prompt: str, base_path: Path) -> Path:
    """
    Save generated prompt to file.

    Examples:
        >>> base = Path('.')
        >>> prompt_path = _save_prompt("test prompt", base)
        >>> prompt_path.exists()
        True
    """
    output_dir = base_path / ".wepublic_defender"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "deep_research_prompt.md"
    output_file.write_text(prompt, encoding="utf-8")

    return output_file


def generate_prompt(
    focus: Optional[str] = None,
    stage_override: Optional[str] = None
) -> Tuple[str, Path]:
    """
    Main function to generate deep research prompt.

    Args:
        focus: Optional specific topic to focus research on
        stage_override: Optional override for case stage detection

    Returns:
        Tuple of (prompt_text, saved_file_path)

    Examples:
        >>> prompt, path = generate_prompt()
        >>> isinstance(prompt, str)
        True
        >>> isinstance(path, Path)
        True
    """
    base_path = Path.cwd()

    # Detect or use override stage
    stage = stage_override if stage_override else _detect_case_stage(base_path)

    # Gather context
    gameplan = _read_gameplan(base_path)
    case_overview = _read_case_overview(base_path)
    filed_docs = _get_filed_documents(base_path)
    research_done = _get_research_done(base_path)
    jurisdiction = _load_jurisdiction_config(base_path)

    # Generate appropriate prompt
    if stage in ["new_case", "planning"]:
        prompt = _generate_new_case_prompt(case_overview, jurisdiction, focus)
    else:
        prompt = _generate_active_litigation_prompt(
            stage, case_overview, gameplan, filed_docs,
            research_done, jurisdiction, focus
        )

    # Save prompt
    saved_path = _save_prompt(prompt, base_path)

    return prompt, saved_path


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="wpd-deep-research-prompt",
        description="Generate prompt for Claude.ai Deep Research mode"
    )
    parser.add_argument(
        "--focus",
        help="Specific topic to focus research on (e.g., 'summary judgment standards')"
    )
    parser.add_argument(
        "--stage",
        choices=["new_case", "planning", "filed", "discovery", "motions", "trial_prep"],
        help="Override automatic stage detection"
    )

    args = parser.parse_args()

    try:
        print("=" * 70)
        print("DEEP RESEARCH PROMPT GENERATOR")
        print("=" * 70)
        print()

        # Generate prompt
        prompt, saved_path = generate_prompt(args.focus, args.stage)

        print(f"[OK] Prompt generated and saved to: {saved_path}")
        print()
        print("=" * 70)
        print("COPY THIS PROMPT TO CLAUDE.AI")
        print("=" * 70)
        print()
        print(prompt)
        print()
        print("=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print()
        print("1. Copy the entire prompt above")
        print("2. Open https://claude.ai")
        print("3. Start a new chat with Claude 3.7 Sonnet")
        print("4. Enable 'Deep Research' mode in the chat")
        print("5. Paste the prompt and send")
        print("6. Wait for comprehensive research (typically 5-10 minutes)")
        print("7. Copy the complete markdown results")
        print("8. Return to Claude Code and paste the results")
        print("9. I'll organize the research and suggest next actions")
        print()
        print("COST ESTIMATE: $2-8 depending on research depth and web searches")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

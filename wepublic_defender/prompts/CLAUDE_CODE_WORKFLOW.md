# Enhanced Claude Code + WePublicDefender Workflow

## Overview

Claude Code acts as the PRIMARY legal analyst, using enhanced prompts to do the work itself FIRST, then validates with external LLMs for adversarial redundancy.

## Three-Stage Workflow for Each Agent

### Stage 1: Claude Code Does the Work (FREE)
1. Claude Code calls agent in `--mode guidance` to get the enhanced prompt
2. Claude Code executes the prompt instructions thoroughly
3. Claude Code saves its results to `.wepublic_defender/reviews/[agent]_claude_code_[timestamp].json`

### Stage 2: External LLM Validation (COSTS MONEY)
1. Claude Code calls agent in `--mode external-llm` to get second opinions
2. External LLMs (GPT-5, Grok-4) provide their analysis
3. Results saved to `.wepublic_defender/reviews/[agent]_[model]_[timestamp].json`

### Stage 3: Synthesis and Decision
1. Claude Code reads ALL results (its own + external LLMs)
2. Claude Code compares findings:
   - Where do all agree? (high confidence)
   - Where do they disagree? (needs investigation)
   - What did Claude miss that LLMs caught?
   - What did Claude find that LLMs missed?
3. Claude Code presents synthesized findings to user
4. Claude Code recommends next actions based on consensus

## Example Workflow: Self Review

```bash
# Step 1: Claude gets the guidance prompt
wpd-run-agent --agent self_review --file draft.md --mode guidance

# Step 2: Claude executes the prompt (reviews document thoroughly)
# Claude identifies:
# - 3 critical issues (missing jurisdiction, wrong statute, no damages)
# - 5 major issues (weak causation, missing citations, etc.)
# - 8 minor issues (formatting, typos, etc.)

# Step 3: Claude saves its results
# Saves to: .wepublic_defender/reviews/self_review_claude_code_20251016_143022.json
{
  "agent": "self_review",
  "model": "claude_code",
  "timestamp": "2025-10-16T14:30:22",
  "critical_issues": [...],
  "major_issues": [...],
  "minor_issues": [...],
  "ready_to_file": false,
  "overall_assessment": "..."
}

# Step 4: Claude calls external LLMs for validation
wpd-run-agent --agent self_review --file draft.md --mode external-llm

# Step 5: External LLMs save their results
# GPT-5: .wepublic_defender/reviews/self_review_gpt5_20251016_143045.json
# Grok-4: .wepublic_defender/reviews/self_review_grok4_20251016_143050.json

# Step 6: Claude reads and compares all three reviews
- Claude found 3 critical, GPT-5 found 2, Grok-4 found 4
- All agree on: missing jurisdiction (critical)
- Claude unique finding: wrong statute citation
- GPT-5 unique finding: potential arbitration issue
- Grok-4 unique finding: standing problem

# Step 7: Claude synthesizes and reports
"I've completed review with external validation:
- CONSENSUS CRITICAL: Missing jurisdiction statement (all 3 reviewers)
- DISPUTED CRITICAL: Standing issue (only Grok-4 flagged)
- MY UNIQUE FINDING: Wrong statute cited in Count II
- RECOMMENDED ACTION: Fix jurisdiction first, then investigate standing"
```

## Benefits of This Workflow

1. **Cost Efficiency**: Claude does main work for free, LLMs only validate
2. **Quality**: Multiple perspectives catch different issues
3. **Transparency**: All findings saved and comparable
4. **Learning**: Claude can see what it missed and improve
5. **Confidence**: Consensus findings have high confidence
6. **Speed**: Claude works immediately, LLMs run in parallel after

## Implementation Pattern for Claude Code

### Saving Claude's Results

```python
import json
from datetime import datetime
from pathlib import Path

def save_claude_review(agent_type: str, results: dict):
    """Save Claude Code's review results in standard format."""

    # Ensure reviews directory exists
    review_dir = Path(".wepublic_defender/reviews")
    review_dir.mkdir(parents=True, exist_ok=True)

    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_type}_claude_code_{timestamp}.json"
    filepath = review_dir / filename

    # Add metadata
    results["agent"] = agent_type
    results["model"] = "claude_code"
    results["timestamp"] = datetime.now().isoformat()

    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    return filepath

# Example usage after Claude reviews:
my_review = {
    "critical_issues": ["Missing jurisdiction", "No standing alleged"],
    "major_issues": ["Weak causation", "Missing damages calculation"],
    "minor_issues": ["Typos in paragraph 14", "Formatting inconsistent"],
    "ready_to_file": False,
    "overall_assessment": "Document needs significant revision before filing"
}

save_claude_review("self_review", my_review)
```

### Reading and Comparing All Results

```python
def compare_all_reviews(agent_type: str) -> dict:
    """Read and compare all reviews for an agent."""

    review_dir = Path(".wepublic_defender/reviews")
    pattern = f"{agent_type}_*.json"

    reviews = {}
    for file in review_dir.glob(pattern):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            model = data.get("model", "unknown")
            reviews[model] = data

    # Compare findings
    comparison = {
        "all_models": list(reviews.keys()),
        "consensus_critical": [],
        "disputed_critical": [],
        "unique_findings": {},
    }

    # Find consensus and disputes
    all_critical = {}
    for model, review in reviews.items():
        for issue in review.get("critical_issues", []):
            if issue not in all_critical:
                all_critical[issue] = []
            all_critical[issue].append(model)

    for issue, models in all_critical.items():
        if len(models) == len(reviews):
            comparison["consensus_critical"].append(issue)
        else:
            comparison["disputed_critical"].append({
                "issue": issue,
                "flagged_by": models
            })

    return comparison
```

## Agent-Specific Workflows

### Self Review
1. Claude reviews for legal sufficiency
2. External LLMs validate
3. Focus on: elements, jurisdiction, damages, procedure

### Citation Verify
1. Claude researches each citation
2. External LLMs with web search verify
3. Focus on: good law, supports position, pin cites

### Opposing Counsel
1. Claude attacks document aggressively
2. External LLMs find additional weaknesses
3. Focus on: dismissal risks, weak arguments, missing elements

### Strategy
1. Claude develops comprehensive strategy
2. External LLMs suggest alternatives
3. Focus on: next actions, deadlines, risks, opportunities

### Research
1. Claude researches with web search
2. External LLMs find additional authorities
3. Focus on: relevant cases, statutes, arguments

### Drafter
1. Claude drafts document/section
2. External LLMs suggest improvements
3. Focus on: clarity, persuasion, completeness

### Final Review
1. Claude does pre-filing check
2. External LLMs confirm ready
3. Focus on: compliance, formatting, completeness

## Cost Management

- Stage 1 (Claude): FREE - unlimited analysis
- Stage 2 (External): $ - use selectively
- Stage 3 (Synthesis): FREE - Claude compares

## When to Skip External Validation

- Minor documents
- Time-critical situations
- Budget constraints
- High confidence in Claude's analysis
- User explicitly says skip

## When External Validation is CRITICAL

- Final filing documents
- High-stakes motions
- Novel legal arguments
- Significant damage claims
- Anything with dismissal risk

## Summary

This workflow maximizes Claude Code's capabilities while maintaining quality through selective external validation. Claude does the heavy lifting, external LLMs provide safety net, and everything is tracked for review and learning.
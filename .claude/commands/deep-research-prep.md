# /deep-research-prep Command

Generate a comprehensive prompt for Claude.ai Deep Research mode based on current case status.

## What This Does

Analyzes your case's current state and creates a specialized research prompt that you can copy to Claude.ai's Deep Research feature. This is more efficient than doing extensive web searches in Claude Code - Deep Research mode is optimized for heavy research tasks.

## When to Use This

- **New cases**: Need to assess case type, damages potential, venue, likelihood of success
- **Active litigation**: Need deep research on specific legal issues, standards, or strategies
- **Before major filings**: Need comprehensive research for motions, briefs, or responses
- **Anytime**: You need more web research than Claude Code should handle

## Usage

```
/deep-research-prep
/deep-research-prep --focus "summary judgment standards for breach of contract"
/deep-research-prep --stage new_case
```

## Process

1. **Analyze Case State**
   - Detect current stage (new case, discovery, motions, etc.)
   - Read GAMEPLAN.md and case overview
   - Identify what's been filed and researched
   - Determine research gaps

2. **Generate Tailored Prompt**
   - New cases: Assessment of claims, damages, venue, strategy
   - Active litigation: Focused research on current needs
   - Include jurisdiction context and specific questions
   - Format for easy copy-paste

3. **Save and Display**
   - Save to `.wepublic_defender/deep_research_prompt.md`
   - Display full prompt for copying
   - Provide instructions for next steps

## Example Output

```
============================================================
DEEP RESEARCH PROMPT GENERATED
============================================================

✓ Saved to: .wepublic_defender/deep_research_prompt.md

============================================================
COPY THIS TO CLAUDE.AI
============================================================

# Deep Legal Research: New Case Assessment

## My Situation

[Your case details from 01_CASE_OVERVIEW/]

## What I Need from Deep Research

### 1. Legal Claims Analysis
- What legal claims apply to my situation?
- Elements I need to prove
- Likelihood of success in South Carolina

[... detailed research objectives ...]

============================================================
NEXT STEPS
============================================================

1. Copy the entire prompt above
2. Open https://claude.ai
3. Start new chat with Claude 3.7 Sonnet
4. Enable 'Deep Research' mode
5. Paste the prompt
6. Wait for research (5-10 minutes)
7. Copy results
8. Paste back here for me to organize

Cost estimate: $2-8 depending on depth
```

## What Happens Next

After you paste the research results back:
1. I'll save them to `06_RESEARCH/[topic].md`
2. Update GAMEPLAN.md with key findings
3. Identify next actions based on research
4. Suggest follow-up research if needed

## Tips

- **Be specific with --focus**: Instead of "damages", use "punitive damages standards for fraud in South Carolina"
- **Stage matters**: New case prompts focus on assessment, active litigation prompts focus on current needs
- **Review before sending**: Check if the prompt includes all your case context
- **Save the results**: When you paste research back, I'll organize it properly

## Implementation

Run the Python CLI command to generate the prompt:

```python
import subprocess
result = subprocess.run(
    ["wpd-deep-research-prompt"] +
    (["--focus", focus] if focus else []) +
    (["--stage", stage] if stage else []),
    capture_output=True,
    text=True
)
print(result.stdout)
```

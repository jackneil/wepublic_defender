# First Case Initialization Workflow

**TRIGGER**: `.wepublic_defender/case_initialized.json` does NOT exist in current working directory

This is the first time Claude Code is processing this legal case directory. Follow this checklist to set up properly.

## ⚠️ CRITICAL: Windows File Editing (READ FIRST)

**If on Windows (`<env>` shows `win32`)**, you MUST use backslashes `\` in Edit/MultiEdit file paths:

**❌ WRONG - Will cause errors:**
```
Edit(file_path: "C:/github/file.py", ...)
```

**✅ CORRECT - Always works:**
```
Edit(file_path: "C:\\github\\file.py", ...)
```

**Bash commands still use forward slashes `/`** - this is ONLY for Edit/MultiEdit tool paths.

**This is a known bug in Claude Code** - Edit tool requires backslashes on Windows even though everything else uses forward slashes.

## 1. Verify Environment Setup

Run environment check to ensure Python, packages, and API keys are configured:

```bash
<python_path> -m wepublic_defender.cli.check_env
```

**If environment issues detected:**
- Install missing packages
- Help user create `.env` with API keys
- Verify wepublic_defender package is installed
- DO NOT proceed until environment is clean

## 2. Verify Directory Structure

Check if standard case directories exist:
- `00_NEW_DOCUMENTS_INBOX/`
- `01_CASE_OVERVIEW/`
- `02_PLEADINGS/`
- ... (all standard dirs)

**If directories missing:**
- This case hasn't been initialized with `wpd-init-case`
- Offer to run: `<python_path> -m wepublic_defender.cli.init_case`
- Wait for completion, then continue

## 3. Check Inbox for Files

Look in `00_NEW_DOCUMENTS_INBOX/` for files:

**If files present:**
- List them to user
- Offer: "I see X files in the inbox. Would you like me to organize them with `/organize`?"
- If user agrees, run `/organize` to categorize and move files

**If inbox empty:**
- Note it and continue

## 4. Assess Case Status

Read existing case files to understand current state:

**Read these files:**
1. `01_CASE_OVERVIEW/case_summary.md` (if exists)
2. `01_CASE_OVERVIEW/timeline.md` (if exists)
3. `01_CASE_OVERVIEW/parties.md` (if exists)
4. `GAMEPLAN.md`

**Categorize case status:**
- **New case, no research done**: GAMEPLAN.md is empty template, minimal/no overview docs
- **Research in progress**: Some research in `06_RESEARCH/`, GAMEPLAN partially filled
- **Active litigation**: Pleadings in `02_PLEADINGS/`, GAMEPLAN has strategy
- **Existing case imported**: Files scattered, needs organization

## 5. Offer Initial Actions Based on Status

### If New Case (No Research Done):

Explain to user:

> "This appears to be a new case. To help you build a strong foundation, I recommend starting with deep research to assess:
> - Case viability and legal claims
> - Applicable statutes and case law
> - Damages assessment
> - Venue and jurisdiction analysis
> - Strategic considerations
>
> Would you like me to generate a comprehensive deep research prompt? I'll create a prompt you can paste into Claude.ai's Deep Research mode. It takes 5-10 minutes but gives you a much more thorough analysis than quick web searches.
>
> After the research completes, I'll use it to generate your strategic GAMEPLAN.md."

**If user agrees:**
1. Run `/deep-research-prep` to generate comprehensive prompt
2. User copies prompt to Claude.ai (https://claude.ai)
3. User enables Deep Research mode and submits
4. Wait 5-10 minutes for Claude.ai to complete research
5. User pastes results back
6. Save results to `06_RESEARCH/deep_research_initial_assessment.md`
7. **Generate strategic GAMEPLAN.md from research** (see step 6 below)

**If user declines:**
- Note it: "Understood. Let me know when you're ready for research or if you'd like help with something else."

### If Research in Progress:

- Summarize what research exists
- Check GAMEPLAN.md for next actions
- Offer to help with next steps

### If Active Litigation:

- Summarize current pleadings and status
- Check GAMEPLAN.md for upcoming deadlines
- Offer to help with next filing or response

### If Existing Case Imported:

- Offer `/organize` to clean up structure
- Suggest reviewing and updating GAMEPLAN.md

## 6. Generate GAMEPLAN.md (After Deep Research)

**IMPORTANT**: After deep research completes, generate a REAL strategic gameplan, not just the empty template.

Use the deep research findings to populate:

```markdown
# Case Strategy and Game Plan

## Case Overview
[Summarize the case from research: parties, claims, key facts]

## Legal Assessment
### Strengths
- [List strong legal arguments and evidence from research]

### Weaknesses
- [List potential problems and opposing arguments from research]

### Key Legal Issues
- [List main legal questions that will determine outcome]

## Strategic Approach
[Based on research, what's the overall strategy? Aggressive offense? Settle early? Motion to dismiss?]

## Immediate Next Steps
1. [Action item from research - e.g., "Draft complaint asserting claims X, Y, Z"]
2. [Action item - e.g., "Gather evidence for element X of claim Y"]
3. [Action item - e.g., "Research affirmative defenses opponent might raise"]

## Key Deadlines
- [Date]: [Statute of limitations / filing deadline / response deadline]

## Evidence Needed
- [List evidence we need to gather based on claims]

## Anticipated Opposing Arguments
[From research, what will opponent argue? How do we counter?]

## Settlement Considerations
[What's the case worth? What's realistic settlement range? When to consider settling?]

## Risks and Concerns
- [List risks from research: bad case law, missing evidence, procedural issues, etc.]

## Research Notes
[Link to deep research file: see 06_RESEARCH/deep_research_initial_assessment.md]
```

Save to `GAMEPLAN.md` and tell user:
> "I've generated your strategic GAMEPLAN.md based on the research. This will guide all future work on this case. Review it and let me know if you want to adjust the strategy."

## 7. Mark Case as Initialized

Create `.wepublic_defender/case_initialized.json`:

```json
{
  "initialized_date": "2025-10-13",
  "initialized_by": "claude_code",
  "case_status": "new|research|active|imported",
  "initial_deep_research_completed": true|false,
  "gameplan_generated": true|false,
  "python_exe": "/path/to/python.exe",
  "conda_env": "wepublic_defender",
  "repo_path": "/path/to/wepublic_defender"
}
```

This file prevents this workflow from running again on future sessions.

## 8. Transition to Session Start Workflow

Tell user:
> "Case initialization complete. Future sessions will use the regular workflow. What would you like to work on?"

Then follow `.claude/workflows/session_start_checklist.md` for subsequent interactions.

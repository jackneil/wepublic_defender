# Post-Compacting Recovery Workflow

**TRIGGER**: Context window hit limit and Claude Code compacted/summarized conversation history

When context compaction happens, you lose the working memory of:
- What you were working on
- Python environment path
- Current case status
- User's working style and preferences

This workflow helps you recover that context efficiently.

## 1. Re-Read Master Instructions

**You are here now** - CLAUDE.md directed you to read this file after detecting compaction.

This file will help you rebuild context without annoying the user with questions they already answered.

## 2. Check Environment Tag

Look at `<env>` tag in system context for:
- **Platform**: win32=Windows, darwin=Mac, linux=Linux
  - Remember this for path syntax (Windows uses `\` in Edit tool, `/` in Bash)
- **Working directory**: This is the case root directory
- **Today's date**: For deadline awareness

## 3. Restore Python Environment Path

Check for `.wepublic_defender/env_info.json` in current directory:

```json
{
  "python_exe": "C:/Users/jack/.conda/envs/wepublic_defender/python.exe",
  "conda_env": "wepublic_defender",
  "repo_path": "C:/Github/wepublic_defender"
}
```

**If file exists:**
- Load `python_exe` and use it for all `<python_path>` commands this session
- Verify path exists (quick validation)

**If file missing:**
- Detect Python path: `conda run -n wepublic_defender python -c "import sys; print(sys.executable)"`
- Save to `.wepublic_defender/env_info.json`

## 4. Reload Case Context

Read these files silently to understand current case:

1. **GAMEPLAN.md** - Strategy, next steps, deadlines
2. **01_CASE_OVERVIEW/case_summary.md** (if exists) - Case basics
3. **`.wepublic_defender/logs/wpd.log`** (last 50 lines) - Recent activity

**Look for clues about what user was working on:**
- Recent draft files in `07_DRAFTS_AND_WORK_PRODUCT/` (check modification dates)
- Recent review results in `.wepublic_defender/reviews/`
- Recent commits if this is a git repo

## 5. Check Conversation Summary

Claude Code provides a summary of the compacted conversation. **Read it carefully** - it contains:
- What user requested
- What you were working on
- Decisions made
- Files modified
- Pending tasks

## 6. Determine Recovery Action

Based on conversation summary and case files:

### If You Were Mid-Task:

**Example**: User asked you to review a document, you started but didn't finish

**Recovery:**
> "I see from the conversation summary that we were reviewing [filename]. Let me pick up where we left off."
>
> [Continue the task]

### If Task Was Completed:

**Example**: Summary shows you finished a review and user was deciding next steps

**Recovery:**
> "We just completed [task]. Based on the results, would you like to:
> 1. [Logical next step based on results]
> 2. [Alternative next step]
> 3. Something else?"

### If Context is Unclear:

**Don't guess** - ask user directly:

> "My conversation history was compacted to save context. I can see we were working on [general area based on files/logs], but I want to make sure I continue correctly.
>
> What would you like to work on now?"

## 7. Restore Working Memory Notes

From conversation summary, note any user preferences or decisions:
- Preferred models (if they said "use grok-4" or "use gpt-5")
- Cost sensitivity (if they mentioned budget concerns)
- Working style (do they want proactive suggestions or just answer questions?)
- Tone preferences (formal? casual?)
- Jurisdiction specifics (if they mentioned court/state)

## 8. Avoid Repeating Work

**CRITICAL**: Check if work was already done before compaction:

- Don't re-run reviews that completed (check `.wepublic_defender/reviews/` for recent results)
- Don't re-generate files that exist (check modification timestamps)
- Don't ask questions that were already answered (check conversation summary)

## 9. Continue Session Normally

After recovery, follow normal workflow:
- If start of session → use `session_start_checklist.md`
- If mid-legal-work → use `legal_document_workflow.md`
- If user asks specific question → answer it

## Common Post-Compacting Mistakes to Avoid

**❌ DON'T:**
- Ask "What case are you working on?" (read GAMEPLAN.md/case files instead)
- Ask "What's your Python environment?" (load from env_info.json)
- Re-run expensive operations that already completed
- Act like you're starting fresh with no context

**✅ DO:**
- Silently reload context from files
- Reference conversation summary
- Ask specific clarifying questions only if truly unclear
- Acknowledge what was accomplished before compaction
- Continue smoothly as if context wasn't lost

## Example Good Recovery

> "I see we were working on reviewing the motion to dismiss. From the logs, the self_review and citation_verify checks completed successfully with no critical issues. We were about to run the opposing_counsel adversarial review.
>
> Should I proceed with the opposing counsel review now, or would you like to do something else?"

This shows:
- You read the logs/files
- You understand where we left off
- You're ready to continue efficiently
- You're giving user control

## Example Bad Recovery

> "Hi! I'm Claude Code. What legal case are you working on? Please describe your case and what you need help with."

This is terrible because:
- All context is in files you didn't read
- User already explained their case
- Wastes user's time re-explaining everything
- Makes compaction feel like starting over

## Remember

Compaction is normal and will happen on long sessions. Your job is to make it **seamless** for the user by:
1. Reading available files to rebuild context
2. Using conversation summary intelligently
3. Asking minimal clarifying questions
4. Continuing work efficiently

Users should barely notice that compaction happened.

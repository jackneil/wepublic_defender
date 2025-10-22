#!/bin/bash
# SessionStart hook: Auto-run session checklist when Claude Code opens
#
# This hook fires when:
# - User opens Claude Code (source: "startup")
# - Session resumes after compacting (source: "resume")
# - Session cleared (source: "clear")
#
# Payload provides: source, session_id, parent_session_id (if forked)

# Output instructions to stderr (exit code 2 shows to user without blocking)
cat >&2 <<'EOF'
═══════════════════════════════════════════════════════════════════════════════
                    !!! MANDATORY SESSION START - EXECUTE NOW !!!
═══════════════════════════════════════════════════════════════════════════════

**CRITICAL: You MUST run session start checklist BEFORE responding to user**

**THIS IS NOT OPTIONAL. THIS IS NOT A SUGGESTION. DO THIS NOW.**

**THIS WORKS EVEN IN PLAN MODE** - Reading files is non-destructive and allowed!

---

## What to Do (Takes 30 seconds):

1. Read `.claude/SESSION_START_MANDATORY.md` for quick overview

2. Follow `.claude/workflows/session_start_checklist.md`:
   - Load context from session_notes.md, case_timeline.md, GAMEPLAN.md
   - Check 00_NEW_DOCUMENTS_INBOX/ for new files
   - Identify upcoming deadlines (next 7 days)
   - Detect case stage (PRE-FILING, DISCOVERY, MOTION PRACTICE, TRIAL PREP)
   - Present 6 numbered options tailored to detected stage

3. THEN respond to user with stage-appropriate options

---

## CRITICAL: File Editing on Windows

**MANDATORY: Always Use Backslashes (\) in file paths for Edit/MultiEdit tools**

WRONG - Will cause errors:
Edit(file_path: "D:/repos/file.tsx", ...)

CORRECT - Always works:
Edit(file_path: "D:\\repos\\file.tsx", ...)

Bash commands use forward slashes (/), but Edit tool requires backslashes on Windows.

---

**EXECUTE SESSION START CHECKLIST NOW - BEFORE RESPONDING TO USER'S MESSAGE**

═══════════════════════════════════════════════════════════════════════════════
EOF

# Exit with code 0 (success) so Claude Code shows the message
exit 0

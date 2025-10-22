#!/bin/bash
# PreCompact hook: Critical reminders before conversation compaction

cat >&2 <<'EOF'
===============================================================================
                    !!! PRE-COMPACT CHECKLIST - READ THIS !!!
===============================================================================

CRITICAL: Before compacting, preserve these things in your compact summary:

## 1. Windows Path Issues (ALWAYS INCLUDE THIS VERBATIM)

**MANDATORY: When using Edit/MultiEdit/Write tools on Windows:**
- file_path parameter MUST use BACKSLASHES: C:\\path\\to\\file.txt
- WRONG: "C:/path/to/file.txt" (will error)
- CORRECT: "C:\\path\\to\\file.txt" (works)
- Bash commands use forward slashes, Edit tools use backslashes
- This is the #1 issue that breaks after compacting - REMEMBER IT!

## 2. Case Context to Preserve

**Read these files NOW (before compact) and include key info:**

A. `.wepublic_defender/session_notes.md`
   - What work was completed this session
   - What was being worked on (if interrupted)
   - Recent user requests and context
   - Important findings or blockers

B. `.wepublic_defender/case_timeline.md`
   - Recent major events (last 3-5 entries)
   - What's been filed/received recently

C. `GAMEPLAN.md`
   - Upcoming deadlines (next 7-14 days)
   - Current strategic priorities
   - Next steps planned

D. Current Stage of Work
   - What document/task is active
   - What phase: drafting, revising, reviewing, researching, filing
   - What's blocking progress (if anything)
   - What user is waiting for

## 3. Compact Summary Should Include

**Session Progress:**
- What was accomplished (e.g., "Completed self-review of Motion to Dismiss, found 3 critical issues, fixed 2, still need to research jurisdiction issue")
- What tools/agents were run (e.g., "Ran citation_verify on 5 citations, all good law")
- File operations (e.g., "Organized 10 documents from inbox into evidence folders")

**User Context:**
- Last thing user asked for
- Decisions user made (e.g., "User chose to strengthen argument rather than remove it")
- User's tone/priorities (e.g., "User wants aggressive motion practice, prioritize strongest arguments")

**What's Next:**
- Immediate next step (e.g., "Need to run opposing_counsel agent after user reviews fixes")
- Pending tasks from session_notes.md
- Upcoming deadlines from GAMEPLAN.md

**Technical Context:**
- Python environment: Check .wepublic_defender/env_info.json for python path
- Case directory structure in place
- What agents/tools are available

## 4. After Compact Resumes

**First actions when session resumes:**
1. Verify you remember Windows path backslash requirement
2. Read session_notes.md to see what was being worked on
3. Check GAMEPLAN.md for deadlines
4. Ask user: "We were [last activity]. Would you like to continue or do something else?"

===============================================================================
                    NOW COMPACT WITH THIS CONTEXT IN MIND
===============================================================================
EOF

# Exit with code 2 to show message to user without blocking
exit 2

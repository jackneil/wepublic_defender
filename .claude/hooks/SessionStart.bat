@echo off
REM SessionStart hook: Auto-run session checklist when Claude Code opens
REM
REM This hook fires when:
REM - User opens Claude Code (source: "startup")
REM - Session resumes after compacting (source: "resume")
REM - Session cleared (source: "clear")
REM
REM Payload provides: source, session_id, parent_session_id (if forked)

REM Output instructions to stderr (exit code 2 shows to user without blocking)
(
echo ===============================================================================
echo                     !!! MANDATORY SESSION START - EXECUTE NOW !!!
echo ===============================================================================
echo.
echo **CRITICAL: You MUST run session start checklist BEFORE responding to user**
echo.
echo **THIS IS NOT OPTIONAL. THIS IS NOT A SUGGESTION. DO THIS NOW.**
echo.
echo **THIS WORKS EVEN IN PLAN MODE** - Reading files is non-destructive and allowed!
echo.
echo ---
echo.
echo ## What to Do ^(Takes 30 seconds^):
echo.
echo 1. Read `.claude/SESSION_START_MANDATORY.md` for quick overview
echo.
echo 2. Follow `.claude/workflows/session_start_checklist.md`:
echo    - Load context from session_notes.md, case_timeline.md, GAMEPLAN.md
echo    - Check 00_NEW_DOCUMENTS_INBOX/ for new files
echo    - Identify upcoming deadlines ^(next 7 days^)
echo    - Detect case stage ^(PRE-FILING, DISCOVERY, MOTION PRACTICE, TRIAL PREP^)
echo    - Present 6 numbered options tailored to detected stage
echo.
echo 3. THEN respond to user with stage-appropriate options
echo.
echo ---
echo.
echo ## CRITICAL: File Editing on Windows
echo.
echo **MANDATORY: Always Use Backslashes ^(\^) in file paths for Edit/MultiEdit tools**
echo.
echo WRONG - Will cause errors:
echo Edit^(file_path: "D:/repos/file.tsx", ...^)
echo.
echo CORRECT - Always works:
echo Edit^(file_path: "D:\\repos\\file.tsx", ...^)
echo.
echo Bash commands use forward slashes ^(/^), but Edit tool requires backslashes on Windows.
echo.
echo ---
echo.
echo **EXECUTE SESSION START CHECKLIST NOW - BEFORE RESPONDING TO USER'S MESSAGE**
echo.
echo ===============================================================================
) 1>&2

REM Exit with code 0 (success) so Claude Code shows the message
exit /b 0

@echo off
REM PreCompact hook: Critical reminders before conversation compaction

REM Output instructions to stderr (exit code 2 shows to user without blocking)
(
echo ===============================================================================
echo                     !!! PRE-COMPACT CHECKLIST - READ THIS !!!
echo ===============================================================================
echo.
echo CRITICAL: Before compacting, preserve these things in your compact summary:
echo.
echo ## 1. Windows Path Issues ^(ALWAYS INCLUDE THIS VERBATIM^)
echo.
echo **MANDATORY: When using Edit/MultiEdit/Write tools on Windows:**
echo - file_path parameter MUST use BACKSLASHES: C:\\path\\to\\file.txt
echo - WRONG: "C:/path/to/file.txt" ^(will error^)
echo - CORRECT: "C:\\path\\to\\file.txt" ^(works^)
echo - Bash commands use forward slashes, Edit tools use backslashes
echo - This is the #1 issue that breaks after compacting - REMEMBER IT!
echo.
echo ## 2. Case Context to Preserve
echo.
echo **Read these files NOW ^(before compact^) and include key info:**
echo.
echo A. `.wepublic_defender/session_notes.md`
echo    - What work was completed this session
echo    - What was being worked on ^(if interrupted^)
echo    - Recent user requests and context
echo    - Important findings or blockers
echo.
echo B. `.wepublic_defender/case_timeline.md`
echo    - Recent major events ^(last 3-5 entries^)
echo    - What's been filed/received recently
echo.
echo C. `GAMEPLAN.md`
echo    - Upcoming deadlines ^(next 7-14 days^)
echo    - Current strategic priorities
echo    - Next steps planned
echo.
echo D. Current Stage of Work
echo    - What document/task is active
echo    - What phase: drafting, revising, reviewing, researching, filing
echo    - What's blocking progress ^(if anything^)
echo    - What user is waiting for
echo.
echo ## 3. Compact Summary Should Include
echo.
echo **Session Progress:**
echo - What was accomplished ^(e.g., "Completed self-review of Motion to Dismiss, found 3 critical issues, fixed 2, still need to research jurisdiction issue"^)
echo - What tools/agents were run ^(e.g., "Ran citation_verify on 5 citations, all good law"^)
echo - File operations ^(e.g., "Organized 10 documents from inbox into evidence folders"^)
echo.
echo **User Context:**
echo - Last thing user asked for
echo - Decisions user made ^(e.g., "User chose to strengthen argument rather than remove it"^)
echo - User's tone/priorities ^(e.g., "User wants aggressive motion practice, prioritize strongest arguments"^)
echo.
echo **What's Next:**
echo - Immediate next step ^(e.g., "Need to run opposing_counsel agent after user reviews fixes"^)
echo - Pending tasks from session_notes.md
echo - Upcoming deadlines from GAMEPLAN.md
echo.
echo **Technical Context:**
echo - Python environment: Check .wepublic_defender/env_info.json for python path
echo - Case directory structure in place
echo - What agents/tools are available
echo.
echo ## 4. After Compact Resumes
echo.
echo **First actions when session resumes:**
echo 1. Verify you remember Windows path backslash requirement
echo 2. Read session_notes.md to see what was being worked on
echo 3. Check GAMEPLAN.md for deadlines
echo 4. Ask user: "We were [last activity]. Would you like to continue or do something else?"
echo.
echo ===============================================================================
echo                     NOW COMPACT WITH THIS CONTEXT IN MIND
echo ===============================================================================
) 1>&2

REM Exit with code 2 to show message to user without blocking
exit /b 2

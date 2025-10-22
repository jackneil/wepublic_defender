@echo off
REM UserPromptSubmit hook: Remind about Windows backslash requirement BEFORE processing user input
REM This hook fires before Claude processes each user message
REM WINDOWS ONLY - prevents Edit/MultiEdit path errors

REM Output reminder to stderr (exit code 2 shows to Claude without blocking user)
(
echo ===============================================================================
echo ## CRITICAL: File Editing on Windows
echo ===============================================================================
echo.
echo ### MANDATORY: Always Use Backslashes ^(\^) in file paths for Edit/MultiEdit
echo.
echo WRONG - Will cause errors:
echo   Edit^(file_path: "D:/repos/file.tsx", ...^)
echo.
echo CORRECT - Always works:
echo   Edit^(file_path: "D:\\repos\\file.tsx", ...^)
echo.
echo Bash commands use forward slashes ^(/^), but Edit tool requires backslashes on Windows.
echo.
echo ===============================================================================
) 1>&2

REM Exit with code 2 to show message to Claude without blocking
exit /b 2

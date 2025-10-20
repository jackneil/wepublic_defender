# Session Start Workflow

Execute the complete session start checklist to load case context and present options.

## Your Task

Follow `.claude/workflows/session_start_checklist.md` immediately:

1. **Load Context**
   - Read `.wepublic_defender/session_notes.md` for last session's work
   - Read `.wepublic_defender/case_timeline.md` for recent case events
   - Read `GAMEPLAN.md` for strategy and deadlines
   - Clear "Currently Working On" in session_notes.md

2. **Check Inbox**
   - List files in `00_NEW_DOCUMENTS_INBOX/`
   - If files exist, offer to organize with `/organize`

3. **Identify Upcoming Deadlines**
   - Extract deadlines from GAMEPLAN "Key Deadlines" section
   - Flag any deadlines within next 7 days

4. **Detect Case Stage**
   - PRE-FILING: No 02_PLEADINGS/01_Complaint/ folder exists
   - DISCOVERY: 03_DISCOVERY/ folder has recent files (last 60 days)
   - MOTION PRACTICE: 02_PLEADINGS/03_Motions/ has recent activity (last 45 days)
   - TRIAL PREP: case_timeline mentions "trial scheduled"
   - GENERAL: Stage unclear or none of above

5. **Present Stage-Appropriate Multiple Choice Questions**
   - Show exactly 6 numbered options
   - Tailor options to detected case stage
   - Option 6 always: "Something else (tell me what)"

Execute the full checklist now and present the appropriate multiple choice questions.

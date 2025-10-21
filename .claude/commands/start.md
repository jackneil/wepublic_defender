# Session Start Workflow

**Manual trigger for session start checklist.**

Use this command when:
- Session start hook didn't fire automatically
- You want to reload context after long session
- Case context feels stale and you want fresh perspective
- You just want Claude to tell you what to work on

---

## Your Task

Follow `.claude/workflows/session_start_checklist.md` immediately:

1. **Load Context** (silently - don't output full contents)
   - Read `.wepublic_defender/session_notes.md` for last session's work
   - Read `.wepublic_defender/case_timeline.md` for recent case events
   - Read `GAMEPLAN.md` for strategy and deadlines
   - Update "Currently Working On" to "[Nothing in progress - ready for next task]"

2. **Check Inbox**
   - List files in `00_NEW_DOCUMENTS_INBOX/`
   - If files exist, mention count and offer `/organize`
   - If empty, don't mention it

3. **Identify Upcoming Deadlines**
   - Extract deadlines from GAMEPLAN "Key Deadlines" section
   - Flag any deadlines within next 7 days with warning
   - If no urgent deadlines, note it internally

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
   - Make options actionable and relevant to current stage

---

## This Command is Your Backup

If the SessionStart hook doesn't fire or you forget to run the checklist, type `/start` to manually trigger it.

**Execute the full checklist now and present the appropriate multiple choice questions.**

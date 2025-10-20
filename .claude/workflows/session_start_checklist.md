# Session Start Checklist

**TRIGGER**: Every time a new Claude Code session starts (after first case init is complete)

This checklist helps you quickly understand the current case status and offer relevant next actions.

---

## CRITICAL: File Editing on Windows

### ⚠️ MANDATORY: Always Use Backslashes on Windows for File Paths

**When using Edit or MultiEdit tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).**

#### ❌ WRONG - Will cause errors:
```
Edit(file_path: "D:/repos/project/file.tsx", ...)
MultiEdit(file_path: "D:/repos/project/file.tsx", ...)
```

#### ✅ CORRECT - Always works:
```
Edit(file_path: "D:\\repos\\project\\file.tsx", ...)
MultiEdit(file_path: "D:\\repos\\project\\file.tsx", ...)
```

**This is a known bug in Claude Code** - Edit/MultiEdit require backslashes on Windows even though Bash commands use forward slashes.

---

## 1. Quick Context Load

Read these files to understand current state (read silently, don't output full contents):

1. **`.wepublic_defender/session_notes.md`** - Last session's work and current status
2. **`.wepublic_defender/case_timeline.md`** - Recent case events and document status
3. **GAMEPLAN.md** - Current strategy, next steps, deadlines
4. **01_CASE_OVERVIEW/case_summary.md** (if exists) - Case basics
5. Check for `00_NEW_DOCUMENTS_INBOX/` contents - New files to organize?

**IMPORTANT**: Update `session_notes.md` at the start of session:
- Clear "Currently Working On" section (set to "[Nothing in progress - ready for next task]")
- Keep "Completed This Session" from last session for continuity
- Add new date section when you complete first task of new session

## 2. Check for New Files in Inbox

List files in `00_NEW_DOCUMENTS_INBOX/`:

**If files present:**
> "I see X files in the inbox:
> - [list filenames]
>
> Would you like me to organize them with `/organize`?"

**If inbox empty:**
- Note it internally, don't mention it unless asked

## 3. Identify Upcoming Deadlines

From GAMEPLAN.md "Key Deadlines" section:

**If deadline within 7 days:**
> "⚠️ You have a deadline coming up:
> - [Date]: [Deadline description]
>
> Current status: [check if related work exists in drafts]
>
> Would you like to work on this?"

**If no urgent deadlines:**
- Note it internally, continue

## 4. Review Immediate Next Steps

From GAMEPLAN.md "Immediate Next Steps" section:

**If action items exist:**
> "According to your GAMEPLAN, the next steps are:
> 1. [Action item]
> 2. [Action item]
> 3. [Action item]
>
> What would you like to work on?"

**If next steps section is empty/vague:**
> "Your GAMEPLAN doesn't have specific next steps. Would you like me to analyze the current case status and suggest a strategy?"
>
> (If user agrees, run `/strategy` or offer deep research if case is new)

## 5. Detect Case Stage and Present Options

**IMPORTANT**: Intelligently detect where user is in case lifecycle and present stage-appropriate multiple choice questions.

### Stage Detection Logic

Check these indicators to determine case stage (check in order, first match wins):

#### PRE-FILING Indicators:
- No `02_PLEADINGS/01_Complaint/` folder exists OR folder is empty
- `04_EVIDENCE/` has files but no complaint filed
- `case_timeline.md` shows investigation/evidence gathering phase
- GAMEPLAN mentions "investigating claim" or "assess viability"

#### DISCOVERY Indicators:
- `03_DISCOVERY/` folder exists with files from last 60 days
- `case_timeline.md` shows discovery deadlines or discovery exchanges
- Pending discovery requests/responses in `03_DISCOVERY/`
- GAMEPLAN mentions "discovery" or "interrogatories" or "depositions"

#### MOTION PRACTICE Indicators:
- `02_PLEADINGS/03_Motions/` has files modified within last 45 days
- `case_timeline.md` shows motion deadlines or motion hearings
- Opposition briefs exist in `07_DRAFTS_AND_WORK_PRODUCT/`
- GAMEPLAN mentions specific motions (dismiss, summary judgment, compel, etc.)

#### TRIAL PREP Indicators:
- `case_timeline.md` explicitly mentions "trial scheduled" or "trial date"
- `08_REFERENCE/` contains trial exhibits or witness lists
- Witness preparation documents in `07_DRAFTS_AND_WORK_PRODUCT/`
- GAMEPLAN mentions "trial preparation" or "jury instructions"

### Present Stage-Appropriate Questions

**Format**: Always present exactly 6 numbered options, with option 6 being "Something else (tell me what)"

#### PRE-FILING Stage Questions

When detected:
```
I see you're investigating a potential case. What would you like to work on?

1. Organize evidence from inbox
2. Research case viability (deep research)
3. Calculate potential damages
4. Check statute of limitations
5. Identify potential claims
6. Something else (tell me what)

Choose 1-6:
```

**Action mapping:**
- 1 → Run `/organize` command
- 2 → Run `/deep-research-prep` or `/strategy`
- 3 → Help calculate damages from evidence
- 4 → Research statute of limitations for jurisdiction
- 5 → `/strategy` focused on potential claims
- 6 → Ask user to specify

#### DISCOVERY Stage Questions

When detected (check for urgent deadlines first):
```
You're in active discovery. What's your priority?

1. Respond to pending discovery requests (deadline: [DATE if exists])
2. Draft new interrogatories/document requests
3. Organize opponent's document production
4. Prepare for depositions
5. Check discovery deadlines
6. Something else (tell me what)

Choose 1-6:
```

**Action mapping:**
- 1 → List pending requests, offer to draft responses
- 2 → `/draft` discovery requests
- 3 → `/organize` discovery production folder
- 4 → Create deposition outline from evidence
- 5 → Extract deadlines from timeline and GAMEPLAN
- 6 → Ask user to specify

#### MOTION PRACTICE Stage Questions

When detected:
```
I see recent motion activity. How can I help?

1. Draft new motion (specify type)
2. Respond to opponent's motion (which one?)
3. Research motion standards
4. Review draft before filing (fact-check pipeline)
5. Prepare for oral argument
6. Something else (tell me what)

Choose 1-6:
```

**Action mapping:**
- 1 → Ask which motion type, then `/draft`
- 2 → List opponent's motions, offer to draft response
- 3 → `/research` on motion standards for jurisdiction
- 4 → Run `/review` with full pipeline (self-review, citations, opposing counsel, fact verify, final)
- 5 → Create oral argument outline
- 6 → Ask user to specify

#### TRIAL PREP Stage Questions

When detected:
```
Trial preparation mode. What do you need?

1. Organize trial exhibits
2. Prepare witness examination outlines
3. Draft jury instructions
4. Create trial brief
5. Review pre-trial checklist
6. Something else (tell me what)

Choose 1-6:
```

**Action mapping:**
- 1 → `/organize` exhibits, create exhibit list
- 2 → Draft direct/cross examination outlines
- 3 → `/draft` jury instructions
- 4 → `/draft` trial brief
- 5 → Check pre-trial order compliance
- 6 → Ask user to specify

#### GENERAL/UNCLEAR Stage (Fallback)

When stage cannot be clearly determined:
```
I'm ready to help with your case. What would you like to work on?

1. Organize documents from inbox
2. Research legal issues
3. Draft or review documents
4. Check deadlines and next steps
5. Get strategic recommendations
6. Something else (tell me what)

Choose 1-6:
```

**Action mapping:**
- 1 → `/organize`
- 2 → `/research` or `/deep-research-prep`
- 3 → Ask if drafting or reviewing, then `/draft` or `/review`
- 4 → Check GAMEPLAN and timeline for deadlines
- 5 → `/strategy`
- 6 → Ask user to specify

## 6. Default Offer (If Can't Determine Status)

If GAMEPLAN.md is empty template or you can't determine clear status:

> "I'm ready to help with your case. You can:
> - Tell me what you're working on in plain English
> - Use `/strategy` to get strategic recommendations
> - Use `/deep-research-prep` if you're starting research
> - Use `/organize` if you have documents to file
> - Ask me anything about your case or legal procedures"

## 7. Stay Ready for User Requests

User might:
- Ignore your suggestions and ask something specific → Answer their question
- Accept your suggestion → Execute the command/workflow they chose
- Ask a general question → Answer it, then offer relevant next steps

**Remember:**
- Don't be pushy - offer help, but let user drive
- Don't repeat suggestions they already declined
- Adapt to user's working style (some want proactive help, others want to direct you)

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

**CRITICAL: Use AskUserQuestion tool, NOT text-based numbered lists!**

**Format Requirements**:
- **ALWAYS use AskUserQuestion tool** to present options (provides better UX)
- Limit to 4 options max (tool constraint)
- "Other" option automatically added by tool (don't include it yourself)
- Set multiSelect: false (user picks one option)
- Include clear descriptions for each option

#### PRE-FILING Stage Questions

When detected, use AskUserQuestion:

```
AskUserQuestion(
  questions: [{
    question: "I see you're investigating a potential case. What would you like to work on?",
    header: "Next Action",
    multiSelect: false,
    options: [
      {label: "Organize evidence from inbox", description: "Sort and categorize evidence files into proper directories"},
      {label: "Research case viability (deep research)", description: "Generate comprehensive research prompt for Claude.ai Deep Research mode"},
      {label: "Calculate potential damages", description: "Analyze evidence to calculate damages and settlement value"},
      {label: "Check statute of limitations", description: "Research filing deadlines for potential claims"}
    ]
  }]
)
```

**Action mapping:**
- Organize evidence → Run `/organize` command
- Research case viability → Run `/deep-research-prep` or `/strategy`
- Calculate potential damages → Help calculate damages from evidence
- Check statute of limitations → Research statute of limitations for jurisdiction

#### DISCOVERY Stage Questions

When detected (check for urgent deadlines first), use AskUserQuestion:

```
AskUserQuestion(
  questions: [{
    question: "You're in active discovery. What's your priority?",
    header: "Discovery",
    multiSelect: false,
    options: [
      {label: "Respond to pending discovery requests", description: "Draft responses to interrogatories or document requests (deadline: [DATE if exists])"},
      {label: "Draft new interrogatories/document requests", description: "Create discovery requests to send to opposing counsel"},
      {label: "Organize opponent's document production", description: "Sort and categorize documents received from opposing counsel"},
      {label: "Prepare for depositions", description: "Create deposition outline and examination questions"}
    ]
  }]
)
```

**Action mapping:**
- Respond to pending requests → List pending requests, offer to draft responses
- Draft new interrogatories → `/draft` discovery requests
- Organize opponent's production → `/organize` discovery production folder
- Prepare for depositions → Create deposition outline from evidence

#### MOTION PRACTICE Stage Questions

When detected, use AskUserQuestion:

```
AskUserQuestion(
  questions: [{
    question: "I see recent motion activity. How can I help?",
    header: "Motions",
    multiSelect: false,
    options: [
      {label: "Draft new motion", description: "Create a new motion (will ask which type)"},
      {label: "Respond to opponent's motion", description: "Draft opposition or response to opposing counsel's motion"},
      {label: "Research motion standards", description: "Research legal standards and requirements for motions"},
      {label: "Review draft before filing", description: "Run fact-check pipeline (self-review, citations, opposing counsel, fact verify)"}
    ]
  }]
)
```

**Action mapping:**
- Draft new motion → Ask which motion type, then `/draft`
- Respond to opponent's motion → List opponent's motions, offer to draft response
- Research motion standards → `/research` on motion standards for jurisdiction
- Review draft before filing → Run `/review` with full pipeline (self-review, citations, opposing counsel, fact verify, final)

#### TRIAL PREP Stage Questions

When detected, use AskUserQuestion:

```
AskUserQuestion(
  questions: [{
    question: "Trial preparation mode. What do you need?",
    header: "Trial Prep",
    multiSelect: false,
    options: [
      {label: "Organize trial exhibits", description: "Sort exhibits and create exhibit list for trial"},
      {label: "Prepare witness examination outlines", description: "Draft direct and cross-examination questions"},
      {label: "Draft jury instructions", description: "Create proposed jury instructions for trial"},
      {label: "Create trial brief", description: "Draft comprehensive trial brief"}
    ]
  }]
)
```

**Action mapping:**
- Organize trial exhibits → `/organize` exhibits, create exhibit list
- Prepare witness examination outlines → Draft direct/cross examination outlines
- Draft jury instructions → `/draft` jury instructions
- Create trial brief → `/draft` trial brief

#### GENERAL/UNCLEAR Stage (Fallback)

When stage cannot be clearly determined, use AskUserQuestion:

```
AskUserQuestion(
  questions: [{
    question: "I'm ready to help with your case. What would you like to work on?",
    header: "Next Action",
    multiSelect: false,
    options: [
      {label: "Organize documents from inbox", description: "Sort and categorize documents into proper directories"},
      {label: "Research legal issues", description: "Research case law, statutes, or legal standards"},
      {label: "Draft or review documents", description: "Create new documents or review existing drafts"},
      {label: "Get strategic recommendations", description: "Analyze case status and suggest next steps"}
    ]
  }]
)
```

**Action mapping:**
- Organize documents → `/organize`
- Research legal issues → `/research` or `/deep-research-prep`
- Draft or review documents → Ask if drafting or reviewing, then `/draft` or `/review`
- Get strategic recommendations → `/strategy`

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

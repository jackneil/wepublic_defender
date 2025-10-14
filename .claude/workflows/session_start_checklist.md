# Session Start Checklist

**TRIGGER**: Every time a new Claude Code session starts (after first case init is complete)

This checklist helps you quickly understand the current case status and offer relevant next actions.

## ⚠️ CRITICAL: Windows File Editing (READ FIRST)

**If on Windows (`<env>` shows `win32`)**, you MUST use backslashes `\` in Edit/MultiEdit file paths:

**❌ WRONG - Will cause errors:**
```
Edit(file_path: "C:/github/file.py", ...)
```

**✅ CORRECT - Always works:**
```
Edit(file_path: "C:\\github\\file.py", ...)
```

**Bash commands still use forward slashes `/`** - this is ONLY for Edit/MultiEdit tool paths.

**This is a known bug in Claude Code** - Edit tool requires backslashes on Windows even though everything else uses forward slashes.

## 1. Quick Context Load

Read these files to understand current state (read silently, don't output full contents):

1. **GAMEPLAN.md** - Current strategy, next steps, deadlines
2. **01_CASE_OVERVIEW/case_summary.md** (if exists) - Case basics
3. Check for `00_NEW_DOCUMENTS_INBOX/` contents - New files to organize?

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

## 5. Offer Relevant Help

Based on case status and user's likely needs:

### If Case Needs Research:
- `06_RESEARCH/` is empty or sparse
- GAMEPLAN mentions "research needed"
- Legal issues are not well-defined

**Offer:**
> "I notice you don't have much research yet. Would you like to:
> 1. `/deep-research-prep` - Generate comprehensive research prompt for Claude.ai (best for starting new case)
> 2. `/research [topic]` - Quick research on a specific legal question
> 3. `/strategy` - Get strategic recommendations on what to research first"

### If Case Needs Drafting:
- Research exists in `06_RESEARCH/`
- GAMEPLAN says "draft [document]"
- `07_DRAFTS_AND_WORK_PRODUCT/` is empty or drafts are outdated

**Offer:**
> "You have research completed. Would you like to draft a document? I can help with:
> - `/draft [motion to dismiss / response / complaint / discovery]`
> - Or tell me what you need to write"

### If Draft Needs Review:
- Files exist in `07_DRAFTS_AND_WORK_PRODUCT/`
- GAMEPLAN says "review before filing"
- No recent review results in `.wepublic_defender/reviews/`

**Offer:**
> "I see you have drafts in progress. Before filing, would you like me to review:
> - `/review [filename]` - Run adversarial review (opposing counsel attack, citation verification, final review)
> - I'll check for weaknesses, bad citations, and procedural issues"

### If Case is in Good Shape:
- Research done
- Drafts reviewed and strong
- Next deadline not urgent

**Offer:**
> "Your case looks well-organized. Let me know if you need help with anything, or I can check for:
> - New developments in case law (shepardize existing citations)
> - Strategic adjustments
> - Upcoming deadline preparation"

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

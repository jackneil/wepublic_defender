# /timeline Command

View and update the case timeline and document history.

## Usage

```
/timeline                    # View recent timeline entries
/timeline view               # View full timeline
/timeline add                # Add manual timeline entry (interactive)
/timeline filed [file]       # Mark document as filed
/timeline received [file]    # Mark document as received
```

## What This Does

Manages the case timeline in `.wepublic_defender/case_timeline.md` - the permanent historical record of **MAJOR COMPLETED EVENTS**:

**✅ DO track:**
- Documents FILED with court
- Documents RECEIVED from court/opposing counsel
- Communications SENT to court/opposing counsel
- Major research COMPLETED (ready to use)
- Court filings, orders, hearings, deadlines
- Discovery exchanged
- Strategic decisions

**❌ DO NOT track:**
- Draft versions (v1, v2, v3) - use session_notes.md for work in progress
- Work in progress
- Minor research tasks
- Internal discussions
- File organization

## Actions

### 1. View Timeline (Default)

**Command**: `/timeline` or `/timeline view`

**Action**:
1. Read `.wepublic_defender/case_timeline.md`
2. Display most recent 10 entries (major completed events only)
3. Summarize key upcoming events/deadlines from GAMEPLAN.md

**Output Format**:
```
📋 Recent Case Timeline (Major Completed Events)

### 2025-10-15 09:00 - 📄 DOCUMENT - Motion to Dismiss Filed
Status: Filed
File: 02_PLEADINGS/03_Motions/2025-10-14_MotionToDismiss_FINAL.pdf
Notes: Filed via CM/ECF, case 1:25-cv-00123. Hearing: 2025-11-05

### 2025-10-12 09:00 - ⚖️ COURT_EVENT - Order Granting Motion to Compel
Status: Received
File: 02_PLEADINGS/04_Orders/2025-10-12_Order.pdf

[... 8 more entries ...]

📅 Upcoming Deadlines (from GAMEPLAN):
- 2025-10-26: Defendant must produce financial records
- 2025-11-05: Hearing on Motion to Compel
```

---

### 2. Add Manual Entry

**Command**: `/timeline add`

**Action**:
1. Ask user for entry details:
   - Event type (DOCUMENT, COMMUNICATION, COURT_EVENT, RESEARCH, DISCOVERY, STRATEGY)
   - Brief description
   - Status: Filed | Received | Sent | Completed (NOT Draft or Final - this is for major events)
   - Category (Pleading, Discovery, Evidence, Communication, Research, Court Event)
   - File path (if applicable)
   - Notes (additional context)

2. Format entry with current timestamp
3. Insert at top of timeline (reverse chronological)
4. Confirm addition to user

**⚠️ Remember**: This is for major completed events. Don't add drafts or work in progress - use session_notes.md for that.

**Example Interaction**:
```
User: /timeline add

Claude: Adding manual timeline entry.

Event type? (DOCUMENT, COMMUNICATION, COURT_EVENT, RESEARCH, DISCOVERY, STRATEGY)
> COMMUNICATION

Description?
> Email to opposing counsel re: settlement discussion

Status? (Draft, Sent, Received, Filed)
> Sent

Category?
> Communication

File path (optional)?
> 05_CORRESPONDENCE/01_With_Opposing_Counsel/2025-10-14_Settlement_Email.pdf

Additional notes?
> Initial settlement offer $50k, awaiting response

✓ Timeline entry added:

### 2025-10-14 16:45 - 📨 COMMUNICATION - Email to opposing counsel re: settlement discussion

**Status**: Sent
**Category**: Communication
**File**: 05_CORRESPONDENCE/01_With_Opposing_Counsel/2025-10-14_Settlement_Email.pdf
**Notes**: Initial settlement offer $50k, awaiting response
```

---

### 3. Quick Filed Marker

**Command**: `/timeline filed [file]`

**Action**:
1. Identify the document file (prompt if not provided)
2. Ask for filing details:
   - Case number (if applicable)
   - Hearing scheduled? (Y/N)
   - Hearing date (if applicable)
3. Add timeline entry with status "Filed"
4. Update GAMEPLAN.md with hearing deadline if provided

**Example**:
```
User: /timeline filed 02_PLEADINGS/03_Motions/2025-10-14_MotionToDismiss_FINAL.pdf

Claude:
Filing details:
- Case number: 1:25-cv-00123
- Hearing scheduled? (Y/N): Y
- Hearing date: 2025-11-05

✓ Timeline updated:

### 2025-10-15 09:00 - 📄 DOCUMENT - Motion to Dismiss Filed

**Status**: Filed
**Category**: Pleading
**File**: 02_PLEADINGS/03_Motions/2025-10-14_MotionToDismiss_FINAL.pdf
**Notes**: Filed via CM/ECF, case number 1:25-cv-00123. Hearing scheduled for 2025-11-05.

✓ GAMEPLAN.md updated with hearing deadline
```

---

### 4. Quick Received Marker

**Command**: `/timeline received [file]`

**Shortcut for marking document as received**

Useful for:
- Court orders received
- Opposing counsel filings
- Discovery responses

---

## Integration with Session Notes

When you update the timeline, ALSO update `.wepublic_defender/session_notes.md`:

**After timeline update**:
```markdown
## ✅ Completed This Session

### 2025-10-15 09:05
- **Timeline updated**: Marked Motion to Dismiss as FILED
  - Case number: 1:25-cv-00123
  - Hearing scheduled: 2025-11-05
```

---

## File Format

Timeline entries use this format:

```markdown
### YYYY-MM-DD HH:MM - [EVENT_TYPE] - Brief Description

**Status**: Filed | Received | Sent | Completed
**Category**: Pleading | Discovery | Evidence | Communication | Research | Court Event | Strategy
**File**: path/to/document (if applicable)
**Notes**: Additional context relevant to case history

---
```

**Event Type Emojis**:
- 📄 DOCUMENT - Document filed or received (not drafts!)
- 📨 COMMUNICATION - Email/letter sent or received
- ⚖️ COURT_EVENT - Hearing, order, deadline
- 🔍 RESEARCH - Major research completed
- 📋 DISCOVERY - Discovery exchanged
- 🎯 STRATEGY - Strategic decision

---

## Automatic Timeline Updates

The timeline may be updated automatically when major events occur:

1. **/organize** command:
   - When filing documents with court
   - When receiving court filings or orders

2. **After filing documents**:
   - When user confirms document has been filed with court
   - Includes filing details (case number, hearing date)

**⚠️ Note**: Timeline updates are MANUAL by design to ensure accuracy. Use `/timeline filed [file]` or `/timeline received [file]` to add entries when major events occur.

---

## Example Timeline

```markdown
# Case Timeline & Document History

**Case**: Doe v. ABC Corp (1:25-cv-00123)
**Last Updated**: 2025-10-15 09:05

---

## 🕐 Timeline (Reverse Chronological)

### 2025-10-15 09:00 - 📄 DOCUMENT - Motion to Dismiss Filed

**Status**: Filed
**Category**: Pleading
**File**: 02_PLEADINGS/03_Motions/2025-10-14_MotionToDismiss_FINAL.pdf
**Notes**: Filed via CM/ECF, case number 1:25-cv-00123. Hearing scheduled for 2025-11-05.

---

### 2025-10-14 12:00 - 📨 COMMUNICATION - Discovery Extension Request Sent

**Status**: Sent
**Category**: Communication
**File**: 05_CORRESPONDENCE/01_With_Opposing_Counsel/2025-10-14_Discovery_Extension_Request.pdf
**Notes**: Requested 30-day extension for discovery responses. Opposing counsel agreed verbally.

---

### 2025-10-12 09:00 - ⚖️ COURT_EVENT - Order Granting Motion to Compel

**Status**: Received
**Category**: Court Event
**File**: 02_PLEADINGS/04_Orders/2025-10-12_Order_Granting_Motion_to_Compel.pdf
**Notes**: Court granted our motion to compel. Defendant must produce financial records within 14 days (deadline: 2025-10-26).

---

### 2025-10-10 14:00 - 🔍 RESEARCH - Qualified Immunity Standard Research Completed

**Status**: Completed
**Category**: Research
**File**: 06_RESEARCH/01_Case_Law/qualified_immunity_notes.md
**Notes**: Researched Fourth Circuit qualified immunity standard. Found 5 key cases. Ready to incorporate into Motion to Dismiss.

---
```

**Note**: This timeline shows ONLY major completed events. Draft work (Motion v1, v2, v3, review cycles, finalization) is tracked in `session_notes.md`, not here.

---

## Implementation Notes

This is a **guidance-mode-only** command (like /organize) - no external API calls.

Claude Code:
1. Reads `.wepublic_defender/case_timeline.md`
2. Performs requested action (view/add/update)
3. Updates file directly using Edit tool (remember backslashes on Windows!)
4. Updates `.wepublic_defender/session_notes.md` to reflect timeline change
5. Confirms action to user

**No Python script needed** - this is pure file manipulation by Claude Code.

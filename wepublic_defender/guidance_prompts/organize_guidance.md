# Document Organization Guidance for Claude Code

**IMPORTANT: This agent operates in GUIDANCE MODE ONLY**

This agent **NEVER** calls external APIs. It only provides guidance to Claude Code on how to organize documents. All organization work is performed by Claude Code directly, not by external LLMs.

## CRITICAL REQUIREMENTS (from CLAUDE.md)

**Directory Structure Rules:**
1. New documents go to `00_NEW_DOCUMENTS_INBOX/` first
2. Throughout session, keep files in proper directories
3. Never leave files in wrong locations
4. Use this command to organize files with intelligent categorization

**File Organization Rules:**
- Read document contents to categorize properly
- Find and move related drafts with finalized documents
- Consolidate non-standard folders into standard structure
- Smart file renaming for meaningful names
- State tracking to avoid duplicate work

**Directory Purposes:**
- `00_NEW_DOCUMENTS_INBOX/`: Staging area for new files
- `01_CASE_OVERVIEW/`: Case summary, timeline, parties
- `02_PLEADINGS/`: All court filings (complaints, motions, orders)
- `03_DISCOVERY/`: Discovery requests, responses, depositions
- `04_EVIDENCE/`: Evidence documents and exhibits
- `05_CORRESPONDENCE/`: Letters and communications
- `06_RESEARCH/`: Legal research and case law
- `07_DRAFTS_AND_WORK_PRODUCT/`: Working documents and scripts
- `08_REFERENCE/`: Court rules, forms, templates

## Your Task

Organize files from the inbox into appropriate directories.

**Current Inbox Contents:**
```
{inbox_files}
```

**Existing Case Structure:**
```
{existing_structure}
```

## DOCUMENT ORGANIZATION PROCESS

### STEP 1: ANALYZE EACH FILE

For each file in the inbox, determine:

**1. Read the File Content**
- Open and read the document
- Identify document type from content
- Look for key indicators:
  - Court filings (caption, case number)
  - Discovery (interrogatories, requests for production)
  - Correspondence (letters, emails)
  - Evidence (contracts, receipts, communications)
  - Research (case summaries, legal analysis)
  - Drafts (unfinished documents, work product)

**2. Document Type Identification**

**Court Pleadings (`02_PLEADINGS/`):**
- Complaint/Petition
- Answer
- Motion (any type)
- Order (court-issued)
- Brief/Memorandum
- Amended pleadings
- Notices of appearance/withdrawal

**Key Indicators:**
- Has court caption
- Has case number
- Filed/served stamp
- Judge's signature (for orders)
- Certificate of service

**Discovery Documents (`03_DISCOVERY/`):**
- Interrogatories
- Requests for Production
- Requests for Admission
- Responses to discovery
- Deposition transcripts/notices
- Subpoenas

**Key Indicators:**
- "INTERROGATORIES" in title
- "REQUESTS FOR PRODUCTION" in title
- "RESPONSES TO" in title
- "DEPOSITION OF" in title
- Numbered requests/responses

**Evidence Documents (`04_EVIDENCE/`):**
- Contracts
- Agreements
- Receipts
- Financial records
- Communications (emails, texts)
- Photos/videos
- Expert reports

**Key Indicators:**
- Transaction documents
- Signed agreements
- Dated communications
- Financial statements
- Technical reports

**Correspondence (`05_CORRESPONDENCE/`):**
- Letters to/from opposing counsel
- Letters to/from court
- Internal memos
- Email chains (non-evidence)

**Key Indicators:**
- Letter format
- "Dear" salutation
- Professional signature
- Law firm letterhead

**Research Documents (`06_RESEARCH/`):**
- Case law summaries
- Legal memoranda
- Statute research
- Court rule analysis
- Secondary sources

**Key Indicators:**
- Citations to cases
- Legal analysis
- Research notes
- Case summaries

**Drafts (`07_DRAFTS_AND_WORK_PRODUCT/`):**
- Draft pleadings (not filed yet)
- Work-in-progress documents
- Outlines
- Strategy notes
- Template documents

**Key Indicators:**
- "DRAFT" in filename or content
- Incomplete sections
- [TODO] markers
- Version numbers
- No filing stamp

**Reference Materials (`08_REFERENCE/`):**
- Court rules
- Forms
- Templates
- Practice guides
- Procedural checklists

**Key Indicators:**
- Generic (not case-specific)
- Official court forms
- Template language
- Procedural guides

### STEP 2: CATEGORIZE AND ORGANIZE

**For Each Document:**

**1. Primary Category**
- Determine main category (02-08)
- Read content to confirm
- Check for filing stamps or dates

**2. Subcategory (if applicable)**

**Pleadings Subcategories:**
- `01_Complaint/` - Initial complaint/petition
- `02_Answer/` - Defendant's answer
- `03_Motions/` - All motions
- `04_Orders/` - Court orders
- `05_Briefs/` - Briefs and memoranda
- `06_Amendment/` - Amended pleadings

**Discovery Subcategories:**
- `01_Our_Requests/` - Discovery we sent
- `02_Their_Requests/` - Discovery they sent
- `03_Our_Responses/` - Our responses
- `04_Their_Responses/` - Their responses
- `05_Deposition_Transcripts/` - Deposition materials

**Evidence Subcategories:**
- `01_Documents/` - Contracts, agreements, written evidence
- `02_Communications/` - Emails, letters, texts
- `03_Financial_Records/` - Financial documents
- `04_Expert_Reports/` - Expert witness materials

**Correspondence Subcategories:**
- `01_With_Opposing_Counsel/` - Attorney correspondence
- `02_With_Court/` - Court correspondence
- `03_Internal/` - Internal notes and memos

**Research Subcategories:**
- `01_Case_Law/` - Case research
- `02_Statutes/` - Statutory research
- `03_Secondary_Sources/` - Articles, treatises, etc.

**3. File Naming**

**Good File Names:**
- Descriptive
- Include date (YYYY-MM-DD format)
- No spaces (use underscores)
- Uppercase for document type

**Examples:**
- `MOTION_TO_DISMISS_2025-01-15.pdf`
- `COMPLAINT_FILED_2025-01-01.pdf`
- `DISCOVERY_REQUESTS_SENT_2025-02-01.pdf`
- `CONTRACT_SIGNED_2024-12-15.pdf`

**Rename If Needed:**
- Original: `document1.pdf`
- Better: `MOTION_FOR_SUMMARY_JUDGMENT_2025-03-01.pdf`

### STEP 3: HANDLE SPECIAL CASES

**Multiple Related Files:**
- Draft + Final: Move both, but to different locations
  - Draft → `07_DRAFTS_AND_WORK_PRODUCT/drafts/`
  - Final → Appropriate final location (02-06)
- Exhibits with main document: Keep together
  - Create subfolder if many exhibits
  - Name exhibits: `{MAIN_DOC}_Exhibit_A.pdf`

**Duplicate Files:**
- Check if already organized
- Read `.database/file_management_index.json`
- Skip if already processed
- Note in log if duplicate found

**Uncertain Classification:**
- Read content carefully
- Look for multiple indicators
- Choose most specific category
- Note uncertainty in log
- User can review and move if wrong

### STEP 4: UPDATE STATE TRACKING

**After Each Move:**

**1. Update File Management Log (`.database/file_management_log.md`)**

Append one line:
```
2025-10-13 14:30:00 | moved | 00_NEW_DOCUMENTS_INBOX/doc.pdf | 02_PLEADINGS/03_Motions/MOTION_TO_DISMISS_2025-10-13.pdf | Categorized as motion based on court caption and content
```

**2. Update File Management Index (`.database/file_management_index.json`)**

Add entry:
```json
{
  "02_PLEADINGS/03_Motions/MOTION_TO_DISMISS_2025-10-13.pdf": {
    "timestamp": "2025-10-13 14:30:00",
    "action": "moved",
    "src": "00_NEW_DOCUMENTS_INBOX/doc.pdf",
    "dst": "02_PLEADINGS/03_Motions/MOTION_TO_DISMISS_2025-10-13.pdf",
    "notes": "Categorized as motion based on court caption and content"
  }
}
```

## ORGANIZATION OUTPUT FORMAT

```markdown
# Document Organization Report

## Summary

**Total Files Processed:** {number}
**Successfully Organized:** {number}
**Skipped (Already Organized):** {number}
**Uncertain Classifications:** {number}

---

## Files Organized

### 1. {Original Filename}

**Type Identified:** [Document type]

**Key Indicators:**
- [Indicator 1 from content]
- [Indicator 2 from content]

**Destination:** `{target_directory}/{new_filename}`

**Renamed:** [Yes/No - Old name → New name]

**Reasoning:** [Why this categorization]

---

### 2. {Next File}

[Same format]

---

## Files Requiring Review

[Any files with uncertain classification]

**Filename:** {filename}
**Why Uncertain:** [Explanation]
**Suggested Location:** {directory}
**Alternative:** {other_directory}
**User Action Needed:** [What to decide]

---

## State Tracking Updated

- File management log updated: `.database/file_management_log.md`
- File management index updated: `.database/file_management_index.json`

---

## Inbox Status

**Remaining Files:** {number}

[List any files not processed and why]

---

## Recommendations

1. [Any follow-up actions]
2. [Suggestions for user]
```

## ORGANIZATION CHECKLIST

Before completing organization:

- [ ] I read the content of each file
- [ ] I identified document type from content (not just filename)
- [ ] I checked for existing organization (avoid duplicates)
- [ ] I used meaningful filenames
- [ ] I moved files to appropriate subdirectories
- [ ] I updated file management log
- [ ] I updated file management index
- [ ] I noted any uncertain classifications
- [ ] I provided clear reasoning for each decision

## SPECIAL RULES

**NEVER:**
- Organize based solely on filename
- Delete files (only move)
- Overwrite existing files without checking
- Skip reading file contents
- Leave inbox with unprocessed files without explanation

**ALWAYS:**
- Read file contents to determine type
- Use descriptive filenames
- Update state tracking
- Note reasoning for decisions
- Flag uncertain classifications

## REMEMBER

- **Read contents, don't guess** - Filenames lie, content doesn't
- **Be systematic** - Process every file
- **Update state** - Log every action
- **Be conservative** - When uncertain, flag for review
- **Be helpful** - Good organization saves time later

**This agent never uses external APIs. All work is done by Claude Code directly.**

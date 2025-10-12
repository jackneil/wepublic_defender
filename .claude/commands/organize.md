# /organize Command

Organize all files from 00_NEW_DOCUMENTS_INBOX/ into appropriate directories.

## Process

1. **Scan Inbox**
   - List all files in 00_NEW_DOCUMENTS_INBOX/
   - **MANDATORY: Read document contents** to determine actual document type
   - Do not rely solely on filenames or folder locations

2. **Categorize Files and Find Related Drafts**
   For each file, **read the actual content** and:
   - Determine the appropriate destination directory based on document type
   - Check `.database/` files to identify related drafts in `07_DRAFTS_AND_WORK_PRODUCT/`
   - Match drafts by content similarity, document title, case caption, or subject matter
   - If matching drafts found:
     * Plan to move BOTH the final document AND all related drafts to the same destination
     * Apply smart renaming to both final and draft versions
     * Keep drafts with final documents for historical record
     * Clearly mark draft versions in filename (e.g., `_draft_v1`, `_draft_v2`)

   Categorize into:

   **02_PLEADINGS/** subfolders:
   - Complaint/Petition → 01_Complaint/
   - Answer/Response to Complaint → 02_Answer/
   - Motion → 03_Motions/
   - Court Order/Judgment → 04_Orders/
   - Brief/Memorandum (legal argument) → 05_Briefs/
   - Amended Complaint/Motion to Amend → 06_Amendment/

   **03_DISCOVERY/**:
   - Our discovery requests → 01_Our_Requests/
   - Their discovery requests → 02_Their_Requests/
   - Our responses → 03_Our_Responses/
   - Their responses → 04_Their_Responses/
   - Deposition transcripts → 05_Deposition_Transcripts/

   **04_EVIDENCE/**:
   - Contracts, agreements → 01_Documents/
   - Emails, letters, calls → 02_Communications/
   - Bank statements, financial records → 03_Financial_Records/
   - Expert reports → 04_Expert_Reports/

   **05_CORRESPONDENCE/**:
   - Letters to/from opposing counsel → 01_With_Opposing_Counsel/
   - Letters to/from court → 02_With_Court/
   - Internal case notes → 03_Internal/

   **06_RESEARCH/**:
   - Case law research → 01_Case_Law/
   - Statute research → 02_Statutes/
   - Secondary sources → 03_Secondary_Sources/

   **07_DRAFTS_AND_WORK_PRODUCT/**:
   - Draft documents → drafts/
   - Outlines → outlines/
   - Scripts/tools → scripts/

   **08_REFERENCE/**:
   - Court rules → court_rules/
   - Blank forms → forms/
   - Templates → templates/

3. **Move Files**
   - Move each file to appropriate **subfolder** based on content
   - **Do not leave files in parent directories** (e.g., not in 02_PLEADINGS/ directly, but in 02_PLEADINGS/03_Motions/)
   - Create additional subdirectories if needed
   - Preserve original filenames (or rename per conventions)

## Smart File Renaming (Make Names Human‑Meaningful)

If a filename is not meaningful (e.g., random numbers, scan_####, image####, untitled, generic export names), rename it during the move so a human can identify it at a glance.

1. **Decide if Renaming Is Needed**
   - Low‑value names include patterns like: `IMG_1234`, `scan_20250101`, `000123.pdf`, `doc.pdf`, `export (1).pdf`, `Untitled.docx`.
   - High‑value names already include sender/recipient, document type, and/or date.

2. **Extract Metadata From Content (read the file)**
   - Emails/letters: From/To, Subject/Title, Date (header, letterhead, signature block)
   - Court filings: Case caption (Plaintiff v. Defendant), document title (e.g., Motion to Dismiss), filing date
   - Evidence:
     - Bank statements: Bank name, account last4 if visible, statement date/period
     - Communications: Sender → Recipient, channel (email/sms/letter)
     - Transcripts: Deponent name, date, case

3. **Renaming Convention (keep it short, keep extension)**
   - Prefer ISO date first if known: `YYYY-MM-DD_...`
   - Use underscores `_` as separators; avoid spaces; keep original extension
   - Include a concise, high‑signal summary; examples:
     - Communications: `2025-01-15_Smith>Jones_Email_SubpoenaFollowup.pdf`
     - Court filing: `2025-02-03_Doe_v_CapitalOne_MotionToDismiss.pdf`
     - Evidence: `2024-12-01_BankOfAmerica_Stmt_ending1234.pdf`
     - Transcript: `2025-03-20_Jones_Deposition.pdf`
   - If sender/recipient roles matter (Plaintiff/Defendant/Court), prefer role or name that aids recognition.

4. **Collisions & Length**
   - On name collisions, append a short suffix: `_v2`, `_v3`, or `_(2)`
   - Keep filenames under ~120 characters where possible; abbreviate long subjects (e.g., `SubpoenaFollowup` → `SubpFollowup`)

5. **Record the Rename**
   - Append an entry to `.database/file_management_log.md` and update the JSON index
   - Example (helper command):
     ```
     wpd-file-log --action renamed --src "05_CORRESPONDENCE/email.pdf" --dst "05_CORRESPONDENCE/Smith>Jones_Email_SubpFollowup_2025-01-15.pdf" --notes "meaningful rename"
     ```
   - Or edit both files directly (see State Tracking section)

4. **Report**
   - Show user where each file was moved
   - Ask for confirmation if uncertain about any categorization

## Intelligent Organization Protocol

When organizing, go beyond just the inbox:

1. **Scan Entire Case Directory**
   - Look beyond just 00_NEW_DOCUMENTS_INBOX/
   - Find ALL misplaced files recursively
   - Identify user-created folders that don't match standard structure

2. **Handle Duplicate/Non-Standard Folders**
   - If user has non-standard folders (e.g., `04_EVIDENCE/Contracts/` vs `04_EVIDENCE/01_Documents/`):
     * Recognize the folder serves the same purpose as the standard folder
     * MERGE contents: move files from user folder → standard folder
     * Remove empty non-standard folder after merge
     * Preserve user's organizational intent while normalizing structure

3. **Example Consolidation Scenario**
   User has:
   04_EVIDENCE/01_Contracts/ (3 PDFs)
   04_EVIDENCE/01_Documents/ (empty, from init)
   04_EVIDENCE/02_Statements/ (35 PDFs)
   04_EVIDENCE/02_Communications/ (empty, from init)

   Action:
   Move 04_EVIDENCE/01_Contracts/* → 04_EVIDENCE/01_Documents/
   Remove 04_EVIDENCE/01_Contracts/ (now empty)
   Move 04_EVIDENCE/02_Statements/* → 04_EVIDENCE/03_Financial_Records/
   Remove 04_EVIDENCE/02_Statements/ (now empty)

4. **Move Finalized Drafts With Filed Documents**
   When organizing documents from inbox that match drafts in `07_DRAFTS_AND_WORK_PRODUCT/`:
   - Move the final document to its proper location (e.g., `02_PLEADINGS/03_Motions/`)
   - Move ALL related draft versions to the SAME destination directory
   - Keep drafts with their final versions for historical record
   - Never leave orphaned drafts in `07_DRAFTS_AND_WORK_PRODUCT/` after filing

   Example:
   - Inbox: `MOTION_TO_DISMISS_FINAL.pdf` (needs filing)
   - Related drafts in database: `07_DRAFTS_AND_WORK_PRODUCT/drafts/motion_to_dismiss_v1.md`, `motion_to_dismiss_v2.md`
   - Action:
     * Move final → `02_PLEADINGS/03_Motions/2025-10-12_Doe_v_CapitalOne_MotionToDismiss.pdf`
     * Move drafts → `02_PLEADINGS/03_Motions/2025-10-12_Doe_v_CapitalOne_MotionToDismiss_draft_v1.md`
     * Move drafts → `02_PLEADINGS/03_Motions/2025-10-12_Doe_v_CapitalOne_MotionToDismiss_draft_v2.md`

5. **Guiding Principles**
- Preserve all user files (never delete actual documents)
- Normalize to standard structure over time
- Remove only empty folders after consolidation
- Keep draft history with filed documents (don't orphan drafts)
- Use database/content matching to identify related documents
- Report all moves clearly for user awareness

## State Tracking (.database)

Maintain a file-management ledger under `.database/` so we don't reprocess the same moves unnecessarily:

- Append actions to `.database/file_management_log.md` (and update `.database/file_management_index.json`). You can write these files directly (Edit/MultiEdit) or use the helper command:
```
wpd-file-log --action moved --src "04_EVIDENCE/01_Contracts/file.pdf" --dst "04_EVIDENCE/01_Documents/file.pdf" --notes "normalize folder name"
```

- Before moving a file/folder, read the JSON index to avoid duplicate work.

- Never delete user documents. Remove only empty folders after consolidations. Always record the action.

## Example Output

```
Organizing 7 files from inbox...

✓ AMENDED_COMPLAINT.docx → 02_PLEADINGS/06_Amendment/
✓ discovery_request_draft.md → 03_DISCOVERY/01_Our_Requests/
✓ email_from_opposing_counsel.pdf → 05_CORRESPONDENCE/01_With_Opposing_Counsel/
✓ bank_statement_2023.pdf → 04_EVIDENCE/03_Financial_Records/
✓ research_notes_statute_limitations.md → 06_RESEARCH/
? unknown_document.pdf → [ASK USER]

Moved 6 files, 1 needs categorization.
```

## Implementation

Call the organize_inbox.py script from wepublic_defender/scripts/ or implement inline with file categorization logic.

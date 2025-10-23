# File Organization System

WePublicDefender uses a standard legal file organization system that keeps your case documents organized like a real law firm would.

## Directory Structure Overview

When you initialize a case, these folders are created:

```
YourCaseFolder/
├── 00_NEW_DOCUMENTS_INBOX/      # Drop new files here
├── 01_CASE_OVERVIEW/            # Summary, timeline, strategy
├── 02_PLEADINGS/                # Court filings
│   ├── 01_Complaint/
│   ├── 02_Answers/
│   ├── 03_Motions/
│   └── 04_Orders/
├── 03_DISCOVERY/                # Discovery documents
│   ├── 01_Requests/
│   ├── 02_Responses/
│   └── 03_Productions/
├── 04_EVIDENCE/                 # Evidence and exhibits
├── 05_CORRESPONDENCE/           # Letters and emails
│   ├── 01_With_Opposing_Counsel/
│   ├── 02_With_Court/
│   └── 03_With_Client/
├── 06_RESEARCH/                 # Legal research
├── 07_DRAFTS_AND_WORK_PRODUCT/ # Working documents
├── 08_REFERENCE/                # Rules, templates
├── .wepublic_defender/          # System files (hidden)
├── .database/                   # Tracking files (hidden)
└── .claude/                     # Claude commands (hidden)
```

## Understanding Each Folder

### 00_NEW_DOCUMENTS_INBOX

**Purpose**: Staging area for new documents

**What goes here**:
- Any new documents you receive
- Downloads from email
- Scanned documents
- Documents you're not sure where to file

**How it works**:
1. Drop files here
2. Run `/organize`
3. Claude sorts them into proper folders

**Best practice**: Empty regularly by organizing

### 01_CASE_OVERVIEW

**Purpose**: High-level case information

**Key files**:
- `case_summary.md` - Parties, claims, overview
- `GAMEPLAN.md` - Strategy and next steps
- `timeline.md` - Chronology of events
- `key_facts.md` - Important facts
- `contact_info.md` - Attorney and party contacts

**When to update**: After major case developments

### 02_PLEADINGS

**Purpose**: All court filings

**Subfolders**:

#### 01_Complaint
- Initial complaint/petition
- Amended complaints
- Exhibits to complaint

#### 02_Answers
- Defendant's answers
- Affirmative defenses
- Counterclaims

#### 03_Motions
- All motions (yours and theirs)
- Responses to motions
- Reply briefs
- Supporting declarations

#### 04_Orders
- Court orders
- Scheduling orders
- Rulings on motions

**Naming convention**:
```
2025-10-15_Motion_to_Dismiss.pdf
2025-10-20_Response_to_Motion_to_Dismiss.pdf
2025-10-25_Order_Denying_Motion.pdf
```

### 03_DISCOVERY

**Purpose**: Discovery materials

**Subfolders**:

#### 01_Requests
- Your interrogatories
- Your document requests
- Your admission requests
- Deposition notices

#### 02_Responses
- Your responses to their discovery
- Their responses to your discovery
- Objections

#### 03_Productions
- Documents produced by either side
- Organized by production date or bates numbers

**Organization tip**: Create subfolders by date:
```
03_Productions/
├── 2025-10-15_Defendant_Production/
├── 2025-11-01_Plaintiff_Production/
```

### 04_EVIDENCE

**Purpose**: Evidence supporting your case

**Common subfolders**:
```
04_EVIDENCE/
├── contracts/
├── emails/
├── photos/
├── videos/
├── audio/
├── expert_reports/
├── medical_records/
├── financial_records/
```

**Best practices**:
- Use descriptive names
- Include dates in filenames
- Keep originals untouched
- Create summaries for large collections

### 05_CORRESPONDENCE

**Purpose**: Communications about the case

**Subfolders**:

#### 01_With_Opposing_Counsel
- Letters between lawyers
- Email threads
- Meet and confer communications

#### 02_With_Court
- Letters to judge
- Correspondence from clerk
- Scheduling communications

#### 03_With_Client
- Client communications
- Retainer agreements
- Status updates

### 06_RESEARCH

**Purpose**: Legal research and analysis

**Common files**:
- `case_law_research.md` - Relevant cases
- `statute_research.md` - Applicable statutes
- `CITATIONS_LOG.md` - Verified citations
- `deep_research_[date].md` - Deep research results
- `legal_theories.md` - Theory development

**Organization**:
```
06_RESEARCH/
├── case_law/
├── statutes/
├── regulations/
├── deep_research/
└── strategy_memos/
```

### 07_DRAFTS_AND_WORK_PRODUCT

**Purpose**: Working documents not yet filed

**What goes here**:
- Draft motions
- Work-in-progress briefs
- Outline documents
- Strategy notes
- Meeting notes

**Version control**:
```
motion_to_dismiss_v1.md
motion_to_dismiss_v2.md
motion_to_dismiss_v3.md
motion_to_dismiss_FINAL.md
```

### 08_REFERENCE

**Purpose**: Reference materials

**Common contents**:
- Court rules
- Local rules
- Form templates
- Checklists
- Legal guides
- Sample documents

## Hidden Folders

### .wepublic_defender

**Purpose**: System configuration

**Important files**:
- `env_info.json` - Python paths
- `case_settings.json` - Case configuration
- `legal_review_settings.json` - AI settings
- `session_notes.md` - Current work tracking
- `case_timeline.md` - Major events
- `usage_log.csv` - API costs

### .database

**Purpose**: File tracking

**Files**:
- `file_management_log.md` - Movement history
- `file_management_index.json` - Processing tracker

### .claude

**Purpose**: Claude Code integration

**Contents**:
- `commands/` - Slash commands
- `CLAUDE.md` - Orchestrator instructions

## Using the Organization System

### Manual Organization

Drop file in correct folder yourself:
1. Identify document type
2. Navigate to appropriate folder
3. Copy/move file there
4. Use descriptive filename

### Automatic Organization

Let Claude do it:
```
/organize
```

Claude will:
1. Read each file in inbox
2. Determine correct location
3. Move file
4. Log the action

### Bulk Organization

Got many files?
```
I have 50 documents from discovery. Please organize them.
```

## File Naming Best Practices

### Include Dates

Use YYYY-MM-DD format:
```
2025-10-15_Motion_to_Compel.pdf
```

### Be Descriptive

Good:
```
2025-10-15_Smith_Deposition_Transcript.pdf
```

Bad:
```
doc1.pdf
```

### Use Underscores

Instead of spaces:
```
Motion_to_Dismiss.pdf  ✓
Motion to Dismiss.pdf   ✗
```

### Version Numbers

For drafts:
```
complaint_v1.md
complaint_v2_with_exhibits.md
complaint_v3_FINAL.md
```

### Bates Numbers

For produced documents:
```
DEF_001234-001256.pdf
PLT_000001-000145.pdf
```

## Finding Files

### Quick Search

```
Find all motions filed in October
```

### By Type

```
Show me all correspondence with opposing counsel
```

### Recent Files

```
What documents were added today?
```

### By Content

```
Find documents mentioning "arbitration"
```

## Organization Maintenance

### Regular Tasks

#### Daily
- Check inbox for new files
- Organize anything received

#### Weekly
- Review drafts folder
- Archive old versions
- Update case overview

#### After Major Events
- Update timeline
- File final versions
- Archive drafts

### Spring Cleaning

```
Review my file organization and suggest improvements
```

## Special Scenarios

### Large Productions

Receiving hundreds of documents:

1. Create dated subfolder:
```
03_DISCOVERY/03_Productions/2025-10-15_Defendant_Production/
```

2. Keep production index:
```
production_index.md
```

3. Organize by category within:
```
2025-10-15_Defendant_Production/
├── emails/
├── contracts/
├── financial/
```

### Confidential Documents

Mark sensitive documents:
```
CONFIDENTIAL_settlement_discussion.pdf
PRIVILEGED_attorney_notes.md
```

### Exhibits

Preparing for trial:
```
04_EVIDENCE/trial_exhibits/
├── P001_Contract.pdf
├── P002_Email_Chain.pdf
├── D001_Invoice.pdf
```

## Troubleshooting

### Can't Find a File

```
Help me find the motion to dismiss
```

Claude will search and locate it.

### Duplicate Files

```
Check for duplicate files in my case folder
```

### Wrong Location

If file is in wrong place:
```
Move summary_judgment.pdf from inbox to 02_PLEADINGS/03_Motions/
```

### Messy Organization

```
My files are a mess. Please reorganize everything.
```

## Integration with Features

### Review Pipeline

Reviews need files in correct locations:
- Drafts in `07_DRAFTS_AND_WORK_PRODUCT/`
- Evidence in `04_EVIDENCE/` for fact checking

### Deep Research

Research results go to:
- Initial: `00_NEW_DOCUMENTS_INBOX/`
- Organized: `06_RESEARCH/deep_research/`

### Citation Verification

Citations logged in:
- `06_RESEARCH/CITATIONS_LOG.md`

## Best Practices Summary

1. **Use the inbox** - Don't scatter files everywhere
2. **Organize regularly** - Don't let inbox get too full
3. **Name descriptively** - Future you will thank you
4. **Date everything** - YYYY-MM-DD format
5. **Keep versions** - Don't overwrite, create new versions
6. **Archive old drafts** - Keep final versions accessible
7. **Document organization** - Note where things are

## Tips for Success

### For New Cases

1. Put ALL documents in inbox first
2. Run `/organize` once
3. Review where things went
4. Adjust if needed

### For Ongoing Cases

1. Check inbox daily
2. Organize new documents immediately
3. Update overview files regularly
4. Archive completed work

### For Complex Cases

1. Create additional subfolders as needed
2. Maintain indexes for large collections
3. Use consistent naming schemes
4. Regular organization reviews

## Next Steps

- Learn to [organize automatically](Slash-Commands-Reference#organize)
- Understand [session tracking](Session-Start-Automation)
- Set up [review pipeline](Review-Pipeline)
- Configure [your settings](Configuration)
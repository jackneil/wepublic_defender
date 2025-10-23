# Integration Patterns

How WePublicDefender integrates with other tools, services, and workflows.

## Overview

WePublicDefender is designed to integrate seamlessly with your existing legal workflow. This guide covers common integration patterns and how to connect WePublicDefender with external tools.

## Claude Code Integration

### Primary Integration: Claude Code CLI

WePublicDefender is built as a **Claude Code-native system** - meaning Claude orchestrates everything.

**How it works:**
1. User opens Claude Code in case folder
2. Claude loads case context automatically (session start)
3. User talks to Claude in plain English
4. Claude runs agents, processes results, updates files
5. User reviews Claude's work and approves changes

**Key features:**
- Natural language interface (no command memorization)
- Plan mode for reviewing actions before execution
- Tab key to see Claude's reasoning
- Automatic session memory (session_notes.md)
- Slash commands for common workflows

### Slash Commands

WePublicDefender extends Claude Code with custom slash commands:

```
/check-env        - Verify environment setup
/organize         - Organize files from inbox
/timeline         - View/update case timeline
/deep-research-prep - Generate deep research prompt
/research [topic] - Quick legal research
/strategy         - Get strategic recommendations
/draft [type]     - Draft legal document
/review [file]    - Run adversarial review
```

**These commands are defined in:** `.claude/commands/`

**How they work:**
- Each command is a markdown file with instructions for Claude
- Claude reads the file and follows the workflow
- User interacts with Claude, not the command directly

### Session Context Persistence

WePublicDefender maintains context across sessions using:

**Session files:**
- `.wepublic_defender/session_notes.md` - Work tracking, crash recovery
- `.wepublic_defender/case_timeline.md` - Historical case events
- `GAMEPLAN.md` - Strategic roadmap and deadlines

**Session start workflow:**
- Claude automatically reads these files when starting
- Knows what was worked on last time
- Aware of upcoming deadlines
- Offers relevant next actions

**Manual context refresh:**
```
/start  - Re-run session checklist anytime
```

## External LLM Integration

### Supported LLM Providers

WePublicDefender can call multiple external LLMs for adversarial review:

**Currently supported:**
- OpenAI (GPT-5, GPT-4o, GPT-4-turbo)
- xAI (Grok-4, Grok-3)

**Configuration:** `.wepublic_defender/legal_review_settings.json`

```json
{
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-5", "grok-4"],
      "temperature": 0.3,
      "max_tokens": 8000,
      "web_search": false
    },
    "citation_verify_agent": {
      "models": ["gpt-5"],
      "web_search": true
    }
  }
}
```

### Multi-Model Adversarial Review

**Pattern:** Run multiple LLMs in parallel, compare results

**Why this works:**
- Different training data = different perspectives
- Consensus on issues = high confidence it's real
- Unique findings = potential blind spots to investigate

**Example workflow:**
```python
# Run self-review with 2 models
wpd-run-agent --agent self_review --file draft.md --mode external-llm

# System calls both GPT-5 and Grok-4 in parallel
# Returns consensus findings and unique findings
# Claude analyzes results and presents summary
```

**Consensus analysis:**
```
Issue found by ALL models → Critical, must fix
Issue found by MOST models → Important, investigate
Issue found by ONE model → Evaluate validity
```

### Adding New LLM Providers

**To add Gemini, Claude, Mistral, etc.:**

1. Add API client to `wepublic_defender/llm_client.py`
2. Update settings schema to support new provider
3. Configure in `legal_review_settings.json`

**Future providers being considered:**
- Google Gemini (Pro, Ultra)
- Anthropic Claude (via API)
- Mistral Large
- Llama 3 405B (via Groq, Together, Replicate)
- Cohere Command R+

## Claude.ai Deep Research Integration

### Pattern: Offload Heavy Research to Claude.ai

**Why separate from Claude Code:**
- Claude.ai has Deep Research mode (50+ interconnected web searches)
- More thorough than quick web search in Claude Code
- Better for comprehensive case assessment
- Results downloadable for later reference

**Workflow:**

1. **Generate research prompt in Claude Code:**
   ```
   /deep-research-prep
   ```

2. **Claude Code creates comprehensive research prompt** including:
   - Legal claims analysis
   - Damages assessment
   - Venue & jurisdiction
   - Defense predictions
   - Procedural requirements
   - Strategic considerations

3. **Copy prompt to Claude.ai:**
   - Open https://claude.ai
   - Enable Research mode (button bottom-left)
   - Paste prompt
   - Wait 5-10 minutes for deep research

4. **Download results:**
   - Click three-dots menu
   - Select "Download conversation"
   - Save to `00_NEW_DOCUMENTS_INBOX/`

5. **Tell Claude Code you're done:**
   ```
   Done. I downloaded the research to the inbox.
   ```

6. **Claude Code processes results:**
   - Moves file to `06_RESEARCH/`
   - Analyzes findings
   - Generates GAMEPLAN.md with strategic roadmap
   - Marks initial research complete

**Cost-effectiveness:**
- One deep research session ≈ cost of one lawyer consultation
- Comprehensive 50+ page analysis
- Reusable throughout case lifecycle

## CourtListener API Integration

### Pattern: Legal Citation Verification

**What it does:**
- Verifies citations are still good law
- Checks if cases have been overruled/reversed
- Retrieves case metadata and citations

**Setup:**

1. Register at https://www.courtlistener.com/register/
2. Get API token at https://www.courtlistener.com/api/
3. Add to `.env`:
   ```
   COURTLISTENER_TOKEN=your_token_here
   COURTLISTENER_USER_AGENT=WePublicDefender/0.1
   ```

**Usage in citation verification:**
```bash
# Verify single citation
wpd-verify-citation "Smith v. Jones, 123 F.3d 456 (4th Cir. 2020)"

# Verify all citations in document (with web search)
wpd-run-agent --agent citation_verify --file motion.md --mode external-llm --web-search
```

**How it works:**
1. Agent finds all citations in document
2. Queries CourtListener API for case status
3. Web search for recent developments if needed
4. Returns: good law status, citations, related cases
5. Updates `06_RESEARCH/CITATIONS_LOG.md` cache

**Fallback:** If CourtListener unavailable, uses web search only

## Document Conversion Integration

### Pattern: Markdown to Word for Court Filing

**Problem:** Courts require .docx files, we work in .md (markdown)

**Solution:** Automatic conversion with formatting preservation

```bash
wpd-convert-to-word --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_FINAL.md --output 02_PLEADINGS/03_Motions/MOTION_TO_DISMISS.docx
```

**Conversion features:**
- Preserves headings, lists, emphasis
- Converts citations to proper format
- Applies court-compliant formatting
- Adds page numbers, margins

**Libraries used:**
- `python-docx` for Word document generation
- Custom formatting templates for court rules

### Pattern: PDF to Images for Large Documents

**Problem:** Large PDFs (100+ pages) exceed Claude's token limits

**Solution:** Convert to images, read specific pages

```bash
# Convert entire PDF
wpd-pdf-to-images "huge_credit_report.pdf"

# Creates: huge_credit_report_images/page_0001.png, page_0002.png, ...

# Read specific pages in Claude Code
Read(file_path="huge_credit_report_images/page_0042.png")
```

**When to use:**
- Credit reports (often 50-100+ pages)
- Lengthy court orders
- Large discovery exhibits
- Multi-page contracts

**Libraries used:**
- `PyMuPDF` (fitz) for PDF rendering
- High-quality image conversion (150+ DPI)

## File Organization Integration

### Pattern: Automatic Document Classification

**How organize agent works:**
1. Scans `00_NEW_DOCUMENTS_INBOX/`
2. Reads file contents (PDFs, images, Word docs, text files)
3. Classifies document type (pleading, evidence, discovery, etc.)
4. Moves to appropriate directory
5. Logs action in `.database/file_management_log.md`
6. Indexes in `.database/file_management_index.json`

**Supported file types:**
- PDF (reads with pdfplumber)
- Word (.docx) - reads with python-docx
- Images (PNG, JPG) - OCR with Claude's vision
- Text files (.txt, .md)
- Email exports (.eml, .mbox)

**Integration with case structure:**
```
00_NEW_DOCUMENTS_INBOX/  → Intake
01_CASE_OVERVIEW/        → Classified docs
02_PLEADINGS/            → Court filings
03_DISCOVERY/            → Discovery materials
04_EVIDENCE/             → Evidence files
05_CORRESPONDENCE/       → Communications
06_RESEARCH/             → Legal research
07_DRAFTS_AND_WORK_PRODUCT/ → Work in progress
08_REFERENCE/            → Templates, rules
```

## Version Control Integration (Git)

### Pattern: Track Case Changes with Git

**Why use git:**
- Version history of all drafts
- Revert to previous document versions
- Track what changed between iterations
- Collaborate with other legal team members

**Recommended .gitignore:**
```
# Ignore sensitive files
.env
*.pdf
*.docx

# Ignore ephemeral state
.database/
.wepublic_defender/logs/
.wepublic_defender/usage_log.csv

# Keep important configs
!.wepublic_defender/legal_review_settings.json
!.wepublic_defender/env_info.json
```

**Workflow:**
```bash
# After major milestones
git add 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v3.md
git add GAMEPLAN.md
git add 06_RESEARCH/

git commit -m "Completed motion v3 after opposing counsel review"
git push origin main
```

**Branch strategy:**
```
main              - Finalized filings only
draft/motion-to-dismiss - Working draft
research/qualified-immunity - Research branch
```

## CI/CD Integration (GitHub Actions)

### Pattern: Automated Quality Checks

**Example: Automatic citation verification on push**

`.github/workflows/verify-citations.yml`:
```yaml
name: Verify Citations

on:
  push:
    paths:
      - '07_DRAFTS_AND_WORK_PRODUCT/**/*.md'
      - '02_PLEADINGS/**/*.md'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install wpd
        run: |
          pip install -e .

      - name: Verify citations in changed files
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          COURTLISTENER_TOKEN: ${{ secrets.COURTLISTENER_TOKEN }}
        run: |
          wpd-find-citations 07_DRAFTS_AND_WORK_PRODUCT/drafts/*.md | \
          xargs -I {} wpd-verify-citation "{}"
```

**Use cases:**
- Auto-verify citations on every draft push
- Run self-review on pull requests
- Check formatting compliance
- Alert on missing deadlines

## Email Integration

### Pattern: Process Legal Correspondence Automatically

**Workflow:**

1. **Forward important emails to case folder:**
   - Save .eml files to `00_NEW_DOCUMENTS_INBOX/`
   - Or use email → folder automation (Zapier, IFTTT, etc.)

2. **Run organize agent:**
   ```
   /organize
   ```

3. **Claude processes emails:**
   - Reads sender, subject, body
   - Extracts attachments
   - Classifies (correspondence vs. discovery vs. court filing)
   - Moves to appropriate directory
   - Updates case timeline if important event

**Supported patterns:**
- Extract PDF attachments from emails
- Parse court e-filing notifications
- Track opposing counsel communications
- Log deadline notices

## Case Management Software Integration

### Pattern: Export to WePublicDefender from Other Tools

**From Clio, MyCase, etc.:**

1. Export case documents as PDF
2. Save to `00_NEW_DOCUMENTS_INBOX/`
3. Run `/organize` to classify and file
4. Run `/timeline` to sync timeline with case events

**From WePublicDefender to other tools:**

1. Generate timeline report:
   ```
   /timeline export
   ```

2. Export costs/usage:
   ```
   wpd-usage-summary --format csv > case_costs.csv
   ```

3. Import to case management system

## Cloud Storage Integration

### Pattern: Sync Case Files with Dropbox/Google Drive

**Why:**
- Backup case files automatically
- Access from multiple devices
- Share with co-counsel

**Setup:**

1. **Initialize case in synced folder:**
   ```bash
   cd ~/Dropbox/Cases/CapitalOne_v_Neil
   wpd-init-case
   ```

2. **All work is now automatically synced:**
   - Drafts in `07_DRAFTS_AND_WORK_PRODUCT/`
   - Research in `06_RESEARCH/`
   - GAMEPLAN.md
   - Case timeline

**Best practices:**
- Use selective sync for large evidence files
- Don't sync `.database/` (gitignored for good reason)
- Encrypt sensitive files before cloud sync

## Custom Agent Integration

### Pattern: Extend WePublicDefender with Custom Agents

**Create custom agent:**

1. **Add agent prompt:** `.claude/workflows/custom_agent.md`

2. **Define agent config:** Update `legal_review_settings.json`
   ```json
   {
     "reviewAgentConfig": {
       "custom_agent": {
         "models": ["gpt-5"],
         "temperature": 0.2,
         "web_search": true
       }
     }
   }
   ```

3. **Run custom agent:**
   ```bash
   wpd-run-agent --agent custom --file input.md --mode external-llm
   ```

**Example custom agents:**
- **Deposition prep agent** - Analyzes transcripts, suggests questions
- **Settlement calculator** - Evaluates settlement offers
- **Jury instructions agent** - Drafts jury instructions
- **Discovery analyzer** - Processes large discovery productions

## API Integration (Future)

### Pattern: Expose WePublicDefender as REST API

**Planned feature** (not yet implemented):

```python
# Start WePublicDefender API server
wpd-api-server --port 8000

# Use from other applications
import requests

response = requests.post(
    "http://localhost:8000/api/review",
    json={
        "agent": "self_review",
        "file_content": motion_text,
        "mode": "external-llm"
    }
)

results = response.json()
```

**Use cases:**
- Integrate with custom legal tech tools
- Build web interface for WePublicDefender
- Automate bulk document reviews
- Create specialized workflows

## Summary: Integration Best Practices

1. **Use Claude Code as primary interface** - it orchestrates everything
2. **Offload heavy research to Claude.ai** - Deep Research mode is powerful
3. **Leverage external LLMs for adversarial review** - different perspectives catch more issues
4. **Cache citations to reduce API calls** - CITATIONS_LOG.md is your friend
5. **Sync with cloud storage for backup** - don't lose case files
6. **Version control with git** - track document evolution
7. **Automate repetitive tasks** - GitHub Actions for quality checks
8. **Extend with custom agents** - tailor to your specific workflows

**The goal:** WePublicDefender fits into your existing workflow, doesn't replace it.

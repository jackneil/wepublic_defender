# Quick Command Reference

You don't need to memorize these. Just ask Claude in plain English. But these slash commands do specific things if you want to be precise.

## Getting Started

### `/check-env`
**What it does:** Checks if Python, API keys, and packages are set up correctly
**When to use:** First thing if you get errors, or if something seems broken
**Example:**
```
/check-env
```

### `/organize`
**What it does:** Moves files from your inbox into the right folders
**When to use:** After adding new PDFs, court documents, or evidence to `00_NEW_DOCUMENTS_INBOX/`
**Example:**
```
/organize
```

## Understanding Modes (Free vs Paid)

**Most commands work in TWO ways:**

### Guidance Mode (FREE - Default)
Claude Code does the work with help from structured prompts. No external AI calls = $0.00 cost.

**Examples:**
```
/draft motion to dismiss
/research summary judgment standards
/strategy
```

These return guidance that Claude Code uses to help you. Free.

### External-LLM Mode (COSTS MONEY)
Calls external LLMs (GPT-5, Grok 4) to validate or automate the work. Costs tokens.

**When to use:**
- Critical filings that need extra validation
- Want automated second opinion
- Citation verification with web search

**How to use:**
Add `--mode external-llm` to any command (requires using full command syntax):

```bash
python <path>/python.exe -m wepublic_defender.cli.run_agent --agent self_review --file draft.md --mode external-llm
```

**Cost depends on:**
- Document size (more text = more tokens)
- Number of models (1 or 2 in parallel)
- Web search enabled (costs extra)

**Special case:** `/organize` is ALWAYS free (guidance only) because it needs Claude Code's file access.

## Research

### `/deep-research-prep`
**What it does:** Creates a research assignment for Claude.ai Deep Research mode
**When to use:**
- Starting a new case (need to assess viability, claims, damages, venue)
- Before major filings (need comprehensive research on legal standards)
- Need to dig deep into case law and statutes (more than simple web search)

**How it works:**
1. You type `/deep-research-prep`
2. Claude Code generates a comprehensive prompt
3. You copy the prompt to Claude.ai (https://claude.ai)
4. Enable Deep Research mode and paste
5. Wait 5-10 minutes for Claude.ai to do extensive web research
6. Copy results and paste back to Claude Code
7. Claude Code organizes results into your case files

**Example:**
```
/deep-research-prep

# Or focus on specific topic:
/deep-research-prep --focus "summary judgment standards for breach of contract"
```

### `/research [topic]`
**What it does:** Quick legal research using web search (lighter than deep research)
**When to use:** Need quick answers on specific legal questions
**Example:**
```
/research statute of limitations for fraud in South Carolina

/research Fourth Circuit standard for granting TRO
```

## Strategy

### `/strategy`
**What it does:** Analyzes your case and recommends next steps
**When to use:**
- Need to figure out what to do next
- Feeling overwhelmed or stuck
- Want strategic guidance on timing and priorities

**Example:**
```
/strategy
```

## Writing

### `/draft [document type]`
**What it does:** Drafts a legal document with proper format and citations
**When to use:** Need to write a motion, response, brief, or other court filing
**Example:**
```
/draft motion to dismiss

/draft response to summary judgment

/draft discovery requests
```

### `/review [file]`
**What it does:** Runs multiple AI models to review your document before filing
**When to use:** Before filing anything with the court (catches errors, weak arguments, bad citations)
**Example:**
```
/review 07_DRAFTS_AND_WORK_PRODUCT/motion_to_dismiss.md
```

### `wpd-convert-to-word`
**What it does:** Converts markdown legal documents to properly formatted Word documents for court filing
**When to use:** When you're ready to convert your drafted markdown document to a Word document with perfect court formatting
**Features:**
- Perfect case caption with aligned brackets
- Automatic court header formatting
- Federal court compliant (Times New Roman 12pt, double-spaced, 1" margins)
- Loads case details from `.wepublic_defender/case_config.json`
- Supports command-line overrides for quick changes

**Examples:**
```bash
# Basic conversion (uses case_config.json settings)
wpd-convert-to-word --file motion.md

# Specify output file
wpd-convert-to-word --file brief.md --output final_brief.docx

# Override case number
wpd-convert-to-word --file motion.md --case-number "3:25-cv-12345-MGL"

# Override parties
wpd-convert-to-word --file motion.md --plaintiff "John Doe" --defendant "ABC Corp"

# Preview configuration without converting
wpd-convert-to-word --preview-config
```

**Configuration:**
Update `.wepublic_defender/case_config.json` with your case details:
- Court name and district
- Party names and labels (Plaintiff/Defendant, Petitioner/Respondent)
- Case number
- Formatting preferences

---

## Don't Like Commands?

Just talk to Claude in plain English:

- "I need to figure out if I have a case against my bank"
- "Can you help me organize these documents?"
- "I need to draft a response to their motion for summary judgment"
- "What should I do next in my case?"

Claude will figure out what command to run (or just do it without commands).

---

## Need Help?

- **Environment issues?** → `/check-env`
- **Files messy?** → `/organize`
- **Don't know what to do?** → `/strategy`
- **Need research?** → `/deep-research-prep` (heavy) or `/research [topic]` (quick)
- **Need to write something?** → `/draft [type]`
- **Ready to file?** → `/review [file]` first!

Still stuck? Just ask Claude: "I'm stuck, what should I do?"

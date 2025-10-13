# Legal Case Management - Claude Code Orchestrator

**You are assisting with a legal case using the wepublic_defender system.**

This file provides core configuration and conditional logic to load the appropriate workflow for each situation.

---

## ⚙️ Workflow Routing (READ FIRST EVERY SESSION)

**Follow this conditional logic to determine which workflow to load:**

### 1. Check for First-Time Initialization

**IF** `.wepublic_defender/case_initialized.json` does **NOT** exist in current working directory:
```
→ Read and follow: `.claude/workflows/first_case_init.md`
→ After completion, that workflow creates the case_initialized.json file
→ This only happens once per case directory
```

### 2. Detect Post-Compacting Recovery

**IF** conversation summary indicates context was recently compacted/summarized:
```
→ Read and follow: `.claude/workflows/post_compact_recovery.md`
→ This helps you rebuild context from files without annoying user
→ Then proceed to normal session workflow
```

### 3. Normal Session Start

**IF** case is initialized and context is intact:
```
→ Read and follow: `.claude/workflows/session_start_checklist.md`
→ This checks inbox, deadlines, and offers relevant next actions
```

### 4. User Requests Legal Document Work

**IF** user wants to draft, review, or file legal documents:
```
→ Read and follow: `.claude/workflows/legal_document_workflow.md`
→ **CRITICAL**: This contains the mandatory POST-REVIEW DECISION POINT
→ **ALWAYS** follow `.claude/protocols/LEGAL_WORK_PROTOCOL.md` for quality standards
```

---

## 🔄 Session Management

**Refresh instructions periodically**: Every 10-15 interactions during long sessions, re-read this file to refresh routing logic.

**Multi-Model Cost Awareness**: When agent configs have multiple models (e.g., `["gpt-5", "grok-4"]`), wepublic_defender runs ALL models in parallel for adversarial redundancy. This means **2x token usage and cost**.

Periodically remind user:
- "Running both {model1} and {model2} in parallel for redundancy (doubles cost)"
- Suggest checking `.wepublic_defender/usage_log.csv` or running `wpd-usage-summary`

To run single model: Use `--model <model_name>` flag.

---

## 🎯 Agent Mode Architecture (CRITICAL)

**ALL agents support TWO operating modes:**

### Mode 1: Guidance (DEFAULT - FREE)
- Returns structured prompt for Claude Code to execute
- **NO API calls** - completely free, no token usage
- Claude Code does all the work based on the guidance prompt
- Default mode to minimize costs

**When to use:**
- Most of the time (this is the default)
- When you want to review/draft/research yourself with guidance
- For file organization (organize agent ONLY supports this mode)

**Example:**
```bash
<python_path> -m wepublic_defender.cli.run_agent --agent drafter --text "Draft motion" --mode guidance
# Returns: Guidance prompt
# Cost: $0.00
```

### Mode 2: External-LLM (COSTS MONEY)
- Calls external LLM(s) configured in `.wepublic_defender/legal_review_settings.json`
- Number of models depends on agent configuration:
  - `"models": ["gpt-5"]` → calls ONE model
  - `"models": ["gpt-5", "grok-4"]` → calls BOTH in parallel (2x cost)
- Override with `--model <name>` flag or `--run-both` to force both

**When to use:**
- Automated validation from external LLMs
- Second opinions on critical filings
- Citation verification with web search
- Adversarial review (opposing counsel simulation)

**Example:**
```bash
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file draft.md --mode external-llm
# Calls LLM(s) from settings
# Cost: Depends on document size, models, web search
```

### Special Case: Organize Agent

`organize` agent **ONLY** operates in guidance mode - external LLMs cannot access file system.

If you try `--mode external-llm` with organize, it auto-falls back to guidance with warning.

---

## 💻 OS Detection (FIRST THING EVERY SESSION)

Check `<env>` tag for platform and remember for entire session:

**Windows (win32)**:
- Edit/MultiEdit file_path: MUST use backslashes `\` (e.g., `C:\\repos\\file.txt`)
- Bash commands: Use forward slashes `/` (e.g., `"C:/repos/file.txt"`)
- Shell commands: `copy`, `move`, `del`, `dir`

**Mac/Linux (darwin/linux)**:
- All paths: forward slashes `/`
- Shell commands: `cp`, `mv`, `rm`, `ls`

---

## 🐍 Python Environment (MANDATORY)

**On first Python command each session**: Determine absolute Python path for wepublic_defender environment.

### Environment Path Source (Case-Aware)

1. Check for `.wepublic_defender/env_info.json` in current case directory
2. If exists, load `python_exe` path from it
3. If missing, detect path and create the file:
   ```bash
   conda run -n wepublic_defender python -c "import sys; print(sys.executable)"
   ```
4. Save to `.wepublic_defender/env_info.json`:
   ```json
   {
     "python_exe": "C:/Users/you/.conda/envs/wepublic_defender/python.exe",
     "conda_env": "wepublic_defender",
     "repo_path": "C:/path/to/wepublic_defender"
   }
   ```

**NEVER** use bare `python` or `python3` - always use full explicit path with `-m` flag.

---

## 📁 Directory Structure

Standard directory structure (maintained by `/organize` command):

- `00_NEW_DOCUMENTS_INBOX/` - Staging area for new files
- `01_CASE_OVERVIEW/` - Case summary, timeline, parties
- `02_PLEADINGS/` - All court filings
- `03_DISCOVERY/` - Discovery requests/responses
- `04_EVIDENCE/` - Evidence documents
- `05_CORRESPONDENCE/` - Letters and communications
- `06_RESEARCH/` - Legal research and case law
- `07_DRAFTS_AND_WORK_PRODUCT/` - Working documents
- `08_REFERENCE/` - Court rules, forms, templates

**ALWAYS** maintain this organization throughout session.

---

## 🛠️ Available Commands

### Core Commands

- **`/check-env`** - Check Python environment and API keys
- **`/organize`** - Organize files from inbox (guidance-only, always free)
- **`/deep-research-prep`** - Generate comprehensive prompt for Claude.ai Deep Research
- **`/research [topic]`** - Quick legal research on specific topic
- **`/strategy`** - Get strategic recommendations
- **`/draft [type]`** - Draft legal document
- **`/review [file]`** - Run adversarial review

See `.claude/COMMANDS_REFERENCE.md` for detailed command documentation.

---

## 🔧 wepublic_defender CLI Usage

### Basic Invocation

Use full Python path from env_info.json:

```bash
# Environment check
<python_path> -m wepublic_defender.cli.check_env

# Initialize case (if not already done)
<python_path> -m wepublic_defender.cli.init_case

# Run agent (guidance mode - free)
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file draft.md --mode guidance

# Run agent (external-llm mode - costs money)
<python_path> -m wepublic_defender.cli.run_agent --agent citation_verify --file draft.md --mode external-llm --web-search
```

### Multi-Model Behavior

If agent has 2+ models configured, **ALL run in parallel** by default (adversarial redundancy, 2x cost).

Override:
```bash
# Force single model
--model gpt-5

# Force both models
--run-both
```

---

## 📝 File Naming Conventions

- Use UPPERCASE for document types: `MOTION_TO_DISMISS.docx`
- Include dates for versions: `MOTION_TO_DISMISS_2025-10-15.docx`
- Use underscores, not spaces: `DISCOVERY_RESPONSE_01.docx`
- Use version numbers for drafts: `MOTION_v1.md`, `MOTION_v2.md`, `MOTION_FINAL.md`

---

## 💾 State Tracking (.database)

Claude manages lightweight state directly:

**Ledger**: `.database/organization_log.md`
- Format: `timestamp | action | src | dst | notes`
- Append one line per file management action

**Index**: `.database/organization_index.json`
- JSON object keyed by path
- Tracks what's been processed to avoid duplicate work

Read index before organizing to skip already-processed files/folders.

---

## 🔍 Citation Verification

### CourtListener Setup (If Missing)

If `COURTLISTENER_TOKEN` not in `.env`:
1. Open https://www.courtlistener.com/api/
2. Create API token (free account)
3. Add to `.env`:
   ```
   COURTLISTENER_TOKEN=your_token_here
   COURTLISTENER_USER_AGENT=WePublicDefender/0.1
   ```

### Citation Caching Protocol

1. Before verifying citation, check `06_RESEARCH/CITATIONS_LOG.md`
2. If case recently verified for same proposition, skip recheck (unless context changed)
3. After verification, update `CITATIONS_LOG.md` with:
   - Good law status
   - Holding
   - Key quotes + pin cites
   - Propositions supported
   - Sections it applies to

**Prefer South Carolina and Fourth Circuit authority when relevant. Always include pin cites.**

---

## ⚖️ Quality Standards

**ALWAYS follow `.claude/protocols/LEGAL_WORK_PROTOCOL.md`** for quality standards.

Critical principles:
- Research extensively BEFORE drafting (never draft without research)
- ALWAYS run adversarial review before filing
- Analyze LLM feedback critically against research (don't blindly accept)
- Triple-check all citations
- Track API costs and report after expensive operations

---

## 💰 Cost Management

- Monitor token usage throughout session
- Provide cost summary after major tasks
- Check `.wepublic_defender/usage_log.csv` regularly
- Alert if costs exceed $10 for single operation
- Default to guidance mode (free) unless user specifically requests external-llm

---

## 📋 Logging and Debugging

- All agent runs log to `.wepublic_defender/logs/wpd.log`
- Include log path when reporting issues
- Check log for model selections, parse results, citation updates

---

## ⚠️ CRITICAL: File Editing on Windows

**When using Edit/MultiEdit on Windows, MUST use backslashes `\` in file paths:**

❌ WRONG: `file_path: "D:/repos/file.txt"` (will error)

✅ CORRECT: `file_path: "D:\\repos\\file.txt"` (works)

Bash commands use forward slashes `/`, but Edit tool requires backslashes on Windows.

---

## 🔗 Workflow Integration

This orchestrator file is **lightweight and focused on routing**. Detailed workflows are in separate files:

- **First time setup**: `.claude/workflows/first_case_init.md`
- **Session start**: `.claude/workflows/session_start_checklist.md`
- **Post-compacting**: `.claude/workflows/post_compact_recovery.md`
- **Legal documents**: `.claude/workflows/legal_document_workflow.md`
- **Quality standards**: `.claude/protocols/LEGAL_WORK_PROTOCOL.md`

**Always start by checking the routing logic at the top of this file to determine which workflow to follow.**

---

## ⚠️ Important Reminders

- This is federal court litigation - mistakes have consequences
- Always verify citations before filing
- Human lawyer must review and sign all filings
- AI is an assistant, not an attorney
- When in doubt, ask the user

---

**Now execute the workflow routing logic at the top of this file to determine your next action.**

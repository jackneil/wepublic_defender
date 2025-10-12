# Legal Case Management Instructions with wepublic_defender

You are assisting with a legal case using the wepublic_defender system for final review. Follow these protocols:

## Session Management (IMPORTANT)

**Refresh instructions periodically**: Every 10-15 interactions during long sessions, re-read this file to refresh guidance. This prevents instruction drift in extended conversations.

**Multi-Model Cost Awareness**: When agent configs have multiple models (e.g., `["gpt-5-mini", "grok-4-fast"]`), wepublic_defender automatically runs ALL models in parallel for adversarial redundancy. This means **2x token usage and cost**.

During processing, periodically remind the user:
- "Running both {model1} and {model2} in parallel for redundancy (doubles cost)"
- Suggest checking `.wepublic_defender/usage_log.csv` or running `wpd-usage-summary` to track costs

To override and run a single model: Use `--model` flag to specify which one.

## OS Detection (FIRST THING EVERY SESSION)

**At session start (or after context compaction)**: Check `<env>` tag for platform (win32=Windows, darwin=Mac, linux=Linux). Remember for entire session:

**Windows (win32)**:
- Edit/MultiEdit file_path: MUST use backslashes `\` (e.g., `C:\\repos\\file.txt`) - forward slashes cause errors
- Bash commands: Use forward slashes `/` (e.g., `"C:/repos/file.txt"`) - more portable
- Shell commands: `copy`, `move`, `del`, `dir`

**Mac/Linux (darwin/linux)**:
- All paths: forward slashes `/`
- Shell commands: `cp`, `mv`, `rm`, `ls`

## Python Environment (MANDATORY)

**On first Python command each session**: Determine the absolute Python path for your wepublic_defender environment. Save this path and use it for ALL Python commands in the session.

To get the path: `conda run -n wepublic_defender python -c "import sys; print(sys.executable)"`

Example result: `C:/Users/you/miniconda3/envs/wepublic_defender/python.exe`

NEVER use bare `python` or `python3` - always use the full explicit path with `-m` flag.

### Environment Path Source (Case-Aware)

- First, look for `.wepublic_defender/env_info.json` in the current case folder.
  - If present, load and use:
    - `python_exe`: absolute path to the environment’s Python
    - `conda_env`: environment name (if applicable)
    - `repo_path`: absolute path to the central wepublic_defender repo clone
  - Validate `python_exe` exists. If missing or invalid, re-detect the path and refresh the JSON.
- If the file does not exist, detect `python_exe` as above, then create `.wepublic_defender/env_info.json` with the discovered values. Do not ask the user to copy/paste paths.
- Always use `python_exe` from this file for all subsequent `-m wepublic_defender...` calls in this session.

## Environment Check (CRITICAL - Check on First Interaction)

**Before doing any work, verify the Python environment is properly configured:**

1. **Run environment check**: Always run commands from the case root. Run `<python_path> -m wepublic_defender.cli.check_env` from the case root
2. **Check Python**: Verify Python 3.9+
3. **Check environment**: Ensure in dedicated conda/venv (not base/global)
4. **Check wepublic_defender**: If already installed, do NOT reinstall
5. **Check packages**: Ensure openai, pydantic>=2.0, python-docx, PyPDF2 installed
6. **Check API keys**: Verify OPENAI_API_KEY and XAI_API_KEY are set

**If environment issues detected:**
- Warn user about missing packages or incorrect environment
- Recommend creating dedicated environment (see setup section below)
- DO NOT proceed with AI-powered operations if environment is broken

Interaction style for non-technical users
- Do not ask users to run commands. Ask what they want to do in plain language, then execute the necessary commands yourself.
- Summarize what you did, show where outputs/logs are, and provide a brief cost/usage summary.

### First Run: Environment Setup (If needed)

If Python/Conda environment is missing or broken:

1. **Create environment**
   - Conda: `conda create -n wepublic_defender python=3.11 -y`
   - Or venv: `python -m venv wepublic_defender_env`

2. **Get absolute Python path** (save this for all commands):
   - Conda: `conda run -n wepublic_defender python -c "import sys; print(sys.executable)"`
   - Or venv: Find `python.exe` in venv's `Scripts/` (Windows) or `bin/` (Unix)
   - Example: `C:/Users/you/miniconda3/envs/wepublic_defender/python.exe`

3. **Install wepublic_defender**:
   ```
   <python_path> -m pip install -e C:/path/to/wepublic_defender
   ```

4. **Verify**:
   ```
   <python_path> -m wepublic_defender.cli.check_env
   ```

Note: Always use forward slashes `/` in Bash command paths, even on Windows.

## Directory Structure
This case uses a standardized directory structure. ALWAYS maintain this organization.

### File Organization Rules
1. New documents go to `00_NEW_DOCUMENTS_INBOX/` first
2. **On first interaction, check inbox and offer to run /organize if files present**
3. Throughout session, keep files in proper directories
4. Never leave files in wrong locations
5. Use `/organize` command to organize files - it handles:
   - Reading document contents to categorize properly
   - Finding and moving related drafts with finalized documents
   - Consolidating non-standard folders into standard structure
   - Smart file renaming for meaningful names
   - State tracking to avoid duplicate work

### Directory Purposes
- `00_NEW_DOCUMENTS_INBOX/`: Staging area for new files
- `01_CASE_OVERVIEW/`: Case summary, timeline, parties
- `02_PLEADINGS/`: All court filings (complaints, motions, orders)
- `03_DISCOVERY/`: Discovery requests, responses, depositions
- `04_EVIDENCE/`: Evidence documents and exhibits
- `05_CORRESPONDENCE/`: Letters and communications
- `06_RESEARCH/`: Legal research and case law
- `07_DRAFTS_AND_WORK_PRODUCT/`: Working documents and scripts
- `08_REFERENCE/`: Court rules, forms, templates

## Available Commands

### /organize
Organize files from 00_NEW_DOCUMENTS_INBOX/ into proper directories

### /review [file]
Run wepublic_defender adversarial review on a legal document

### /research [topic]
Perform legal research using web search

### /strategy
Generate case strategy recommendations

### /draft [document_type]
Draft a legal document with AI assistance

### Make My Pleading Strong (Claude-Orchestrated Review)

**IMPORTANT: Claude orchestrates the review workflow by calling individual agents step-by-step.**

DO NOT use `wpd-review-pipeline` directly. The full pipeline command exists for convenience/automation, but Claude should manage the workflow by:
1. Calling each agent independently via `wpd-run-agent`
2. Processing results between steps
3. Deciding next actions based on findings
4. Some agents may return prompts for Claude to execute (not perform work themselves)

#### Typical Review Workflow:

After drafting (or when reviewing a draft in 07_DRAFTS_AND_WORK_PRODUCT/), run targeted checks:

```bash
# 1. Self review - legal sufficiency, clarity
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md --verbose

# 2. Citation verification - confirm authorities are good law
<python_path> -m wepublic_defender.cli.run_agent --agent citation_verify --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md --web-search --verbose

# 3. Opposing counsel - adversarial attack on arguments
<python_path> -m wepublic_defender.cli.run_agent --agent opposing_counsel --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md --web-search --verbose

# 4. Final review - pre-filing compliance check
<python_path> -m wepublic_defender.cli.run_agent --agent final_review --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md --verbose
```

#### Between Each Step:

- **Examine results**: Check structured JSON output for critical/major issues
- **Process findings**: Decide if revision needed or can proceed
- **Run drafter if needed**: Use `--agent drafter` to refine based on issues found
- **Re-run checks**: After revision, rerun affected agents to verify fixes
- **Iterate**: Repeat until critical=0, major<=2 (or user-defined threshold)

#### Advanced Pipeline (Optional):

For automated iteration, `wpd-review-pipeline` exists but is primarily for batch processing:

```bash
<python_path> -m wepublic_defender.cli.review_pipeline --file draft.md --plan-only
```

This shows the command sequence Claude should execute manually. Claude can run it for reference but should still orchestrate independently.

### CourtListener Setup (If missing token)
If CourtListener token is missing, prompt the user to create one and save it:

1. Open https://www.courtlistener.com/api/ and create an API token (free account).
2. Add to case `.env` (Claude can do this):
```
COURTLISTENER_TOKEN=your_token_here
COURTLISTENER_USER_AGENT=WePublicDefender/0.1 (+your_email_or_url)
```
3. Re-run `<python_path> -m wepublic_defender.cli.check_env` and proceed.

### Finding and Verifying Citations
Use retrieval first, then LLM for verification.

1) Find candidate cites for propositions:
```
<python_path> -m wepublic_defender.cli.find_citations --props-file 06_RESEARCH/propositions.json --verbose --heartbeat 10
```
Outputs:
- 06_RESEARCH/citation_candidates.json (raw JSON)
- 06_RESEARCH/citation_candidates.md (summary with links)

2) Verify citations in a draft:
```
<python_path> -m wepublic_defender.cli.verify_citation --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md --verbose --heartbeat 10
```
Behavior:
- Resolves citations via CourtListener (by citation string)
- Uses the `citation_verify` agent to produce structured verification (good law, supports_position, quotes + pin cites)
- Upserts results into `06_RESEARCH/CITATIONS_LOG.md` so future runs skip rechecking

## Critical Workflow Sequence

**IMPORTANT: Follow this exact workflow for all legal work:**

1. **Organize & Assess** - Keep directory structure organized, understand case status
2. **Research Extensively** - Perform thorough web search on legal issues, case law, procedural requirements
3. **Draft Documents** - Create initial drafts based on research and strategy
4. **Invoke wepublic_defender** - Use the library for final adversarial review and refinement

**DO NOT skip the adversarial review step.** The wepublic_defender library is specifically designed to double and triple check work products before filing through:
- Multi-AI adversarial review (GPT-5 + Grok 4)
- Opposing counsel simulation to find weaknesses
- Citation verification with web search
- Iterative refinement until consensus reached

## Mandatory Protocols

### Before Any Legal Work
1. Check LEGAL_WORK_PROTOCOL.md for quality standards
2. Review GAMEPLAN.md for case strategy
3. Understand current case status from 01_CASE_OVERVIEW/

### When Creating Legal Documents
1. Research extensively with web search first
2. Draft initial document based on research
3. Save draft to 07_DRAFTS_AND_WORK_PRODUCT/
4. Invoke wepublic_defender for adversarial review
5. Refine based on feedback
6. Repeat review until consensus reached
7. Follow LEGAL_WORK_PROTOCOL.md standards throughout
8. Report costs after major operations
9. Move final approved version to appropriate directory

### File Naming Conventions
- Use UPPERCASE for document types: `MOTION_TO_DISMISS.docx`
- Include dates for versions: `MOTION_TO_DISMISS_2025-10-15.docx`
- Use underscores, not spaces: `DISCOVERY_RESPONSE_01.docx`

## wepublic_defender Library Usage

### Invocation (Claude: how to call checks)

Use these concrete commands to invoke wepublic_defender from the case root:

Shell/CLI (using full Python path from session start):
```
<python_path> -m wepublic_defender.cli.check_env
<python_path> -m wepublic_defender.cli.init_case
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md
<python_path> -m wepublic_defender.cli.run_agent --agent citation_verify --file 06_RESEARCH/citations.md --web-search
<python_path> -m wepublic_defender.cli.run_agent --agent opposing_counsel --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md
```
Note: `<python_path>` is the full path determined at session start (e.g., `C:/Users/jack/.conda/envs/wepublic_defender/python.exe`).

Python (for programmatic use):
```python
from wepublic_defender import WePublicDefender

wpd = WePublicDefender()
text = Path("07_DRAFTS_AND_WORK_PRODUCT/draft.md").read_text(encoding="utf-8")
result = await wpd.call_agent("self_review", text)
print(result.get("text", ""))
```

Important: wepublic_defender provides single-purpose checks and cost tracking. Claude is the orchestrator: decide based on results whether to refine, research more, run opposing counsel, or proceed.

### Batch Citation Verification (Claude extracts, Defender verifies)

1. Extract citations from the document you’re reviewing. For each citation, capture:
   - citation (full Bluebook)
   - case_name (if available)
   - argument (the proposition we cited this case for)
   - context_snippet (1–2 sentences from our draft around the cite)
   - applies_to_sections (e.g., ["COUNT II – Negligence"]) 

2. De-duplicate against `06_RESEARCH/CITATIONS_LOG.md`. If an entry was verified recently and clearly supports the same proposition, skip unless the user requests recheck or context changed.

3. Save the batch as JSON to `06_RESEARCH/batch_citations.json`. See example in `wepublic_defender/config/batch_citations.example.json`.

4. Run Defender citation verification (batch):
```
<python_path> -m wepublic_defender.cli.run_agent \
  --agent citation_verify \
  --file 06_RESEARCH/batch_citations.json \
  --web-search \
  --run-both
```

### Using a Central WePublicDefender Clone (Multiple Cases)

If the repository is cloned elsewhere (not inside the case folder):

1. Install it once into the environment:
```
<python_path> -m pip install -e C:/path/to/wepublic_defender
```

2. From each case root, use the same commands:
```
<python_path> -m wepublic_defender.cli.check_env
<python_path> -m wepublic_defender.cli.init_case
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file 07_DRAFTS_AND_WORK_PRODUCT/draft.md
```

5. Defender returns structured JSON and updates `06_RESEARCH/CITATIONS_LOG.md` automatically.

6. Use results to revise the draft: keep supporting cites; replace/remove those that don’t; add key quotes + pin cites; note contrary authority.

## Decision Points & Questions (Claude must ask)

When invoking tools, confirm these with the user unless already specified in GAMEPLAN.md:
- **Multi-model runs**: When agent has 2+ models configured, both run automatically in parallel for adversarial redundancy (2x cost). To run single model, use `--model` flag.
- Web search: "Allow web search for this check? Any source/budget limits?" (Default: allow for citation verification and opposing counsel.)
- Cost/time: "Service tier (auto/flex/standard/priority)? Any budget ceiling for this run?" (Default: auto.)
- Effort: "Use high reasoning effort?" (Default: depends on agent config.)
- Outputs: "Where should I save results (e.g., 06_RESEARCH/, 07_DRAFTS_AND_WORK_PRODUCT/)?"

If user defers, apply defaults above and proceed.

**Cost Awareness Reminders**:
- First time multi-model runs in a session: "Note: Running {N} models in parallel ({models}) - this doubles/triples token costs for adversarial redundancy."
- Periodically (every 3-4 agent calls): "Current session costs: [check usage_log.csv or run wpd-usage-summary]"
- Before expensive operations (large documents, web search): "This will use ~X tokens across Y models. Proceed?"

### Reading and Updating Preferences

- Read per-agent candidates from per‑case settings: `.wepublic_defender/legal_review_settings.json` under `reviewAgentConfig` (key names: `strategy_agent`, `self_review_agent`, etc.). Treat these as tool‑level settings.
- Use `models` list (ordered) and `effort` to plan runs. If the user picks a different model/effort and wants it remembered, persist it by running:

```
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --model grok-4 --effort high --save-choice
```

This will update `.wepublic_defender/legal_review_settings.json` so future runs prefer that choice.

Notes:
- `workflowConfig.default_effort` is a fallback only. Per‑agent `effort` overrides it. If the user wants the fallback to apply everywhere, remove per‑agent `effort` keys or overwrite them.
- On load, Defender merges packaged defaults into per‑case settings (case wins) to keep new keys without losing user preferences.

## Typical Toolbox Workflow (Claude)

1) First run
- If CLAUDE.md not in root, run `<python_path> -m wepublic_defender.cli.init_case`
- Run env check: `<python_path> -m wepublic_defender.cli.check_env`
- Offer to organize `00_NEW_DOCUMENTS_INBOX/`
- Read GAMEPLAN.md and 01_CASE_OVERVIEW/* to learn context

2) Research-then-draft
- Perform web research on core issues; save to `06_RESEARCH/` as markdown
- Draft in `07_DRAFTS_AND_WORK_PRODUCT/`

3) Targeted checks (run as needed)
- Self review on draft: clarity, legal sufficiency
- Citation verify: confirm all authorities are good law (with web search)
- Opposing counsel: adversarial attack on arguments (with web search)

4) Iterate and refine
- Address issues, rerun targeted checks
- For critical filings, ask to run both providers before finalizing

5) Finalize
- Convert to Word if needed using the converter
- Update GAMEPLAN.md with status/next steps

### Initialize System
```python
from wepublic_defender import WePublicDefender

# Initialize with config files from package
defender = WePublicDefender()
```

### Run Adversarial Review on Draft Document
```python
# After you've done extensive research and created a draft,
# use wepublic_defender for final adversarial review
result = await defender.review_document(
    document_path="07_DRAFTS_AND_WORK_PRODUCT/MOTION_FOR_SUMMARY_JUDGMENT.docx",
    document_type="Motion for Summary Judgment",
    max_iterations=3
)

# Check if document is ready to file
if result['ready_to_file']:
    print("Document passed adversarial review - ready for filing")
else:
    print("Issues found - refinement needed")
```

### Get Cost Report
```python
# Always report costs after expensive operations
print(defender.get_cost_report())
print(defender.get_detailed_cost_report())
```

## Quality Standards
- Follow LEGAL_WORK_PROTOCOL.md ALWAYS
- Do extensive web search research BEFORE drafting
- Triple-check all citations using wepublic_defender
- ALWAYS run adversarial review before filing (use wepublic_defender)
- Never skip the multi-AI review step
- Track all API costs and report after expensive operations

## Cost Management
- Monitor token usage throughout session
- Provide cost summary at end of major tasks
- Use Grok 4 Fast for cost-sensitive operations
- Alert if costs exceed $10 for single operation

## Session Workflow

### On First Interaction
1. Check if 00_NEW_DOCUMENTS_INBOX/ has files
2. If yes, offer: "I see X files in the inbox. Would you like me to organize them?"
3. Read GAMEPLAN.md to understand current case status
4. Offer to help with next action items

### When Working on Legal Documents (Standard Workflow)
1. **Organize** - Ensure all files are in proper directories
2. **Research** - Perform extensive web search on relevant legal issues
3. **Draft** - Create initial document draft in 07_DRAFTS_AND_WORK_PRODUCT/
4. **Review** - Invoke wepublic_defender for adversarial multi-AI review
5. **POST-REVIEW DECISION POINT** - **CRITICAL: DO NOT SKIP THIS STEP**
   - **When LLMs identify concerns/weaknesses, DO NOT immediately accept or reject them**
   - **MANDATORY WORKFLOW AFTER RECEIVING LLM FEEDBACK:**
     1. **Read ALL review outputs** from `.wepublic_defender/reviews/*.json`
     2. **If concerns require research:** Conduct research and save to `06_RESEARCH/`
     3. **After research complete, STOP and perform critical analysis:**
        - **ALWAYS prompt user:** "Research complete. Let's review the LLM feedback against our new findings before deciding what changes to make."
        - Read each LLM review output (.wepublic_defender/reviews/*.json files)
        - For each concern raised by LLMs, compare against research findings:
          * Was the LLM concern valid? (research confirmed the weakness)
          * Was the LLM concern invalid? (research showed our original approach was correct)
          * Is there a middle ground? (LLM had a point, but research suggests different fix)
        - Document your reasoning for each decision in a summary
        - Present findings to user: "Based on research, here's my analysis of the LLM feedback: [summary of each concern and whether research supports/contradicts it]"
     4. **Make informed decisions about what to change:**
        - Changes to implement (LLM was right + research supports)
        - Original approach to keep (LLM concern not supported by research)
        - Alternative approaches (research suggests better solution than either draft or LLM suggestion)
   - **USER REMINDER: Claude will NOT remember to do this step unless explicitly prompted. User should ask: "Let's review the LLM feedback against our research before deciding what to change."**
6. **Refine** - Implement decided changes based on post-research analysis (NOT blind acceptance of LLM feedback)
7. **Finalize** - Move approved document to appropriate directory

### Citation Caching Protocol
1. Before re-verifying a case, check `06_RESEARCH/CITATIONS_LOG.md`.
2. If the case is already verified recently and clearly supports the same proposition, do not re-check unless the user requests or context changed.
3. When new verifications occur, append/update the entry in `CITATIONS_LOG.md` with:
   - Good law status, date, holding, support/contrary assessment, key quotes + pin cites, propositions supported, sections it applies to.
4. Prefer South Carolina and Fourth Circuit authority when relevant. Always include pin cites.

### Logging and Debugging
- All agent runs log to `.wepublic_defender/logs/wpd.log` in the case root.
- Include the log path when reporting issues. Check this file for model selections, parse results, and citation log writes.

### Throughout Session
1. Keep files organized in proper directories
2. Update GAMEPLAN.md after completing major tasks
3. Report API costs after expensive operations
4. Maintain professional, efficient tone
5. **NEVER skip the wepublic_defender adversarial review step**

### File Management
1. Never create files in root directory (except specific config files)
2. Always use appropriate subdirectories
3. Follow naming conventions strictly
4. Ask before moving/deleting important files

## State Tracking (.database) — Claude‑Managed

Keep lightweight, case‑scoped state that Claude updates directly (no Python needed):

- Ledger: `.database/organization_log.md`
  - Append one line per action: `timestamp | action | src | dst | notes`
  - Use Edit/MultiEdit (Windows: backslashes in paths per CRITICAL note).

- Index: `.database/organization_index.json`
  - JSON object keyed by path. Minimal schema per entry:
    ```json
    {
      "<path>": {
        "timestamp": "2025-10-11 12:34:56",
        "action": "moved|merged|deleted_empty|categorized|renamed|other",
        "src": "<src_path or null>",
        "dst": "<dst_path or null>",
        "notes": "<free text>"
      }
    }
    ```
  - Before organizing, read this index to avoid reprocessing the same files/folders.
  - After moves/merges, update both the JSON index and the markdown ledger.

Notes:
- Python helper `wpd-org-log` exists but is optional. Prefer direct edits so state remains simple and transparent to the user and Claude.

## Important Notes
- This is federal court litigation - mistakes have consequences
- Always verify citations before filing anything
- Human lawyer must review and sign all filings
- AI is an assistant, not an attorney
- When in doubt, ask the user

## CRITICAL: File Editing on Windows

⚠️ MANDATORY: Always Use Backslashes on Windows for File Paths

When using Edit or MultiEdit tools on Windows, you MUST use backslashes (\) in file paths, NOT forward slashes (/).

❌ WRONG - Will cause errors:

Edit(file_path: "D:\/repos\/project\/file.tsx", ...)

MultiEdit(file_path: "D:\/repos\/project\/file.tsx", ...)

✅ CORRECT - Always works:

Edit(file_path: "D:\\repos\\project\\file.tsx", ...)

MultiEdit(file_path: "D:\\repos\\project\\file.tsx", ...)

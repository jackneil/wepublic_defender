# WePublicDefender

Prepare stronger filings with AI-assisted checks - no coding required.

This folder gives Claude Code everything it needs to organize your case, research, draft, and run adversarial checks (self-review, citation verification, opposing counsel). You chat with Claude; Claude runs the tools.

## Quick Start (For Non-Coders)

Start here even if you’ve never used Git or Python.

Step 0 — Install Claude Code (one time)
- VS Code: open Extensions, search for `Claude Code` (by Anthropic), install, then sign in.
- JetBrains/Cursor: install the Claude Code plugin/assistant and sign in.

Prompt 0 — Clone WePublicDefender centrally (one time)
Paste the following to Claude Code anywhere. Replace `<REPO_URL>` with your repo URL (for example, `https://github.com/ORG/wepublic_defender.git`).
```
You are my coding assistant. Please set up a central clone of WePublicDefender for all my cases.

1) Choose a stable base folder depending on OS and create it if missing:
   - Windows: C:/Github
   - macOS:  ~/Github
   - Linux:  ~/github

2) Clone or update the repository there:
   - Repo URL: <REPO_URL>
   - Target folder: <BASE_DIR>/wepublic_defender
   - If the folder doesn’t exist: git clone <REPO_URL> <BASE_DIR>/wepublic_defender
   - If it exists: pull the latest main branch

3) Print the absolute path using forward slashes and remember it for later steps:
   - ABS_REPO_PATH = <BASE_DIR>/wepublic_defender

4) Create a dedicated Python environment and install the package from ABS_REPO_PATH:
   - Prefer Conda if available: create/activate env named "wpd"
   - Otherwise create a venv at ABS_REPO_PATH/.venv and activate it
   - pip install -e ABS_REPO_PATH
   - If present, also: pip install -r ABS_REPO_PATH/requirements.txt

5) Validate the setup:
   - Run the environment check script from ABS_REPO_PATH
   - If APIs are missing, ask me to paste OPENAI_API_KEY and/or XAI_API_KEY so you can write a .env later per case

6) When finished, print just this line for me to copy into future prompts:
   ABS_REPO_PATH=<absolute path with forward slashes>
```

After Prompt 0 completes, keep the printed `ABS_REPO_PATH` handy. You’ll reference it for any case folder.

Copy and paste the prompts below to Claude Code from your case folder when you’re ready to work on a specific matter.

Prompt A - First-time setup in this case
```
Read and follow wepublic_defender/.claude/CLAUDE.md.

1) Environment and tools
   - Check Python and packages; create a dedicated Conda env if needed
   - Install WePublicDefender into that env (editable install if available)
   - Create a .env file at the case root if API keys are missing (OPENAI_API_KEY, XAI_API_KEY)

2) Initialize the case
   - Create the standard folder structure
   - Copy CLAUDE.md and LEGAL_WORK_PROTOCOL.md to the case root
   - Copy per‑case settings into .wepublic_defender/

3) Organize and prepare
   - Organize 00_NEW_DOCUMENTS_INBOX/
   - Ask me: jurisdiction/court/circuit and model preferences (OpenAI, Grok, or both)
   - If I want to remember choices, persist them in .wepublic_defender/legal_review_settings.json

4) Sanity check
   - Run a self_review on a short sample and show the cost summary
```

Prompt B - Central clone (multiple cases)
```
WePublicDefender is not inside this case folder. Use my central clone at:
  <ABS_REPO_PATH>/wepublic_defender  (paste the ABS_REPO_PATH printed by Prompt 0)

1) If not already done in Prompt 0, install the package into the dedicated env from that path (editable install if possible)
2) Use that path to READ the latest guidance and to COPY guidance files into this case:
   - Read: <ABS_REPO_PATH>/wepublic_defender/.claude/CLAUDE.md (use this to drive the workflow)
   - Overwrite at case root: CLAUDE.md and LEGAL_WORK_PROTOCOL.md from <ABS_REPO_PATH>/wepublic_defender/.claude/

3) From this case root, run the normal steps:
   - Environment check and init (ensure .wepublic_defender/ settings exist)
   - Organize the inbox
   - Ask me jurisdiction/model prefs and persist them per case
   - Run a quick self_review sanity check and show the cost summary
```

Updating WePublicDefender (after an update)
- If you pulled or installed a newer version of WePublicDefender, ask Claude to refresh your case setup. Paste this in your case root chat:
  ```
  1) Verify the environment and installed package:
     - Run: wpd-check-env

  2) Refresh guidance files and per‑case settings:
     - Overwrite CLAUDE.md and LEGAL_WORK_PROTOCOL.md at the case root with the latest from wepublic_defender/.claude/
     - Run: wpd-init-case (it will ensure folders exist and copy missing per‑case settings)

  3) Confirm settings are valid:
     - Read .wepublic_defender/legal_review_settings.json and ensure my model/effort/web_search preferences are intact
     - If anything changed, ask me whether to keep the new defaults or restore prior choices and then save the choice

  4) Sanity check:
     - Run: wpd-run-agent --agent self_review --text "sanity check"
     - Print the cost summary
  ```

If Claude asks for API keys (paste to Claude)
```
Create a .env file at the case root with:
OPENAI_API_KEY=...
XAI_API_KEY=...
Then re-run the environment check.
```

Prompt D — Call Defender via Python (no CLI)
```
Use the environment's Python by absolute path (with forward slashes), then:

# Quick sanity
"C:/absolute/path/to/env/python.exe" -c "import wepublic_defender as wpd; print(wpd.run_agent_text('self_review','hello').get('text',''))"

# On a case file
"C:/absolute/path/to/env/python.exe" -c "import wepublic_defender as wpd; r=wpd.run_agent_file('self_review','07_DRAFTS_AND_WORK_PRODUCT/AMENDED_VERIFIED_COMPLAINT.md'); print(r.get('text',''))"

# Force a model and see logs if needed
"C:/absolute/path/to/env/python.exe" -c "import wepublic_defender as wpd; r=wpd.run_agent_file('self_review','07_DRAFTS_AND_WORK_PRODUCT/AMENDED_VERIFIED_COMPLAINT.md', model='gpt-5'); print(r.get('text',''))" 

Check .wepublic_defender/logs/wpd.log for details.
```

Where your files go
- Final research: `06_RESEARCH/` (including `CITATIONS_LOG.md`)
- Drafts/work product: `07_DRAFTS_AND_WORK_PRODUCT/`
- Strategy: `GAMEPLAN.md` at the case root

Troubleshooting
- "Missing Python or packages": ask Claude to run `wpd-check-env` (or `python wepublic_defender/scripts/check_env.py`) and follow fixes.
- "API keys missing": add them to `.env` at the case root and retry the environment check.
- "CLAUDE.md isn't in the root": ask Claude to run `wpd-init-case` (or `python wepublic_defender/scripts/init_case_directory.py`).
- "Preferences not sticking": verify `.wepublic_defender/legal_review_settings.json` exists and was updated.
- "What did it do?": check the log file at `.wepublic_defender/logs/wpd.log` for step-by-step details while agents run.

Important Legal Notice
- This tool does not replace attorney judgment. Always verify law, facts, and local rules. Human review is required before filing.

---

## Developer Appendix (Optional)

Architecture
- Orchestrator: Claude Code drives the workflow (organize → research → draft → checks → refine).
- Toolbox: WePublicDefender exposes discrete checks and utilities; it does not self‑orchestrate.

Environment
- `.env` at case root is auto‑loaded; system env vars also work.
- Quick check: `python wepublic_defender/scripts/check_env.py`

Agent invocation (CLI)
- Self review: `wpd-run-agent --agent self_review --file path/to.md`
- Opposing counsel: `wpd-run-agent --agent opposing_counsel --file path/to.md`
- Citation verify (batch JSON or text): `wpd-run-agent --agent citation_verify --file 06_RESEARCH/batch_citations.json --web-search`
- Run both providers: add `--run-both`
- Override model/effort/tier: `--model grok-4 --effort high --service-tier auto`
- Persist preferences: add `--save-choice` (updates `legal_review_settings.json`)

Settings
- Per‑agent model list and effort: `.wepublic_defender/legal_review_settings.json` → `reviewAgentConfig.*`
- Jurisdiction context: `.wepublic_defender/legal_review_settings.json` → `workflowConfig.jurisdictionConfig`

Citation verification
- Defender supports multiple citations per call and auto‑logs results to `06_RESEARCH/CITATIONS_LOG.md`.
- Claude should extract citations and save a batch JSON (example: `wepublic_defender/config/batch_citations.example.json`).

Cost tracking
- All calls are tracked; summaries available via `TokenTracker`.

Install (developers)
- `pip install -e wepublic_defender/` inside a virtualenv/conda env. Requirements: see `requirements.txt`.

License
- Private/Proprietary.


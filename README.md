# WePublicDefender

Welcome. We’re glad you’re here to use WePublicDefender — an LLM‑guided case management and pro se assistance helper.

Important: Use at your own risk. This is AI, not a lawyer. Always verify facts, law, and local rules before filing.

## Step 0 - Get Ready (One-Time)

- Get Claude (Anthropic) with access to the Claude Code CLI:
  - Plans: [Anthropic Pricing](https://www.anthropic.com/pricing)
  - Which plan? We recommend Claude Pro 5× for most users. If you have large or complex matters, consider Claude Pro 20×. See pricing details on the official page.
  - Claude (web): [claude.ai](https://claude.ai/)
  - Install the Claude Code CLI (you’ll paste commands into it next): see [Anthropic Docs](https://docs.anthropic.com/claude)

What “CLI” means and how you’ll use it
- CLI = Command Line Interface — a small program you run in your computer’s Terminal or Command Prompt.
- You will open a terminal, run `claude`, and paste the prompts in Steps 1–3. Claude will do the setup and guide you.
- Open Terminal/Command Prompt:
  - Windows: Press Start, type “PowerShell” (or “Command Prompt”), press Enter.
  - macOS: Open Applications → Utilities → Terminal.
  - Linux: Open your distro’s Terminal app.

Install Claude Code CLI (simple)
- Go to: [Anthropic Docs](https://docs.anthropic.com/claude)
- Find the Claude Code CLI section, choose your operating system, and follow the install steps.
- After installing, in your terminal run:
  - `claude --version` (should print a version)
  - `claude login` (sign in to your Anthropic account)

Note: You do NOT need to manually install Git, Python, or Conda. In Step 1, Claude will check for these and install Miniconda if needed.

### Open the Terminal in Your Case Folder (Before Step 1)

Put all the files for your case into a single folder on your computer (for example, Desktop/MyCase). Then open a terminal in that exact folder:

- Windows
  - Open File Explorer and go to your case folder.
  - In Windows 11: right‑click inside the folder background and click “Open in Terminal”.
  - Or click the address bar, type `cmd`, and press Enter.
  - A window opens that shows your folder in the prompt, e.g., `C:\Users\You\Desktop\MyCase>`.

- macOS
  - Create/open your case folder in Finder (for example, Desktop/MyCase).
  - Open Terminal: press Command+Space, type “Terminal”, press Enter.
  - Type `cd ` (with a space), then drag the folder from Finder into the Terminal window. Press Enter.
  - The prompt will now end with `/Desktop/MyCase`.

- Linux
  - Open your file manager, go to the case folder.
  - Right‑click the background → “Open in Terminal”. If you don’t see that, open your Terminal app and type `cd `, then paste or drag the folder path and press Enter.
 - The prompt should show your case folder path.

Start Claude Code here:
- Type `claude` and press Enter. If it asks you to sign in, follow the prompt.
- Leave this window open. You will paste the next steps into this Claude window.

API accounts you'll need (we'll collect keys in Step 1):
- OpenAI: [Create API Key](https://platform.openai.com/api-keys) • [Quickstart](https://platform.openai.com/docs/quickstart)
- xAI Grok: [Console](https://console.x.ai/) • [Docs](https://docs.x.ai/)
- Optional CourtListener: [Register](https://www.courtlistener.com/register/) • [API](https://www.courtlistener.com/api/)

Tip: Using both OpenAI and Grok improves cross‑checking and adversarial analysis.

## Step 1 - Central Setup (Paste into Claude Code CLI)

In that same terminal window, type `claude` (if it’s not already running). Then copy everything between the lines and paste into the Claude Code CLI. Replace `<REPO_URL>` with your repo URL (for example, `https://github.com/ORG/wepublic_defender.git`).

```
You are my coding assistant. Please perform a central setup for WePublicDefender that I can reuse across cases.

1) Create a stable base folder if missing and print it when done:
   - Windows: C:/Github
   - macOS:  ~/github
   - Linux:  ~/github

2) Check and install prerequisites automatically (do NOT ask me to install anything):
   - Verify Git and Python 3.11+; if missing, install them using the appropriate method for my OS.
   - If `conda` is not available, install Miniconda silently.
   - Print versions for confirmation.

3) Clone or update the repository:
   - Repo URL: <REPO_URL>
   - Target: <BASE_DIR>/wepublic_defender
   - If missing: git clone <REPO_URL> <BASE_DIR>/wepublic_defender
   - If present: pull latest main

4) Create a Python environment named "wepublic_defender" (Conda preferred; install Miniconda first if needed). If Conda is not possible, use a local venv in the repo. Then install the package:
   - pip install -e <BASE_DIR>/wepublic_defender

5) Run environment check from the repo root and handle any missing tools/packages:
   - Command: wpd-check-env

6) Collect my API keys and save them to a reusable template (don’t ask me to set environment variables):
   - Show me these links to create keys if I need them:
     • OpenAI: https://platform.openai.com/api-keys
     • xAI Grok: https://console.x.ai/
     • CourtListener (optional): https://www.courtlistener.com/api/
   - Prompt me to paste values, then write a starter .env template we can reuse for cases with:
     OPENAI_API_KEY=...
     XAI_API_KEY=...
     COURTLISTENER_TOKEN=... (optional)

7) Print exactly one line for me to copy for future steps:
   ABS_REPO_PATH=<absolute path to /wepublic_defender with forward slashes>
```

Save the printed `ABS_REPO_PATH` — you’ll use it in the next step.

## Step 2 - Create a Case Folder (Paste into Claude Code CLI)

Make sure your terminal is “in” your case folder (see the section above), then paste this:

```
Use my central install at: ABS_REPO_PATH=<paste the line from Step 1>

1) In this case folder, initialize WePublicDefender and standard directories:
   - Run: wpd-init-case
   - Ensure the following exist:
     00_NEW_DOCUMENTS_INBOX/
     06_RESEARCH/
     07_DRAFTS_AND_WORK_PRODUCT/
     .wepublic_defender/
     .wepublic_defender/legal_review_settings.json
     .wepublic_defender/logs/
     GAMEPLAN.md

2) If a .env doesn’t exist here, help me create one by reusing my central keys (don’t teach env vars; just guide me and write the file).

3) Ask my preferences and persist them into .wepublic_defender/legal_review_settings.json:
   - Jurisdiction, court, circuit
   - Preferred models per agent (OpenAI, Grok, or both)
   - Default web_search on/off

4) Sanity check and print a short summary of keys found, models available, and config paths:
   - Run: wpd-check-env
```

## Step 3 — Run Reviews (Paste into Claude Code CLI)

```
I’ve placed documents in 07_DRAFTS_AND_WORK_PRODUCT/ and/or 00_NEW_DOCUMENTS_INBOX/.
Show me copy/paste commands for:

1) Self review (single file):
   wpd-run-agent --agent self_review --file "07_DRAFTS_AND_WORK_PRODUCT/FILE.md"

2) Opposing counsel attack (single file):
   wpd-run-agent --agent opposing_counsel --file "07_DRAFTS_AND_WORK_PRODUCT/FILE.md"

3) Citation verification (batch JSON with many citations):
   wpd-run-agent --agent citation_verify --file "06_RESEARCH/batch_citations.json" --web-search

4) Run both providers for redundancy (OpenAI + Grok):
   wpd-run-agent --agent self_review --file "07_DRAFTS_AND_WORK_PRODUCT/FILE.md" --run-both

5) Optional per‑run overrides:
   --model gpt-5-mini | grok-4-fast  --service-tier auto  --effort medium  --save-choice

Also show where outputs/logs will be and how to view costs.
```

## Where Outputs Go

- Research and citation logs: `06_RESEARCH/` (e.g., `CITATIONS_LOG.md`)
- Drafts and work product: `07_DRAFTS_AND_WORK_PRODUCT/`
- Case plan: `GAMEPLAN.md`
- Logs: `.wepublic_defender/logs/wpd.log`
- Usage/cost CSV: `.wepublic_defender/usage_log.csv`

## Troubleshooting

- Keys missing — Claude should help you create `.env` at the case root. Then run `wpd-check-env`.
- Import errors (e.g., docx) - Ask Claude to reinstall: `pip install -e ABS_REPO_PATH`.
- Wrong Python/env — Ask Claude to activate the env from Step 1, then run `wpd-check-env`.
- What happened? — Open `.wepublic_defender/logs/wpd.log` for step‑by‑step trace.

## Claude Plan Overview (FYI)

| Plan | Includes CLI | Typical Price | Recommended For | Subscribe |
| --- | --- | --- | --- | --- |
| Pro 5× (Recommended) | Yes | ~$100/mo | Most users and typical matters | [Anthropic Pricing](https://www.anthropic.com/pricing) |
| Pro 20× (Heavy Use) | Yes | ~$200/mo | Large/complex documents and heavier workloads | [Anthropic Pricing](https://www.anthropic.com/pricing) |

Note: Names, features, and prices change. Always confirm current details on the official pricing page.

---

## Technical Appendix (Optional)

For technical users who prefer manual commands (without Claude guiding each step):

1) Clone repo and create env
   - Windows (PowerShell)
     - `New-Item -ItemType Directory -Path C:\Github -Force | Out-Null`
     - `cd C:\Github`
     - `git clone <REPO_URL> wepublic_defender` (or `git -C wepublic_defender pull`)
     - Conda: `conda create -n wepublic_defender python=3.11 -y; conda activate wepublic_defender`
     - Or venv: `py -3.11 -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`
     - Install: `pip install -e wepublic_defender\\`
   - macOS/Linux (Bash)
     - `mkdir -p ~/github && cd ~/github`
     - `git clone <REPO_URL> wepublic_defender` (or `git -C wepublic_defender pull`)
     - Conda: `conda create -n wepublic_defender python=3.11 -y && conda activate wepublic_defender`
     - Or venv: `python3 -m venv .venv && source .venv/bin/activate`
     - Install: `pip install -e wepublic_defender/`

2) Create a case and run
   - `cd /path/to/your/case` (create a new folder for each case)
   - `wpd-init-case`
   - Let Claude (Step 2) help you create `.env` at the case root and persist preferences.
   - `wpd-check-env`
   - `wpd-run-agent --agent self_review --file "07_DRAFTS_AND_WORK_PRODUCT/FILE.md"`

Links
- OpenAI Keys: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- xAI Grok Console: [console.x.ai](https://console.x.ai/)
- CourtListener API: [courtlistener.com/api](https://www.courtlistener.com/api/)

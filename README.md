# WePublicDefender

Welcome. We’re glad you’re here to use WePublicDefender — an LLM‑guided case management and pro se assistance helper.

Important: Use at your own risk. This is AI, not a lawyer. Always verify facts, law, and local rules before filing.

## Step 0 - Get Ready (One-Time)

- Get Claude (Anthropic) with access to the Claude Code CLI:
  - Plans: [Anthropic Pricing](https://www.anthropic.com/pricing)
  - Which plan? We recommend Claude Max 5x for most users. If you have large or complex matters, consider Claude Max 20x. You can try Claude Pro, but you may run out of usage quickly. See pricing details on the official page.
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

In that same terminal window, type `claude` (if it's not already running). Then copy everything between the lines and paste into the Claude Code CLI. Use this repo URL: https://github.com/jackneil/wepublic_defender.git

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
   - Repo URL: https://github.com/jackneil/wepublic_defender.git
   - Target: <BASE_DIR>/wepublic_defender
   - If missing: git clone https://github.com/jackneil/wepublic_defender.git <BASE_DIR>/wepublic_defender
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

7) Initialize THIS case (the folder where my terminal is open) and prepare guidance:
   - Run: wpd-init-case in the current working directory (do not create a new folder)
   - Ensure standard directories exist and .wepublic_defender/ is created
   - Copy CLAUDE.md and LEGAL_WORK_PROTOCOL.md into this case folder
   - Copy default per-case settings into .wepublic_defender/
   - If a .env is missing here, help me create it by reusing the keys you collected

8) Tell me clearly what to do next, pointing to CLAUDE.md:
   - "Open CLAUDE.md in this folder and follow it step-by-step to organize your case files (it includes the init/checklists). When done, come back here to run reviews."

9) Persist paths so I don't have to copy anything:
   - Store the absolute path to the created environment's Python executable and env name
   - Store the central repo path you cloned
   - Save these to .wepublic_defender/env_info.json in this case folder with keys:
     { "python_exe": "...", "conda_env": "...", "repo_path": "..." }

10) Offer to run common reviews now (do NOT show me CLI commands):
   - Ask me in plain language which to run first (Self Review on my main draft, Opposing Counsel attack, or Citation Verification)
   - You run the chosen review(s) for me and summarize results in plain language
   - Include a brief cost/usage summary and where to find outputs/logs
```

Save the printed `ABS_REPO_PATH` — you’ll use it in the next step.

## Where Outputs Go

- Research and citation logs: `06_RESEARCH/` (e.g., `CITATIONS_LOG.md`)
- Drafts and work product: `07_DRAFTS_AND_WORK_PRODUCT/`
- Case plan: `GAMEPLAN.md`
- Logs: `.wepublic_defender/logs/wpd.log`
- Usage/cost CSV: `.wepublic_defender/usage_log.csv`

## Troubleshooting

- Keys missing — Ask Claude to create/update `.env` in this case folder; it will handle it.
- Import errors (e.g., docx) — Ask Claude to repair the environment and reinstall the package; it will handle it.
- Wrong Python/env — Ask Claude to switch to the environment it created and recheck; it will handle it.
- What happened? — Ask Claude to show the latest `.wepublic_defender/logs/wpd.log` and explain the steps.

## Claude Plan Overview (FYI)

| Plan | Includes CLI | Typical Price | Recommended For | Subscribe |
| --- | --- | --- | --- | --- |
| Max 5x (Recommended) | Yes | ~$100/mo | Most users and typical matters | [Anthropic Pricing](https://www.anthropic.com/pricing) |
| Max 20x (Heavy Use) | Yes | ~$200/mo | Large/complex documents and heavier workloads | [Anthropic Pricing](https://www.anthropic.com/pricing) |

Note: Names, features, and prices change. Always confirm current details on the official pricing page.

---

## Technical Appendix (Optional)

For technical users who prefer manual commands (without Claude guiding each step):

1) Clone repo and create env
   - Windows (PowerShell)
     - `New-Item -ItemType Directory -Path C:\Github -Force | Out-Null`
     - `cd C:\Github`
    - `git clone https://github.com/jackneil/wepublic_defender.git wepublic_defender` (or `git -C wepublic_defender pull`)
     - Conda: `conda create -n wepublic_defender python=3.11 -y; conda activate wepublic_defender`
     - Or venv: `py -3.11 -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`
     - Install: `pip install -e wepublic_defender\\`
   - macOS/Linux (Bash)
     - `mkdir -p ~/github && cd ~/github`
    - `git clone https://github.com/jackneil/wepublic_defender.git wepublic_defender` (or `git -C wepublic_defender pull`)
     - Conda: `conda create -n wepublic_defender python=3.11 -y && conda activate wepublic_defender`
     - Or venv: `python3 -m venv .venv && source .venv/bin/activate`
     - Install: `pip install -e wepublic_defender/`

2) Create a case and run
   - `cd /path/to/your/case` (create a new folder for each case)
   - `wpd-init-case`
   - Let Claude help you create `.env` at the case root and persist preferences.
   - `wpd-check-env`
   - `wpd-run-agent --agent self_review --file "07_DRAFTS_AND_WORK_PRODUCT/FILE.md"`

Links
- OpenAI Keys: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- xAI Grok Console: [console.x.ai](https://console.x.ai/)
- CourtListener API: [courtlistener.com/api](https://www.courtlistener.com/api/)





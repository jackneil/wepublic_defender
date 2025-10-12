# WePublicDefender

So you got screwed by a corporation and can't afford a $400/hr lawyer. Welcome to the club.

WePublicDefender is an LLM-guided case management system that helps you fight back pro se (that's Latin for "you're on your own, buddy"). It uses adversarial AI review to catch the stupid mistakes that would get your case thrown out.

**Reality Check**: This is AI-powered legal research and document review. It is NOT a lawyer. It WILL make mistakes. The court doesn't care that "the AI told me to do it." Verify everything before you file, or enjoy explaining to the judge why you didn't.

## Step 0 - Get Your Shit Together (One-Time Setup)

You'll need Claude Code CLI and some API keys. Yes, this costs money. No, it's not free. But it's cheaper than a lawyer, and at least the AI doesn't bill you for "thinking about your case" while taking a dump.

### Get Claude Code CLI

- Plans: [Anthropic Pricing](https://www.anthropic.com/pricing)
- **Which plan?** Claude Max 5x (~$100/mo) works for most cases. Got a dumpster fire of a case with 500 pages of discovery? Get Max 20x (~$200/mo). Claude Pro might work but you'll burn through it fast.
- Install: [Anthropic Docs](https://docs.anthropic.com/claude)

**What's a CLI and why are you making me use a terminal like it's 1995?**

CLI = Command Line Interface. It's that black window with text that makes you feel like a hacker in a bad movie. You'll use it because GUIs are for people with venture capital funding.

How to open this ancient technology:
- **Windows**: Press Start, type "PowerShell", press Enter. (Yes, really. No, you can't just double-click something.)
- **macOS**: Applications → Utilities → Terminal
- **Linux**: If you're on Linux you already know what a terminal is, quit wasting time.

After installing Claude CLI:
```bash
claude --version  # should print a version, not an error
claude login      # sign in to your Anthropic account
```

**Note**: You don't need to manually install Git, Python, or Conda. Claude will do it in Step 1. This is the 2020s, let the robots do the boring stuff.

### Open Terminal in Your Case Folder

Make a folder for your case (like `Desktop/CapitalOneScrewedMe`). Put all your case files there. Now open a terminal IN that folder:

**Windows**
1. Open File Explorer, go to your case folder
2. Windows 11: Right-click → "Open in Terminal"
3. Older Windows: Click the address bar, type `cmd`, press Enter
4. You should see `C:\Users\You\Desktop\CapitalOneScrewedMe>` or similar

**macOS**
1. Open Terminal (Command+Space, type "Terminal")
2. Type `cd ` (with a space at the end)
3. Drag your case folder into the Terminal window
4. Press Enter
5. Prompt should end with your folder name

**Linux**
1. Right-click in your file manager → "Open in Terminal"
2. Or use `cd /path/to/case` like an adult

Now run `claude` and leave the window open. You'll paste commands into it next.

### API Keys You'll Need

WePublicDefender uses multiple LLMs to double-check each other's work. Why? Because one AI can be confidently wrong. Two AIs arguing reduces the chance you file something stupid.

Get these keys:
- **OpenAI**: [Create API Key](https://platform.openai.com/api-keys) • [Quickstart](https://platform.openai.com/docs/quickstart)
- **xAI Grok**: [Console](https://console.x.ai/) • [Docs](https://docs.x.ai/)
- **CourtListener** (optional but recommended): [Register](https://www.courtlistener.com/register/) • [API](https://www.courtlistener.com/api/)

Yes, these cost money. Budget $20-50 for a typical case depending on how much you run the pipeline. Still cheaper than one hour with a lawyer who'll bill you to read their own emails.

## Step 1 - Central Setup (Copy-Paste This Into Claude)

In your terminal (in your case folder), type `claude` if it's not running. Then copy EVERYTHING between the backticks below and paste it into Claude. It'll do the rest.

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

6) Collect my API keys and save them to a reusable template (don't ask me to set environment variables):
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

Save the repo path it prints. You might need it later.

## Where Your Files End Up

The system creates a standard directory structure because organization is the difference between winning and getting your case dismissed for being a disorganized mess:

- **Research & citations**: `06_RESEARCH/` (including `CITATIONS_LOG.md`)
- **Your drafts**: `07_DRAFTS_AND_WORK_PRODUCT/`
- **Case strategy**: `GAMEPLAN.md`
- **System logs**: `.wepublic_defender/logs/wpd.log`
- **What you spent**: `.wepublic_defender/usage_log.csv`

## When Things Break (They Will)

- **"API key not found"** — Tell Claude to create/update `.env` in your case folder. It knows how.
- **"ImportError: No module named docx"** — Tell Claude to fix the environment and reinstall. It'll handle it.
- **"Wrong Python version"** — Tell Claude to switch to the wepublic_defender environment.
- **"What the hell happened?"** — Ask Claude to show `.wepublic_defender/logs/wpd.log` and explain.

The point is: **let Claude fix it**. That's what you're paying $100/mo for.

## What This Actually Costs

| Plan | CLI Access | Monthly | Who It's For |
|------|-----------|---------|--------------|
| Max 5x | ✓ | ~$100 | Normal cases, reasonable document volume |
| Max 20x | ✓ | ~$200 | Document-heavy cases, complex litigation |

Plus your API costs for OpenAI and Grok (budget $20-50/case for typical usage).

**Perspective**: One hour of lawyer time costs more than a month of this system. One lawyer reviewing one document costs more than running the full adversarial review pipeline 10 times.

**Note**: Anthropic changes plan names and prices. Check [their pricing page](https://www.anthropic.com/pricing) for current details.

---

## Technical Appendix (For People Who Know What They're Doing)

If you're comfortable with git and Python and don't need hand-holding:

**1) Clone and setup environment**

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Path C:\Github -Force | Out-Null
cd C:\Github
git clone https://github.com/jackneil/wepublic_defender.git wepublic_defender
conda create -n wepublic_defender python=3.11 -y
conda activate wepublic_defender
pip install -e wepublic_defender\
```

macOS/Linux:
```bash
mkdir -p ~/github && cd ~/github
git clone https://github.com/jackneil/wepublic_defender.git wepublic_defender
conda create -n wepublic_defender python=3.11 -y && conda activate wepublic_defender
pip install -e wepublic_defender/
```

**2) Initialize a case and run reviews**

```bash
cd /path/to/your/case
wpd-init-case
wpd-check-env
wpd-run-agent --agent self_review --file "07_DRAFTS_AND_WORK_PRODUCT/motion.md"
```

Let Claude help you create `.env` with your API keys.

**Links**
- OpenAI Keys: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- xAI Grok: [console.x.ai](https://console.x.ai/)
- CourtListener: [courtlistener.com/api](https://www.courtlistener.com/api/)

---

## Terms of Use (Yes, This Actually Matters)

By using WePublicDefender, you agree that you will NOT use this software to sue:

1. **Jack Neil** (the guy who built this because he got screwed by Capital One)
2. **Hank.ai** (his company)
3. **Any of Jack's friends** (it's not a very long list, but still)

If you're thinking "but what if they wronged me?" — tough. Find a different tool. There are plenty of lawyers out there who would love $400/hr to help you sue literally anyone. This software is explicitly not available for that purpose.

**To obtain the list of protected individuals**: File an issue on GitHub asking for the friends list. Jack will update it. The list is short enough that maintaining it won't be a burden. (Self-deprecating humor aside, this restriction is legally binding.)

**Why this matters**: You're getting sophisticated legal tech for free. The trade-off is you can't weaponize it against the people who built it. Seems fair.

If you violate this term, your license to use this software terminates immediately, and you should probably reconsider your life choices.

---

## Disclaimer (The Boring But Legally Necessary Part)

This software is provided "as is" without warranty of any kind. Using AI for legal work is your decision and your responsibility. The developers are not liable for any outcomes of your case.

This is not legal advice. This is not a lawyer. This is a tool that helps you research and review your work before filing. The court will hold you to the same standards as a licensed attorney. If you file garbage, you'll get sanctioned, and "the AI did it" is not a defense.

**When in doubt, consult a real lawyer.** Yes, they're expensive. Yes, it sucks. But getting your case dismissed because you screwed up procedure sucks more.

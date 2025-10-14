# WePublicDefender

So you got screwed by a corporation and can't afford a $400/hr lawyer. Welcome to the club.

WePublicDefender is an LLM-guided case management system that helps you fight back pro se (that's Latin for "you're on your own, buddy"). But here's the thing: you're not just using "AI" - you're using **adversarial** AI.

**How it works**: Multiple LLMs review your documents and argue with each other about what's wrong. GPT-5 finds issues. Grok-4 counters with different concerns. They fight until your document is bulletproof. It's like having a lawyer, their opposing counsel, and a paranoid law professor all reviewing your work before you file.

**What it catches**: Missing jurisdiction statements. Weak legal standards. Unsupported factual claims. Citations that don't say what you think they say. The procedural tripwires that get pro se cases dismissed before the judge even reads your argument.

**Reality Check**: This is AI-powered legal research and document review. It is NOT a lawyer. It WILL make mistakes. The court doesn't care that "the AI told me to do it." You still verify everything before filing. But you're verifying **after** multiple AIs have already torn your work apart and forced you to fix it.

**The difference**: Most people filing pro se submit their first draft. You're submitting your tenth draft after surviving an AI firing squad. That's why this works.

## How Claude Code Works - Choose Your Mode

Claude Code has 3 operating modes. Understanding them is crucial for legal work:

### 🤖 Auto-Accept Mode (Default)
- Claude makes changes immediately without asking
- **Don't use this for legal work** - too risky
- Good for: Quick file organization, simple tasks

### ✋ Manual Accept Mode
- Claude proposes changes, you approve each one
- More control but tedious for large reviews
- Good for: Small edits, learning what Claude does

### 📋 Plan Mode (RECOMMENDED FOR LEGAL WORK)
- Claude presents a complete plan before doing anything
- You review the strategy, then approve execution
- **Use this when processing agent results**
- Good for: Document reviews, research processing, anything important

### How to Switch Modes
- **Enter Plan Mode**: Type `/plan` or press Ctrl+P
- **Exit Plan Mode**: Approve the plan when ready
- **Manual Mode**: Settings → Edit Mode → "Manual Accept"

### Best Practice for Legal Work

1. Run an agent (self_review, citation_verify, opposing_counsel)
2. **SWITCH TO PLAN MODE** before processing results
3. Let Claude analyze findings and propose next steps
4. Review the plan carefully
5. Approve to execute

**Why this matters**: Legal work requires deliberate decision-making. Plan mode forces you (and Claude) to think before acting. You catch mistakes before they become filed documents.

## Table of Contents

- [How Claude Code Works - Choose Your Mode](#how-claude-code-works---choose-your-mode) - Understanding auto-accept, manual, and plan modes for legal work
- [Step 0 - Get Your Shit Together](#step-0---get-your-shit-together-one-time-setup) - One-time setup: Claude CLI, terminal basics, API keys
- [Step 1 - Central Setup](#step-1---central-setup-copy-paste-this-into-claude) - Copy-paste this into Claude to set everything up automatically
- [Available Commands](#available-commands-what-you-can-tell-claude-to-do) - Slash commands and plain English instructions you can use
- [How to Use Deep Research](#how-to-use-deep-research-step-by-step) - Complete workflow for comprehensive legal research using Claude.ai
- [Where Your Files End Up](#where-your-files-end-up) - Directory structure and file organization
- [When Things Break](#when-things-break-they-will) - Common errors and how to fix them
- [What This Actually Costs](#what-this-actually-costs) - Pricing breakdown for Claude plans and API usage
- [Technical Appendix](#technical-appendix-for-people-who-know-what-theyre-doing) - Manual setup for developers who don't need hand-holding
- [Terms of Use](#terms-of-use-yes-this-actually-matters) - Who you can't sue with this software
- [Disclaimer](#disclaimer-the-boring-but-legally-necessary-part) - Legal disclaimers and responsibility

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

10) After setup completes, tell me to RESTART Claude Code:
   - The init command installs slash commands to .claude/commands/
   - Claude Code only loads commands at startup, not during a session
   - Tell me: "Exit Claude Code (Ctrl+C) and run 'claude' again in this folder"
   - After restart, commands like /deep-research-prep will work

11) Offer to run common reviews now (do NOT show me CLI commands):
   - Ask me in plain language which to run first (Self Review on my main draft, Opposing Counsel attack, or Citation Verification)
   - You run the chosen review(s) for me and summarize results in plain language
   - Include a brief cost/usage summary and where to find outputs/logs
```

Save the repo path it prints. You might need it later.

## Available Commands (What You Can Tell Claude to Do)

You don't need to memorize commands or learn Python. Just talk to Claude in plain English. But if you want to be specific, these slash commands do specific things:

**For Getting Started:**
- `/check-env` - Check if everything is set up correctly (run this if you get errors)
- `/organize` - Put your messy documents into the right folders

**For Research:**
- `/deep-research-prep` - Create a research assignment for Claude.ai Deep Research
  - Use this when starting a new case or need heavy web research
  - Claude Code will generate a prompt, you copy it to Claude.ai, wait 5-10 minutes for deep research, then paste results back
  - Way more efficient than doing tons of web searches in Claude Code
- `/research [topic]` - Quick research on a specific legal topic (lighter than deep research)

**For Strategy:**
- `/strategy` - Get strategic recommendations for your next moves

**For Writing:**
- `/draft [type]` - Draft a legal document (motion, response, brief, etc.)
- `/review [file]` - Have multiple AIs review your document before filing

**How to use these:**
Just type the command. For example:
```
/deep-research-prep

/research summary judgment standards South Carolina

/draft motion to dismiss

/strategy
```

Claude will do everything else. No technical knowledge required.

### 🎯 Pro Tip: Use Plan Mode After Running Agents

When you run agents like `/review` or get research results:

1. **Switch to Plan Mode** (type `/plan` or Ctrl+P)
2. Say: "Process the review results and propose next steps"
3. Claude will present a plan addressing all findings
4. Review it carefully - does it make sense?
5. Approve to execute

This prevents knee-jerk reactions to agent feedback and ensures you're making deliberate choices about your case strategy.

### 🔮 Coming Soon

Agents will eventually recommend mode switches in their output:
> "Review complete. Switch to Plan Mode (type /plan) to process these findings systematically."

## How to Use Deep Research (Step-by-Step)

**Important: Claude Code will automatically offer to run deep research when appropriate.** You rarely need to trigger this manually. This guide shows you what happens and how to complete the workflow when Claude suggests it.

Deep Research uses Claude.ai's Research feature to conduct thorough legal analysis. It's way more efficient than running dozens of web searches in Claude Code, and gives you comprehensive case assessment in 5-10 minutes.

### When Claude Will Offer Deep Research

Claude Code automatically suggests deep research when:
- You're starting a new case (first time in a case folder)
- GAMEPLAN.md is empty or minimal
- You ask about case viability or strategy
- You need comprehensive legal analysis

You'll see something like:
> "This appears to be a new case. Would you like me to generate a comprehensive deep research prompt? I'll create a prompt you can paste into Claude.ai's Deep Research mode..."

### When to Use Deep Research

- Starting a new case (need viability assessment)
- Major legal motions requiring extensive case law
- Complex legal questions with multiple angles
- Strategic case planning

### Requirements

- Claude Pro, Max, Team, or Enterprise account (for Claude.ai web interface)
- Access to https://claude.ai

### Complete Workflow

**Step 1: Claude Generates Research Prompt**

When Claude Code offers deep research (or you type `/deep-research-prep`), it will generate a comprehensive research prompt tailored to your case with sections like:
- Legal Claims Analysis
- Damages Assessment
- Venue & Jurisdiction Analysis
- Defense Strategy Prediction
- Procedural Requirements
- Strategic Considerations
- Timeline and Cost Estimates

**Step 2: Copy the Entire Prompt**

Select all the text from the generated prompt (usually starts with "# Deep Legal Research" and ends with special instructions). Copy it to your clipboard.

**Step 3: Open Claude.ai in Your Browser**

Go to https://claude.ai and log in with your paid account.

**Step 4: Enable Research Mode**

Look at the bottom left of the chat interface. You'll see a "Research" button:
- If the button is **WHITE** → Research is disabled
- Click the button once to enable it (turns **BLUE**)
- Make sure "Web search" is also enabled

**Step 5: Paste Prompt and Start Research**

- Paste the entire research prompt into the message box
- Choose model: **Claude Sonnet 4.5** (best for legal research)
- Click Send

**Step 6: Wait for Research (5-10 Minutes)**

Claude.ai will now:
- Conduct multiple interconnected web searches automatically
- Explore different legal angles systematically
- Build on previous findings with each search
- Cite all sources

You'll see Claude working through the research with progress updates. Grab coffee. This takes time.

**Step 7: Download Results to Your Case Folder**

When research completes:

1. Click the **three dots menu** (⋮) in the top right of the conversation
2. Select **"Download conversation"**
3. Save the file to: **`YourCaseFolder/00_NEW_DOCUMENTS_INBOX/`**
   - Example: `C:\Users\You\Desktop\CapitalOneScrewedMe\00_NEW_DOCUMENTS_INBOX\deep_research_2025-10-13.md`
4. Use a descriptive filename like `deep_research_initial_assessment.md`

**Why download to inbox?** Claude Code automatically checks the inbox after generating a deep research prompt. It knows to look there.

**Step 8: Tell Claude Code You're Done**

Go back to your Claude Code terminal and say:

```
Done. I downloaded the research to the inbox.
```

Or just:

```
Done
```

**💡 Best Practice**: Switch to Plan Mode before saying you're done:

1. Type `/plan` to enter Plan Mode
2. Say "Done. I downloaded the research to the inbox."
3. Claude will present a complete plan for processing results
4. Review the plan (file organization, GAMEPLAN generation, next steps)
5. Approve when ready

This ensures you see exactly what Claude will do with the research before it happens.

Claude Code will automatically:
- Find the research file in `00_NEW_DOCUMENTS_INBOX/`
- Move it to `06_RESEARCH/deep_research_initial_assessment.md`
- Analyze the findings
- Generate a strategic GAMEPLAN.md with concrete next steps
- Mark initial research as complete

**Alternative: Copy-Paste (If Download Doesn't Work)**

If you can't download or prefer to copy-paste:

1. Select all of Claude.ai's research response
2. Copy to clipboard
3. In Claude Code terminal, say:
```
Here are the deep research results:

[Paste the entire research output here]
```

Claude will save it and process it the same way.

**Step 9: Review Your GAMEPLAN**

Open `GAMEPLAN.md` in your case folder. Claude has generated:
- Case strength assessment (Strong/Moderate/Weak)
- Recommended legal claims with rationale
- Immediate next steps (specific action items)
- Key deadlines
- Evidence you need to gather
- Anticipated opposing arguments
- Settlement considerations
- Risks and concerns

This becomes your roadmap for the entire case.

### Manual Trigger (Rarely Needed)

If Claude doesn't automatically offer deep research, you can trigger it:

```
/deep-research-prep
```

But 99% of the time, Claude will suggest it when appropriate.

### Tips

- **Be specific about your situation**: When Claude asks for case details, provide facts, dates, parties, jurisdiction
- **Let it complete**: Deep Research takes 5-10 minutes (sometimes longer). Don't interrupt
- **Download to inbox**: Claude knows to look there - makes the workflow seamless
- **Check key citations**: After receiving results, verify critical case citations with `/research [case name]`
- **Update GAMEPLAN regularly**: As case evolves, tell Claude to update GAMEPLAN.md

### Troubleshooting

**"Research button is missing in Claude.ai"**
- You need a paid Claude account (Pro, Max, Team, or Enterprise)
- Research is not available on free plans

**"Research isn't working"**
- Make sure Web Search toggle is enabled (bottom of Claude.ai chat)
- Try prompting: "Claude, please use the Research tool to..."

**"Claude Code isn't finding my downloaded file"**
- Make sure you saved it to `00_NEW_DOCUMENTS_INBOX/` in your case folder
- Check the filename doesn't have weird characters
- Tell Claude: "Check the inbox for the research file"

**"Results are too generic"**
- Provide more specific details when Claude asks about your case
- Include: jurisdiction, court, parties, specific facts, dates
- Claude can regenerate the prompt with more details

### Why This Workflow Works

**Separation of concerns:**
- **Claude.ai** does the heavy lifting: 50+ web searches, 5-10 minutes of research
- **Claude Code** does the organization: files the research, generates strategy, manages your case

**Cost effective:**
- One deep research session ≈ cost of one lawyer consultation
- But you get comprehensive analysis instead of "let me think about it and bill you later"

**Reusable:**
- Research goes into `06_RESEARCH/`
- You can reference it throughout the case
- Update GAMEPLAN as situation changes

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

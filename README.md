# WePublicDefender: Your AI Legal War Room

**Imagine having 5 lawyers review your case - one finding weaknesses, another verifying every citation, a third acting as opposing counsel trying to destroy your arguments, a fourth suggesting strategy, and a fifth making sure everything's perfect. Now imagine they're all AI, working 24/7, and arguing with each other until your legal documents are bulletproof.**

That's WePublicDefender. And it costs less than one hour with a real lawyer.

📚 **[Full Documentation on GitHub Wiki →](https://github.com/jackneil/wepublic_defender/wiki)**

## The Secret Weapon: Adversarial AI That Fights Itself

So you got screwed by a corporation and can't afford a $400/hr lawyer. Here's what changes everything: WePublicDefender doesn't just use AI - it uses **multiple AIs that actively fight each other** over your case.

### What You Get

```
You: /review my_motion_to_dismiss.md

Claude runs your document through an adversarial pipeline:
  → Self-review finds 8 structural issues
  → Citation verification catches 3 overruled cases
  → Opposing counsel AI finds arbitration clause weakness
  → Pipeline fixes all issues and re-validates
  → Runs again until ALL AIs agree: READY TO FILE

Total time: 9 minutes
Total cost: $12.83
Lawyer equivalent: $3,600 (9 hours @ $400/hr)
```

**Traditional Pro Se**: You write → File → Judge dismisses for procedural errors → Game over

**With WePublicDefender**: You write → 5 AIs attack it → Fix issues → AIs attack again → Repeat until bulletproof → File with confidence

### Real Capabilities

- **📚 Handles Massive Documents**: 300-page credit reports, 500-page discovery productions - converts PDFs to images and reads every page
- **🔄 Iterative Refinement**: Reviews, fixes, reviews again up to 10+ rounds until all AIs agree your document is solid
- **🔍 Live Legal Research**: AIs search current case law, verify citations are good law, find recent rulings
- **🗂️ Manages Your Entire Case**: Auto-organizes documents, maintains timeline, tracks deadlines, updates strategy
- **💰 Tracks Every Penny**: See exactly what each review costs (typically $2-5 for complete multi-AI review)

**[Learn more about features →](https://github.com/jackneil/wepublic_defender/wiki/Advanced-Features)**

### The Iterative Pipeline (What Makes This Bulletproof)

```
DO {
  Run Complete Review Pipeline (5 phases)
  Track ALL changes made
} WHILE (any_changes_made > 0)

Only exits when ENTIRE pipeline passes with ZERO changes
```

Why? Legal documents are interconnected systems. Fixing one thing can affect everything else. The pipeline keeps re-validating until achieving a perfect zero-defect pass.

**[Deep dive into the pipeline →](https://github.com/jackneil/wepublic_defender/wiki/Review-Pipeline)**

## Quick Start (5 Minutes)

### Requirements

**You'll need:**
- Claude Code CLI ([Max 5x or Max 20x plan](https://www.anthropic.com/pricing) - ~$100-200/mo)
- API keys ([OpenAI](https://platform.openai.com/api-keys), [xAI Grok](https://console.x.ai/), optional [CourtListener](https://www.courtlistener.com/api/))
- Budget $20-50/case for API usage (still cheaper than one lawyer hour)

**[Complete installation guide →](https://github.com/jackneil/wepublic_defender/wiki/Installation-Guide)**

### Setup (Copy-Paste and Go)

1. **Open terminal in your case folder**
   - Windows: Right-click folder → "Open in Terminal"
   - Mac: Open Terminal, type `cd ` and drag folder in
   - **[Need help? →](https://github.com/jackneil/wepublic_defender/wiki/Complete-Beginner-Setup)**

2. **Run Claude Code**
   ```bash
   claude
   ```

3. **Paste this entire setup command:**
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
      - If missing: git clone
      - If present: pull latest main

   4) Create a Python environment named "wepublic_defender" (Conda preferred). Install the package:
      - pip install -e <BASE_DIR>/wepublic_defender

   5) Run environment check and handle any missing tools/packages:
      - Command: wpd-check-env

   6) Collect my API keys and save them to a reusable .env template:
      - Show me links to create keys if I need them
      - Prompt me to paste values
      - Write .env with: OPENAI_API_KEY, XAI_API_KEY, COURTLISTENER_TOKEN (optional)

   7) Initialize THIS case (current directory) and prepare guidance:
      - Run: wpd-init-case
      - Create standard directories and .wepublic_defender/ folder
      - Copy configuration files into this case folder
      - Create .env if missing

   8) Persist paths to .wepublic_defender/env_info.json:
      - { "python_exe": "...", "conda_env": "...", "repo_path": "..." }

   9) Tell me to RESTART Claude Code:
      - Exit and run 'claude' again to load slash commands
      - After restart, commands like /deep-research-prep will work

   10) Offer to run common reviews now in plain language (do NOT show CLI commands)
   ```

4. **Claude does everything automatically** - installs tools, sets up environment, gets your API keys, initializes your case

5. **Restart Claude Code** when setup completes:
   ```bash
   # Exit (Ctrl+C), then:
   claude
   ```

**[Step-by-step beginner guide →](https://github.com/jackneil/wepublic_defender/wiki/Complete-Beginner-Setup)**

## How to Use It (Just Talk to Claude)

You don't need to memorize commands or learn Python. Just talk to Claude in plain English:

```
"Organize my case files"
"Review my motion to dismiss"
"Research qualified immunity in South Carolina"
"Draft a response to their motion"
"What's my next deadline?"
```

### Slash Commands (For Specificity)

- `/organize` - Put messy documents into proper legal folders
- `/deep-research-prep` - Generate comprehensive research prompt for Claude.ai Deep Research
- `/research [topic]` - Quick legal research on specific topic
- `/strategy` - Get strategic recommendations for next moves
- `/draft [type]` - Draft legal documents (motions, responses, briefs)
- `/review [file]` - Run full adversarial review pipeline

**[Complete command reference →](https://github.com/jackneil/wepublic_defender/wiki/Slash-Commands-Reference)**

### Example Workflow

**Starting a new case:**
```
You: I need to sue Capital One for FDCPA violations

Claude: I'll generate a deep research prompt. [Creates comprehensive research assignment]

You: [Paste into Claude.ai, wait 10 minutes, download results to inbox]

Claude: Research processed. Case strength: STRONG.
        Recommended claims: FDCPA §1692e, §1692f
        Next steps: Draft complaint, gather evidence
        Deadline: None yet (pre-filing)
```

**Reviewing a document before filing:**
```
You: /review my_motion_to_dismiss.md

Claude: Running adversarial review pipeline...
        ✓ Self-review: Found 8 issues, fixed
        ✓ Citations: Replaced 3 overruled cases
        ⚠ Opposing counsel: Found arbitration weakness
        ✓ Pipeline re-run: All clear

        READY TO FILE (after 3 complete passes)
        Cost: $12.83 | Time: 9 minutes
```

**[See more examples →](https://github.com/jackneil/wepublic_defender/wiki/Code-Examples)**

## What This Costs

| Plan | CLI Access | Monthly | Who It's For |
|------|-----------|---------|--------------|
| Max 5x | ✓ | ~$100 | Normal cases, reasonable document volume |
| Max 20x | ✓ | ~$200 | Document-heavy cases, complex litigation |

Plus API costs for OpenAI and Grok (budget $20-50/case for typical usage).

**Perspective**: One hour of lawyer time costs more than a month of this system. One lawyer reviewing one document costs more than running the full adversarial review pipeline 10 times.

**[Detailed cost breakdown →](https://github.com/jackneil/wepublic_defender/wiki/Cost-Guide)**

## Documentation

**📚 [GitHub Wiki - Complete Documentation](https://github.com/jackneil/wepublic_defender/wiki)**

**Getting Started:**
- [Complete Beginner Setup](https://github.com/jackneil/wepublic_defender/wiki/Complete-Beginner-Setup) - Assumes zero technical knowledge
- [Installation Guide](https://github.com/jackneil/wepublic_defender/wiki/Installation-Guide) - Technical setup details
- [Getting Started](https://github.com/jackneil/wepublic_defender/wiki/Getting-Started) - Quick orientation
- [Basic Usage](https://github.com/jackneil/wepublic_defender/wiki/Basic-Usage) - Common workflows

**Core Features:**
- [File Organization](https://github.com/jackneil/wepublic_defender/wiki/File-Organization) - How the system organizes your case
- [Review Pipeline](https://github.com/jackneil/wepublic_defender/wiki/Review-Pipeline) - Deep dive into adversarial review
- [Deep Research Workflow](https://github.com/jackneil/wepublic_defender/wiki/Deep-Research-Workflow) - Comprehensive legal research process
- [Session Start Automation](https://github.com/jackneil/wepublic_defender/wiki/Session-Start-Automation) - Claude remembers your case

**Reference:**
- [Slash Commands Reference](https://github.com/jackneil/wepublic_defender/wiki/Slash-Commands-Reference) - All available commands
- [API Reference](https://github.com/jackneil/wepublic_defender/wiki/API-Reference) - Technical API documentation
- [Configuration](https://github.com/jackneil/wepublic_defender/wiki/Configuration) - Customizing settings
- [Troubleshooting](https://github.com/jackneil/wepublic_defender/wiki/Troubleshooting) - Common errors and fixes

**Advanced:**
- [Advanced Features](https://github.com/jackneil/wepublic_defender/wiki/Advanced-Features) - Power user capabilities
- [Best Practices](https://github.com/jackneil/wepublic_defender/wiki/Best-Practices) - Tips for effective use
- [Code Examples](https://github.com/jackneil/wepublic_defender/wiki/Code-Examples) - Real-world usage patterns

## Real Talk: What This Is and Isn't

**This IS:**
- Multiple AI lawyers arguing over your case
- Automated citation checking against real legal databases
- Document review that catches what humans miss
- Case organization that keeps you on track
- Strategic guidance based on millions of similar cases
- A way to not get steamrolled by corporate lawyers

**This is NOT:**
- A replacement for a lawyer in complex cases
- Legal advice (it's legal research and review)
- A guarantee you'll win
- Perfect (but neither are lawyers)

**The Bottom Line**: The AIs make mistakes. But they make *different* mistakes, and they catch each other's mistakes. By the time they all agree your document is ready, it's been through more scrutiny than most lawyer-drafted documents.

## Disclaimer (The Boring But Legally Necessary Part)

This software is provided "as is" without warranty of any kind. Using AI for legal work is your decision and your responsibility. The developers are not liable for any outcomes of your case.

This is not legal advice. This is not a lawyer. This is a tool that helps you research and review your work before filing. The court will hold you to the same standards as a licensed attorney. If you file garbage, you'll get sanctioned, and "the AI did it" is not a defense.

**When in doubt, consult a real lawyer.** Yes, they're expensive. Yes, it sucks. But getting your case dismissed because you screwed up procedure sucks more.

## Terms of Use

By using WePublicDefender, you agree that you will NOT use this software to sue:

1. **Jack Neil** (the guy who built this because he got screwed by Capital One)
2. **Hank.ai** (his company)
3. **Any of Jack's friends** (file an issue on GitHub to get the current list)

If you violate this term, your license to use this software terminates immediately.

**Why this matters**: You're getting sophisticated legal tech for free. The trade-off is you can't weaponize it against the people who built it. Seems fair.

---

**Built by [Jack Neil](https://github.com/jackneil) • [Report Issues](https://github.com/jackneil/wepublic_defender/issues) • [Hank.ai](https://hank.ai)**

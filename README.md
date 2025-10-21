# WePublicDefender: Your AI Legal War Room

**Imagine having 5 lawyers review your case - one finding weaknesses, another verifying every citation, a third acting as opposing counsel trying to destroy your arguments, a fourth suggesting strategy, and a fifth making sure everything's perfect. Now imagine they're all AI, working 24/7, and arguing with each other until your legal documents are bulletproof.**

That's WePublicDefender. And it costs less than one hour with a real lawyer.

## The Secret Weapon: Adversarial AI That Fights Itself

So you got screwed by a corporation and can't afford a $400/hr lawyer. Here's what changes everything: WePublicDefender doesn't just use AI - it uses **multiple AIs that actively fight each other** over your case.

### 🥊 The Self-Improving AI Pipeline (This Is Where It Gets Insane)

This isn't just "multiple AIs reviewing your document." It's an **iterative refinement pipeline** where Claude Code orchestrates, participates, analyzes, fixes, and validates until your document is bulletproof.

**THE MASTER LOOP:**
```
DO {
  Run Phase 1: Document Organization
  Run Phase 2: Self-Review (iterate until clean)
  Run Phase 3: Citation Verification (iterate until valid)
  Run Phase 4: Opposing Counsel (iterate until defensible)
  Run Phase 5: Final Validation

  changes_made = count_all_fixes()
} WHILE (changes_made > 0)

// ONLY exits when ENTIRE pipeline passes with ZERO changes
```

**Phase 1: Claude Reads EVERYTHING**
- Reads all 47 documents in your case folder
- Organizes them into proper legal structure
- Extracts facts, parties, claims, deadlines
- Gets your jurisdiction/court/circuit details
- Builds initial case strategy

**Phase 2: Iterative Self-Review Loop**
```
REPEAT UNTIL PERFECT:
  1. Claude reviews document itself
  2. GPT-5 reviews independently
  3. Grok-4 reviews independently
  4. [Optional: Gemini, Mistral, Llama review]
  5. Claude analyzes all results:
     - Consensus issues (everyone found) → MUST FIX
     - Disputed issues (some found) → INVESTIGATE
     - Unique issues (only one found) → EVALUATE
  6. Claude AUTOMATICALLY FIXES the issues
  7. If still has problems → LOOP BACK TO STEP 1
  8. Else → Move to next stage
```

**Phase 3: Citation Verification Loop**
```
REPEAT UNTIL ALL CITATIONS VALID:
  1. Claude + External AIs verify every citation
  2. Web search for current case law status
  3. Replace overruled cases automatically
  4. Re-verify all citations
  5. Continue until 100% good law
```

**Phase 4: Opposing Counsel Attack Loop**
```
REPEAT UNTIL DEFENSIBLE:
  1. "BigLaw AI" attacks your case viciously
  2. Claude identifies vulnerabilities
  3. Claude strengthens weak points
  4. Re-run opposing counsel attack
  5. Continue until no fatal flaws
```

**Phase 5: Final Pipeline Validation**
```
RUN ENTIRE PIPELINE AGAIN:
  - All stages must pass
  - All models must agree
  - If any issues → iterate affected stages
  - Result: 10th draft quality minimum
```

### 🔴 The Golden Rule: ALWAYS Re-Validate After ANY Changes

**If the pipeline made ANY fixes, it MUST run again from the beginning. No exceptions.**

```python
# The ACTUAL pipeline logic:
DO {
    run_complete_pipeline()  # All 5 phases
    fixes_made = track_all_changes()
} WHILE (fixes_made > 0)

# Only exits when ENTIRE pipeline runs with ZERO changes needed
```

**Why This Is Non-Negotiable:**

Legal documents are **interconnected systems** where changing one thing affects everything:
- Fix a jurisdiction issue → might affect standing arguments
- Fix a citation → might weaken a legal theory
- Strengthen an argument → might create inconsistency elsewhere
- Add a counter-argument → might contradict earlier position

**The Only Way to Be Sure: Full Re-Validation**

```
Pipeline Run #1: Found 19 issues → Fixed them → RESTART
Pipeline Run #2: Found 5 issues → Fixed them → RESTART
Pipeline Run #3: Found 1 issue → Fixed it → RESTART
Pipeline Run #4: Found 0 issues → DONE ✅
```

**What This Prevents:**
- **Regression bugs**: Fix didn't break something else
- **Incomplete fixes**: Change didn't fully solve the problem
- **Cascade effects**: Fix didn't create new issues downstream
- **Hidden dependencies**: Change didn't affect related sections

**This is why WePublicDefender is bulletproof** - it NEVER assumes a fix is good. It validates, re-validates, and validates again until achieving a perfect zero-defect pass through the entire pipeline.

### 🎯 What This System Actually Catches (Real Examples)

**Procedural Landmines That Kill Cases:**
- "Your motion cites *Smith v. Jones* for qualified immunity, but that case was overruled in 2023"
- "You're in South Carolina but citing Ninth Circuit precedent as controlling authority"
- "Your complaint asks for $75,001 in diversity jurisdiction, but you forgot to allege citizenship properly"
- "You have 14 days to amend after this motion, not 21 - that's state court rules you're thinking of"

**The Opposing Counsel AI is Ruthless:**
```
"I found 3 ways to get this dismissed immediately:
1. You didn't plead fraud with particularity under Rule 9(b)
2. Your emotional distress claim fails without physical injury (South Carolina law)
3. The arbitration clause in paragraph 47 of their terms makes this entire filing void"
```

### 💪 Capabilities That Seem Like Magic (But Aren't)

**📚 Handles Massive Documents**: Got a 300-page credit report PDF? The system converts it to images, reads every page, and identifies the violations. Capital One sends 500 pages of discovery? No problem.

**🔄 Iterative Refinement**: The system doesn't just review once. It reviews, fixes issues, reviews again, fixes more, reviews again - up to 10 rounds until all AIs agree your document is solid. Like having an obsessive legal team.

**💰 Tracks Every Penny**: See exactly what each AI review costs. Most documents cost $2-5 for complete multi-AI review. Your lawyer charges that per word they write.

**🗂️ Manages Your Entire Case**:
- Organizes documents automatically (Pleadings, Discovery, Evidence, etc.)
- Maintains a timeline of everything that's happened
- Updates strategy recommendations as your case evolves
- Remembers what was filed, when, and what's due next

**🔍 Live Legal Research**: The AIs have web access. They search current case law, verify citations are still good, find recent similar cases, and update their advice based on last week's rulings.

**🤖 Claude Code Integration**: Works seamlessly with Claude. Just type `/review my_motion.md` and watch the AI war room activate. Claude orchestrates everything and explains what's happening in plain English.

### 📊 A Real Review Session (What You'll Actually See)

```
You: /review my_motion_to_dismiss.md

=== PHASE 1: DOCUMENT ORGANIZATION ===
📚 Claude: Reading 47 documents in case folder...
📁 Claude: Organizing into legal structure...
🎯 Claude: Extracting case facts and strategy...
⚖️ Claude: Jurisdiction: S.C. Federal, 4th Circuit

=== PHASE 2: SELF-REVIEW LOOP ===

--- Iteration 1 ---
🤖 Claude (internal): Found 8 issues
🔴 GPT-5: Found 12 issues
🟡 Grok-4: Found 10 issues
📊 CONSENSUS: 6 critical issues ALL models found
🔧 Claude: Fixing these 6 critical issues...

--- Iteration 2 ---
🤖 Claude: Found 2 issues
🟡 GPT-5: Found 3 issues
🟢 Grok-4: Found 2 issues
📊 CONSENSUS: 1 major issue to fix
🔧 Claude: Fixing jurisdiction statement...

--- Iteration 3 ---
✅ Claude: Clean
✅ GPT-5: Clean
🟢 Grok-4: 1 minor typo
📊 CONSENSUS: Ready for citations
➡️ Moving to Citation Verification...

=== PHASE 3: CITATION VERIFICATION LOOP ===

--- Iteration 1 ---
⚠️ Citation Check: 3 cases overruled!
🔍 Web Search: Finding replacement cases...
🔧 Claude: Replacing with good law...

--- Iteration 2 ---
✅ All 15 citations verified good law
➡️ Moving to Opposing Counsel...

=== PHASE 4: OPPOSING COUNSEL ATTACK ===

--- Iteration 1 ---
👿 BigLaw AI: "Arbitration clause kills this"
🛡️ Claude: Adding arbitration waiver argument...

--- Iteration 2 ---
😤 BigLaw AI: "Weak but no fatal flaws"
✅ Document defensible
➡️ Final validation...

=== PHASE 5: COMPLETE PIPELINE RE-RUN #1 ===
⚠️ Changes were made - must validate entire pipeline...

[Fast-forward through Phases 1-4]
✅ Organization: No changes
🔧 Self-Review: Fixed 1 minor formatting issue
✅ Citations: All valid
✅ Opposing: Defensible

⚠️ Pipeline made changes - MUST RUN AGAIN

=== COMPLETE PIPELINE RE-RUN #2 ===
♻️ Restarting from Phase 1 due to changes...

[Fast-forward through all phases]
✅ Organization: No changes
✅ Self-Review: No issues
✅ Citations: All valid
✅ Opposing: No vulnerabilities
✅ Final: No changes needed

🎉 CLEAN PASS - DOCUMENT READY TO FILE!

📊 FINAL STATISTICS:
- Pipeline Runs: 3 complete passes
- Total Iterations: 11
- Issues Fixed: 20
- API Calls: 42
- Total Cost: $12.83
- Time: 9 minutes
- Equivalent: 15th draft with zero defects
- Lawyer Cost Equivalent: $3,600 (9 hours @ $400/hr)
```

### 🎪 The Features That Make Lawyers Nervous

**Deep Research Mode**: Generates comprehensive legal research prompts, sends them to Claude's research mode, gets back 50+ page analyses with citations, then organizes everything for you.

**Multi-Jurisdiction Aware**: Knows federal vs. state rules. Knows which circuit you're in. Knows local court rules. Warns you when you're citing the wrong authority.

**Procedural Deadline Tracking**: Knows the difference between calendar days and court days. Knows when clock stops for service. Warns you about lesser-known deadlines.

**Settlement vs. Trial Strategy**: Different AIs for different goals. One maximizes settlement value, another prepares for trial. They argue about which approach is better for your situation.

### 🚀 Why This Is Revolutionary

**Traditional Pro Se**: You write a document → You file it → Judge dismisses it for procedural errors → Game over

**With WePublicDefender**: You write → 5 AIs attack it → Fix issues → AIs attack again → Fix more → Repeat until bulletproof → File with confidence

You're not filing your first draft. You're filing your tenth draft after surviving an AI firing squad where one AI is literally programmed to think like opposing counsel trying to destroy you.

### 🔮 The Iterative Refinement Magic (Why Lawyers Should Be Terrified)

**This is Test-Driven Development for Legal Documents**. Every software engineer knows TDD produces bulletproof code. Now that same principle produces bulletproof legal documents.

**How Consensus Building Works:**
```
Issue found by ALL models (100% consensus):
  → Critical issue, MUST fix immediately
  → Example: "Missing jurisdiction statement"

Issue found by MOST models (60-80% consensus):
  → Important issue, should investigate
  → Example: "Weak causation argument"

Issue found by ONE model (unique finding):
  → Potential blind spot, evaluate validity
  → Example: "Consider alternative remedy"
```

**The Convergence Principle:**
- Iteration 1: 20 issues found → Fix them
- Iteration 2: 8 issues found → Fix them
- Iteration 3: 2 issues found → Fix them
- Iteration 4: 0 critical issues → Move to next stage
- Final: All models agree → READY TO FILE

**Why Multiple Models Matter:**
- GPT-5 excels at: Legal reasoning, precedent analysis
- Grok-4 excels at: Real-time law updates, web search
- Claude excels at: Document organization, strategy
- Gemini (when added): Case pattern matching
- Mistral (when added): Multilingual law, EU precedents
- Each model has different training data = different perspectives

**The Statistical Confidence:**
```python
if issue_found_by == ["GPT-5", "Grok-4", "Claude", "Gemini"]:
    confidence = 99.9%  # Definitely a real issue
elif issue_found_by == ["GPT-5", "Grok-4"]:
    confidence = 75%    # Probably important
elif issue_found_by == ["Claude"]:
    confidence = 40%    # Worth considering
```

**What Makes This Unbeatable:**
1. **Automatic Fixing**: Claude doesn't just find problems - it FIXES them
2. **Verification Loops**: After fixing, ALL models re-review to confirm
3. **No Human Fatigue**: Can iterate 50 times if needed, never gets tired
4. **Adversarial Testing**: One AI's job is literally to destroy your case
5. **Continuous Learning**: Each iteration makes the document stronger

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

### 💸 The Math That Matters

- **Lawyer reviewing your motion**: 3 hours @ $400/hr = $1,200
- **WePublicDefender full review**: 5 AI models, 3 rounds = ~$5
- **Lawyer missing a citation issue**: Your case gets dismissed
- **5 AIs checking each other**: One will catch it

You still need to understand your case. You still need to verify everything. But now you have an AI war room that costs less than parking at a law firm.

### 🚀 Infinitely Extensible (Add More Firepower)

**The More Models, The Higher The Confidence**

WePublicDefender can use ANY LLM that has an API. Each new model you add increases the statistical confidence of the consensus. Here's what you can add:

**Currently Supported:**
- ✅ Claude (Anthropic) - Built-in orchestrator
- ✅ GPT-5, GPT-4o (OpenAI)
- ✅ Grok-4 (xAI)

**Easy to Add:**
- 🔜 Gemini Pro/Ultra (Google)
- 🔜 Mistral Large (Mistral AI)
- 🔜 Llama 3 405B (Meta via providers)
- 🔜 Command R+ (Cohere)
- 🔜 Any OpenAI-compatible API

**How to Add a New Model:**
```json
// Just add to .wepublic_defender/legal_review_settings.json
{
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-5", "grok-4", "gemini-ultra", "mistral-large"],
      // Now 4 models review = even higher confidence
    }
  }
}
```

**The Consensus Math Gets Stronger:**
- 3 models agree = 95% confidence
- 4 models agree = 98% confidence
- 5 models agree = 99.5% confidence
- 6+ models agree = You've basically had a jury trial

**Each Model Brings Different Strengths:**
- **Gemini**: Trained on academic papers, great at research
- **Mistral**: European law, GDPR, multilingual
- **Llama**: Open source, customizable, no rate limits
- **Command**: Document understanding, summarization
- **Your Custom Model**: Trained on your specific case type

**The Network Effect:**
```
More Models → More Perspectives → More Issues Caught →
Better Consensus → Higher Confidence → Stronger Documents
```

**Cost vs. Confidence Tradeoff:**
- Minimum (2 models): ~$3 per review, 90% confidence
- Standard (3-4 models): ~$5-8 per review, 95% confidence
- Maximum (6+ models): ~$15 per review, 99% confidence
- Still cheaper than 5 minutes with a lawyer

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

### 🧠 Claude Code 2.0.22+ Features

Recent Claude Code updates include powerful features for legal work:

#### Tab Key: Toggle Claude's Thinking Process

**What it does**: Press Tab to show/hide Claude's internal reasoning

**Why it matters for legal work:**
- See Claude's analysis before it proposes changes
- Understand WHY Claude recommends certain fixes
- Catch faulty reasoning before accepting suggestions
- Learn legal concepts by watching Claude reason through them

**How to use:**
```
1. Claude starts processing agent results
2. Press Tab → see Claude's reasoning appear in real-time
3. Press Tab again → hide reasoning, keep output clean
4. Review reasoning whenever uncertain about recommendations
```

**Example thinking you'll see:**
```
<thinking>
The opposing_counsel agent found the arbitration clause weakness.
I should check if we have any waiver arguments...
Looking at case timeline - defendant litigated merits for 3 months.
That's likely waiver of arbitration. Should add section addressing this.
</thinking>
```

**Best practice**: Keep thinking visible when processing complex agent results (citation verification, opposing counsel attacks). Hide it for simple tasks.

#### /bashes: Monitor Background Tasks

**What it does**: Shows all running background processes and their status

**Why it matters for legal work:**
- Long-running agent calls (external-llm mode) auto-background in Claude Code 2.0.22+
- Check if citation verification still running (can take 3-5 minutes with web search)
- Monitor multiple parallel agent calls
- Debug when processes seem stuck

**How to use:**
```
Type: /bashes

You'll see:
Shell ID | Command | Status | Runtime
---------|---------|--------|--------
bash_1   | wpd-run-agent citation_verify | Running | 2m 34s
bash_2   | wpd-run-agent opposing_counsel | Running | 1m 12s
```

**When to check:**
- Agent seems to be taking a long time
- Running multiple agents in parallel
- Want to verify process didn't crash
- Checking if web search is still working

**Common scenarios:**

*Citation verification with web search:*
```
You: /review draft.md

Claude runs citation_verify with web search...
[2 minutes pass]

You: /bashes

Shows: citation_verify still running, 3m 45s elapsed
Expected: 3-5 minutes for large documents, this is normal
```

*Multiple parallel agents:*
```
Claude: Running self_review and opposing_counsel in parallel...

You: /bashes

Shows:
- self_review: Complete, 2m 14s
- opposing_counsel: Running, 4m 56s

Wait for both to finish before processing results.
```

**No more timeout workarounds needed**: Claude Code 2.0.22+ automatically backgrounds long-running commands instead of killing them at 2 minutes. The /bashes command lets you monitor progress.

### Claude Remembers Your Case (No More Repeating Yourself)

**The best feature you'll never notice: Claude automatically knows what you were working on.**

When you open Claude Code in your case folder, Claude automatically:
- Reads what you worked on last session
- Checks for upcoming deadlines
- Looks for new files in your inbox
- Figures out what stage your case is in (pre-filing, discovery, trial prep, etc.)
- Offers you relevant next actions

**What you'll see:**

Instead of staring at a blank terminal wondering what to do, Claude greets you with clickable options:

```
I see you're in active discovery. What's your priority?

[ ] Respond to pending discovery requests (deadline: Oct 25 - in 5 days!)
[ ] Draft new interrogatories/document requests
[ ] Organize opponent's document production
[ ] Prepare for depositions
[ ] Other

Click an option to get started.
```

**No more:**
- "Where did we leave off?"
- "What was I working on?"
- "What files do I have?"
- Typing "1" or "2" like it's a phone menu from 1997

**Just:**
- Click what you want to do
- Claude does it

**Works on Windows, Mac, and Linux** - The system detects your operating system and sets everything up automatically during Step 1.

**Manual override:** Type `/start` anytime to refresh context and see options again.

## Table of Contents

- [How Claude Code Works - Choose Your Mode](#how-claude-code-works---choose-your-mode) - Understanding auto-accept, manual, and plan modes for legal work
- [Claude Remembers Your Case](#claude-remembers-your-case-no-more-repeating-yourself) - Automatic context loading and smart next actions
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

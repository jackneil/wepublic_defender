# !!! MANDATORY SESSION START - FIRST ACTION EVERY SESSION !!!

═══════════════════════════════════════════════════════════════════════════════
                            STOP AND READ THIS FIRST
═══════════════════════════════════════════════════════════════════════════════

## CRITICAL: IS THIS YOUR FIRST RESPONSE IN THIS SESSION?

**BEFORE responding to the user, answer this question:**

→ **Have you loaded context from session_notes.md, case_timeline.md, and GAMEPLAN.md yet?**

   **NO?** → **STOP RIGHT NOW AND DO THIS:**

   1. Read `.claude/SESSION_START_MANDATORY.md` (10 seconds)
   2. Follow `.claude/workflows/session_start_checklist.md` (30 seconds)
   3. THEN respond to user with stage-appropriate options

   **THIS WORKS IN PLAN MODE** - Reading files is non-destructive and allowed!

   **YES?** → You already ran the checklist, proceed with user's request

═══════════════════════════════════════════════════════════════════════════════

**Why this is MANDATORY:**

- Users shouldn't have to explain context every session
- You need to know what was worked on last time
- You need to see upcoming deadlines
- You should proactively offer relevant next actions
- This makes the user's life easier

**How to verify you did this:**

After running session start checklist, you should know:
- [ ] What was worked on last session (from session_notes.md)
- [ ] Recent case events (from case_timeline.md)
- [ ] Upcoming deadlines (from GAMEPLAN.md)
- [ ] What files are in inbox (from 00_NEW_DOCUMENTS_INBOX/)
- [ ] Current case stage (PRE-FILING, DISCOVERY, MOTION PRACTICE, TRIAL PREP, GENERAL)

If you don't know these things and this is your first message, GO TO `.claude/SESSION_START_MANDATORY.md` NOW.

═══════════════════════════════════════════════════════════════════════════════

# Legal Case Management - Claude Code Orchestrator

**You are assisting with a legal case using the wepublic_defender system.**

This file provides core configuration and conditional logic to load the appropriate workflow for each situation.

---

## Session Start Mechanisms (Multiple Redundant Layers)

### Layer 1: SessionStart Hook (Automatic)
- `.claude/hooks/SessionStart` fires when Claude Code opens (if hooks enabled)
- Outputs instructions to follow `session_start_checklist.md`
- Most reliable method when hooks are working

### Layer 2: SESSION_START_MANDATORY.md (Failsafe)
- If hook didn't fire, the giant warning above should catch you
- Points to `.claude/SESSION_START_MANDATORY.md` for quick reference
- Works EVEN IN PLAN MODE (reading is allowed)

### Layer 3: Manual Override (/start command)
- User can type `/start` anytime to re-run session checklist
- Useful after long sessions or when context is stale
- Backup if automation fails

**The goal: Make it impossible for you to skip session start and make users repeat themselves.**

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

## 📊 Session & Case Tracking Protocol (CRITICAL - UPDATE CONSTANTLY)

**TWO tracking files that MUST be kept updated throughout every session:**

### 1. Session Notes (`.wepublic_defender/session_notes.md`)

**Purpose**: Work tracking + crash recovery - your working memory and fallback if session crashes

**Critical Use Case**: If Claude crashes mid-session, user can restart and Claude reads this file to know:
- What task was being worked on
- What the user's last request was
- Recent context and decisions
- What's been completed this session

**Update Triggers** - Update IMMEDIATELY after:
- Any agent invocation (self_review, citation_verify, opposing_counsel, drafter, etc.)
- Any slash command (/organize, /review, /research, /draft, /strategy, etc.)
- Completing any major research or drafting task
- Finishing any document review or revision
- Any significant work that takes >2 minutes
- **BEFORE starting any task** (update "Currently Working On")
- **IMMEDIATELY after user makes a request** (update "Last User Request")

**How to Update**:

1. **Currently Working On** section:
   - When starting work: Add item to this section
   - While working: Keep item here
   - When finished: Move to "Completed This Session"
   - Always keep this current - it's the crash recovery anchor

2. **Last User Request** section:
   - Update with exact user request when they ask for something
   - Preserves context if session crashes mid-task

3. **Recent Context** section:
   - Important findings, blockers, decisions
   - Things to remember for later in session
   - Key context that affects future work

4. **Completed This Session** section:
   - Add timestamp when completing work
   - Brief description of what was accomplished
   - Most recent items at top (reverse chronological)

**Example Update After Agent Run**:
```markdown
## 🎯 Currently Working On

- [Nothing in progress - waiting for user direction]

## ✅ Completed This Session

### 2025-10-14 14:32
- **Self-review agent (external-llm mode)**: Reviewed MOTION_TO_DISMISS_v3.md
  - Found 2 critical issues (missing jurisdiction statement, weak legal standard)
  - 4 major issues, 8 minor issues
  - Detailed output in .wepublic_defender/reviews/

### 2025-10-14 13:15
- **Research**: Completed qualified immunity standard research
  - Found 5 key Fourth Circuit cases
  - Updated 06_RESEARCH/qualified_immunity_notes.md
```

**Update Method**:
- Use Edit tool to update the file (remember backslashes on Windows!)
- Read current state first, then append/modify
- Keep format clean and scannable

---

### 2. Case Timeline (`.wepublic_defender/case_timeline.md`)

**Purpose**: Permanent historical record of MAJOR COMPLETED case events - NOT work in progress

**⚠️ CRITICAL DISTINCTION**: This is for completed major events that matter to case history. Track work-in-progress in session_notes.md instead.

**✅ DO add to timeline:**
- Documents FILED with court
- Documents RECEIVED from court/opposing counsel
- Communications SENT to court/opposing counsel
- Major research COMPLETED (ready to use for drafting)
- Court events (hearings, oral arguments, deadlines)
- Discovery exchanged
- Strategic pivots

**❌ DO NOT add to timeline:**
- Draft versions (v1, v2, v3) - track those in session_notes.md
- Work in progress
- Minor research tasks
- Internal discussions
- File organization

**Entry Format**:
```markdown
### YYYY-MM-DD HH:MM - [EVENT_TYPE] - Brief Description

**Status**: Filed | Received | Sent | Completed
**Category**: Pleading | Discovery | Evidence | Communication | Research | Court Event | Strategy
**File**: path/to/document (if applicable)
**Notes**: Additional context relevant to case history

---
```

**Event Types**:
- 📄 DOCUMENT - Document filed or received (not drafts!)
- 📨 COMMUNICATION - Email, letter sent/received
- ⚖️ COURT_EVENT - Hearing, order, deadline
- 🔍 RESEARCH - Major research completed
- 📋 DISCOVERY - Discovery exchanged
- 🎯 STRATEGY - Strategic decision

**Example Timeline Entries (Major Completed Events Only)**:
```markdown
### 2025-10-15 09:00 - 📄 DOCUMENT - Motion to Dismiss Filed

**Status**: Filed
**Category**: Pleading
**File**: 02_PLEADINGS/03_Motions/2025-10-14_MotionToDismiss_FINAL.pdf
**Notes**: Filed via CM/ECF, case number 1:25-cv-00123. Hearing scheduled for 2025-11-05.

---

### 2025-10-14 12:00 - 📨 COMMUNICATION - Discovery Extension Request Sent

**Status**: Sent
**Category**: Communication
**File**: 05_CORRESPONDENCE/01_With_Opposing_Counsel/2025-10-14_Discovery_Extension_Request.pdf
**Notes**: Requested 30-day extension for discovery responses. Opposing counsel agreed verbally, confirming in writing.

---

### 2025-10-12 09:00 - ⚖️ COURT_EVENT - Order Granting Motion to Compel

**Status**: Received
**Category**: Court Event
**File**: 02_PLEADINGS/04_Orders/2025-10-12_Order_Granting_Motion_to_Compel.pdf
**Notes**: Court granted our motion to compel. Defendant must produce financial records within 14 days (deadline: 2025-10-26).

---

### 2025-10-10 16:00 - 🔍 RESEARCH - Qualified Immunity Standard Research Completed

**Status**: Completed
**Category**: Research
**File**: 06_RESEARCH/qualified_immunity_notes.md
**Notes**: Researched Fourth Circuit qualified immunity standard. Found 5 key cases supporting our position. Ready to incorporate into motion drafting.

---
```

**Remember**: Draft versions (v1, v2, v3) get tracked in `session_notes.md`, NOT here. Only add to timeline when document is FILED or major research is COMPLETED and ready to use.

**Update Method**:
- Always insert new entries at TOP (reverse chronological)
- Keep existing entries intact (never delete history)
- Use consistent formatting
- Include enough detail to understand event later

---

### Integration with Existing Tracking

These files COMPLEMENT (not replace) existing tracking:

- `.database/file_management_log.md` - File movements and organization actions
- `.database/file_management_index.json` - Index of processed files
- `.wepublic_defender/usage_log.csv` - API usage and costs
- `.wepublic_defender/reviews/` - Agent review outputs

**Relationship**:
- `session_notes.md` = "What am I doing RIGHT NOW and what did I just finish?"
- `case_timeline.md` = "What happened in this case and when?"
- `.database/` files = "What files have been moved/processed?"

---

### When to Update (Checklist)

**✅ ALWAYS update `session_notes.md` after:**
- EVERY agent run (what it found/did)
- EVERY slash command (what happened)
- Starting ANY task (update "Currently Working On")
- Completing ANY task (move to "Completed This Session")
- User makes a request (update "Last User Request")
- Any significant work that takes >2 minutes

**✅ ONLY update `case_timeline.md` for major completed events:**

**Documents:**
- When FILED with court → Add entry
- When RECEIVED from court/opposing counsel → Add entry
- ❌ NOT when drafting (v1, v2, v3) - track in session_notes instead
- ❌ NOT when finalizing - only when FILED

**Communications:**
- Email/letter SENT to court/opposing counsel → Add entry
- Email/letter RECEIVED from court/opposing counsel → Add entry

**Research:**
- Major research COMPLETED and ready to use → Add entry
- ❌ NOT work-in-progress research - track in session_notes instead

**Court Events:**
- Court order RECEIVED → Add entry
- Hearing scheduled → Add entry
- Deadline imposed by court → Add entry

**Discovery:**
- Discovery request/response EXCHANGED → Add entry

**Strategy:**
- Major strategic decision made → Add entry

**Remember the distinction:**
- `session_notes.md` = Everything you're doing right now (drafts, revisions, work in progress)
- `case_timeline.md` = Major events that are complete and matter to case history (filings, orders, completed research)

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

### Special Cases: Agents That ONLY Support Guidance Mode

**`organize` and `fact_verify` agents ONLY operate in guidance mode** - external LLMs cannot access file system.

- `organize`: Needs to read/move files on disk
- `fact_verify`: Needs to read evidence documents from `04_EVIDENCE/` to verify claims

If you try `--mode external-llm` with these agents, they auto-fall back to guidance with warning.

---

## 🤖 Agent Orchestration Protocol (CRITICAL - READ AFTER EVERY AGENT RUN)

**AFTER EVERY AGENT INVOCATION, YOU MUST CHECK FOR AND FOLLOW AGENT INSTRUCTIONS:**

When you run any agent via `wpd-run-agent` or CLI commands, the agent result contains an optional `claude_prompt` field that tells you what to do next.

### 🔴 PIPELINE RE-VALIDATION ORCHESTRATION

**THE GOLDEN RULE**: If ANY agent made changes, you MUST re-run the ENTIRE pipeline from the beginning.

#### How to Track Pipeline Changes:

```python
# Your mental model for tracking:
pipeline_changes = {
    "run_number": 1,
    "phase_1_self_review": 0,
    "phase_2_citations": 0,
    "phase_3_opposing": 0,
    "phase_4_final": 0,
    "total": 0
}

# After each agent run, check claude_prompt:
if "Must fix" in claude_prompt or "Will need to replace" in claude_prompt:
    # Extract number and add to total
    changes = extract_number_from_prompt()
    pipeline_changes["total"] += changes
```

#### Decision Tree After Each Agent:

```
Agent returns claude_prompt
    ↓
Contains "Must fix X" or "Will need to replace X"?
    YES → Fix issues, track changes
    NO → Check "CLEAN PASS"?
        ↓
After ALL phases complete:
    ↓
Total changes > 0?
    YES → RESTART ENTIRE PIPELINE FROM PHASE 1
    NO → PROCEED TO FINALIZATION
```

#### Example Pipeline Execution:

```
=== PIPELINE RUN #1 ===
Self-Review: "Must fix 3 critical issues" → Fix them → Changes: 3
Citations: "Replace 2 bad citations" → Replace them → Changes: 2
Opposing: "Fix 1 weakness" → Strengthen → Changes: 1
Fact Verify: "Wrong date, unsupported claim" → Fix them → Changes: 2
Final: "Fix formatting" → Fix it → Changes: 1
Total: 9 changes → ⚠️ MUST RESTART FROM PHASE 1

=== PIPELINE RUN #2 ===
Self-Review: "Fix 1 major issue" → Fix it → Changes: 1
Citations: "CLEAN PASS" → Changes: 0
Opposing: "CLEAN PASS" → Changes: 0
Fact Verify: "CLEAN PASS" → Changes: 0
Final: "CLEAN PASS" → Changes: 0
Total: 1 change → ⚠️ MUST RESTART FROM PHASE 1

=== PIPELINE RUN #3 ===
Self-Review: "CLEAN PASS" → Changes: 0
Citations: "CLEAN PASS" → Changes: 0
Opposing: "CLEAN PASS" → Changes: 0
Fact Verify: "CLEAN PASS" → Changes: 0
Final: "CLEAN PASS" → Changes: 0
Total: 0 changes → ✅ PROCEED TO FINALIZATION
```

#### Key Phrases in claude_prompt That Require Action:

**Indicates changes needed (and pipeline re-run):**
- "Must fix X critical issues"
- "Will need to replace X citations"
- "Should fix X major weaknesses"
- "After fixing, you MUST re-run the ENTIRE pipeline"

**Indicates clean pass (but check total):**
- "CLEAN PASS - NO CHANGES NEEDED"
- "All citations verified as good law"
- "No critical or major weaknesses"
- "If ANY previous phases made changes, you MUST re-run entire pipeline"

#### Why This Matters:

Legal documents are **interconnected systems** where:
- Fixing jurisdiction affects standing
- New citations might not support revised arguments
- Strengthening one argument can contradict another
- Only a ZERO-CHANGE pass guarantees consistency

**NEVER** skip re-validation. **ALWAYS** restart from Phase 1 if changes were made.

### How It Works

1. **Agents have domain expertise** - They know what their findings mean and can guide your next actions
2. **You orchestrate the workflow** - Check the `claude_prompt` field after each agent run
3. **Follow agent guidance** - The prompts tell you to summarize findings, ask questions, or recommend next steps

### Example Agent Outputs

#### Self Review Found Critical Issues
```json
{
  "agent": "self_review",
  "structured": {"critical_issues": ["Missing jurisdiction", "No legal standard"], ...},
  "claude_prompt": "Found 2 CRITICAL issues that must be fixed before filing: Missing jurisdiction; No legal standard. Also 3 major and 5 minor issues. Present the critical issues as a bulleted list and ask if I should research solutions or if the user wants to review the full output first."
}
```

**What to do:** Follow the prompt! List the critical issues, ask the user how they want to proceed.

#### Citation Verification Passed
```json
{
  "agent": "citation_verify",
  "structured": [{...}, {...}],
  "claude_prompt": "All 5 citations verified as good law and supporting our position. Briefly confirm this success and ask if user wants to proceed with next review step (opposing_counsel)."
}
```

**What to do:** Confirm success to user, offer to run opposing_counsel next.

### When Agent Returns `claude_prompt`

✅ **DO:**
- Read and follow the prompt instructions
- Summarize findings for the user
- Ask questions the prompt suggests
- Recommend next actions from the prompt

❌ **DON'T:**
- Ignore the prompt and just say "Agent run complete"
- Run next agent without user feedback if prompt asks questions
- Blindly accept findings without the critical analysis the prompt may request

### Why This Matters

Agents with domain knowledge (legal review, citation verification) can intelligently guide the orchestration workflow based on what they find. This prevents you from just executing bash commands silently - you'll provide context-aware summaries and recommendations after each step.

### ⚠️ AFTER FOLLOWING AGENT GUIDANCE: UPDATE TRACKING FILES

**MANDATORY after EVERY agent run:**

1. **Update `session_notes.md`**:
   - Add what agent found/did to "Completed This Session"
   - Clear "Currently Working On" if task is complete
   - Update "Recent Context" if agent revealed blockers or important findings

2. **Update `case_timeline.md` ONLY if major event occurred**:
   - Document finalized and FILED with court
   - Major research COMPLETED and ready to use
   - ❌ NOT for drafts, work in progress, or reviews

This ensures crash recovery works and case history stays current. See "Session & Case Tracking Protocol" section above for full details.

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

## 🪟 Windows Unicode (CRITICAL)

**Windows console crashes on Unicode characters (cp1252 encoding).**

**NEVER use in output:**
- Emojis: 🔴 ✅ 📄 ⚠️ → Use text: [CRITICAL] [OK] WARNING:
- Bullets: • ● ▪ → Use: - * >
- Checkboxes: ☐ ☑ ✓ → Use: [ ] [X]
- Special chars: — " " ' ' → Use: -- " " ' '

**Rule: If it's not on a US keyboard, don't print it to console.**

Stick to: A-Z, 0-9, and basic symbols: - * [ ] ! ? . , : ; " ' ( ) / \ | _

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
     "conda_env": "wepublic_defender"
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
- **`/timeline [action]`** - View/update case timeline and document history
- **`/deep-research-prep`** - Generate comprehensive prompt for Claude.ai Deep Research
- **`/research [topic]`** - Quick legal research on specific topic
- **`/strategy`** - Get strategic recommendations
- **`/draft [type]`** - Draft legal document
- **`/review [file]`** - Run adversarial review

### Utility Commands

- **`wpd-pdf-to-images <pdf_path>`** - Convert large PDF to images for Claude to read
  - Use when PDFs are too large (>25K tokens) for Claude to process directly
  - Common use cases: Credit reports, lengthy court orders, large exhibits
  - Example: `wpd-pdf-to-images "F:/capitalone/credit_report.pdf"`
  - Creates folder with numbered page images: `page_0001.png`, `page_0002.png`, etc.
  - Then use Read tool on individual pages: `Read(file_path="credit_report_images/page_0001.png")`

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

### PDF to Images Converter

When PDFs are too large for Claude to read directly (>25K tokens), convert them to images:

```bash
# Convert PDF to images (uses wpd-pdf-to-images command from setup.py entry point)
<python_path> -m wepublic_defender.utils.pdf_to_images "F:/path/to/document.pdf"

# Or use CLI command if installed
wpd-pdf-to-images "F:/path/to/document.pdf"

# Specify output directory
wpd-pdf-to-images "document.pdf" --output-dir "F:/images"

# Use higher quality
wpd-pdf-to-images "document.pdf" --dpi 300
```

**Common use cases:**
- Credit reports (often 50-100+ pages)
- Lengthy court orders or opinions
- Large discovery exhibits
- Settlement agreements with extensive attachments

**After conversion**, read individual pages:
```
Read(file_path="F:/path/to/document_images/page_0001.png")
Read(file_path="F:/path/to/document_images/page_0002.png")
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

### ⏱️ Long-Running Commands and Auto-Backgrounding

**Claude Code 2.0.22+ automatically backgrounds long-running bash commands.**

**No more manual timeout workarounds needed!** Claude monitors background tasks and can check their progress.

#### How It Works

Long-running commands (like external-llm agent calls) automatically move to background if they take too long:
- Bash tool auto-backgrounds instead of killing commands
- Claude monitors logs in real-time
- Can debug from logs when processes crash
- Use `/bashes` command to check running tasks

#### Running Agent Commands

**Simple - just run them:**

```python
# Automatically backgrounds if needed (citation verification with web search, etc.)
Bash(
    command="C:/Users/jack/.conda/envs/wepublic_defender/python.exe -m wepublic_defender.cli.run_agent --agent citation_verify --file draft.md --mode external-llm --web-search",
    description="Run citation verification"
)
```

**No more `timeout=600000` required** for most operations.

#### Checking Background Task Status

User can type `/bashes` to see:
- All running background shells
- Command being executed
- Runtime
- Status (running/completed)

#### When to Still Use Timeout

Rarely needed, but specify timeout if you need a command to fail after specific time:

```python
# Force timeout after 5 minutes (rare)
Bash(command="...", timeout=300000)
```

#### Incremental Result Saving

The CLI automatically saves each model's results immediately upon completion to `.wepublic_defender/reviews/` directory. This prevents data loss if process crashes.

Results are saved as:
- JSON: `.wepublic_defender/reviews/{agent}_{model}_{timestamp}.json`
- Markdown: `.wepublic_defender/reviews/{agent}_{model}_{timestamp}.md`

Even if command backgrounds or times out, completed models have results preserved.

---

## 📝 File Naming Conventions

- Use UPPERCASE for document types: `MOTION_TO_DISMISS.docx`
- Include dates for versions: `MOTION_TO_DISMISS_2025-10-15.docx`
- Use underscores, not spaces: `DISCOVERY_RESPONSE_01.docx`
- Use version numbers for drafts: `MOTION_v1.md`, `MOTION_v2.md`, `MOTION_FINAL.md`

---

## 💾 State Tracking (.database)

The `.database/` directory (per-case, in case root) tracks file management state to prevent duplicate work.

**Created during case initialization**. Contains:

**Ledger**: `.database/file_management_log.md`
- Format: `timestamp | action | src | dst | notes`
- Append one line per file management action
- Human-readable audit trail

**Index**: `.database/file_management_index.json`
- JSON object keyed by file path
- Tracks what's been processed to avoid duplicate work
- Quick lookup: "Have I processed this file?"

**README**: `.database/README.md`
- Explains purpose and usage
- Documents file formats

**Usage:**
- Read index before organizing to skip already-processed files
- Check during session start for organization stats
- Never commit `.database/` contents (gitignored)

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

═══════════════════════════════════════════════════════════════════════════════
                      FINAL SAFETY CHECK - DID YOU SKIP SESSION START?
═══════════════════════════════════════════════════════════════════════════════

**If you're reading this and it's your FIRST message in a new session:**

→ **Did you load context from session_notes.md, case_timeline.md, and GAMEPLAN.md?**

   **NO?** → You skipped session start! GO BACK TO TOP OF THIS FILE NOW!

   **YES?** → Great, proceed with user's request

═══════════════════════════════════════════════════════════════════════════════

**Now execute the workflow routing logic at the top of this file to determine your next action.**

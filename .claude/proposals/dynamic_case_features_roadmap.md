# Dynamic Case-Aware WePublicDefender Features Roadmap

**Status**: Proposed for implementation after PR #[TBD]
**Created**: 2025-10-20
**Priority**: High - Significantly improves UX and workflow intelligence

---

## Executive Summary

Transform WePublicDefender from command-driven to **intelligent case-aware assistant** that:
- Detects where user is in case lifecycle
- Presents contextually relevant options via multiple-choice questions
- Auto-activates stage-appropriate capabilities via Skills
- Validates work automatically via Hooks
- Accesses case data seamlessly via MCP server
- Applies deep reasoning strategically via Extended Thinking

**Key Innovation**: System adapts to case stage without user needing to know commands or workflows.

---

## New Claude Code Features to Leverage

### 1. Skills (October 2025)
- **What**: Modular capabilities that auto-activate based on context
- **How**: Create `.claude/skills/` with stage-specific skill files
- **Benefit**: Claude autonomously uses right tools at right time

### 2. Multiple Choice Questions (October 2025)
- **What**: Structured numbered options for user clarification
- **How**: Present 1-6 options based on detected case stage
- **Benefit**: Guides users through workflow intelligently

### 3. Hooks (June 2025)
- **What**: Shell commands that execute at lifecycle events
- **How**: `.claude/hooks/post-edit.sh` for auto-validation
- **Benefit**: Automatic quality gates without manual checks

### 4. MCP - Model Context Protocol (2025)
- **What**: Standardized data source connections
- **How**: Custom MCP server for case evidence folder
- **Benefit**: Natural language queries against case files

### 5. Extended Thinking / UltraThink (2025)
- **What**: Deep reasoning mode with serial test-time compute
- **How**: Trigger "ultrathink" for strategic analysis
- **Benefit**: Better quality for complex legal decisions

---

## Implementation Phases

### PHASE 1: Multiple Choice Questions (Week 1)
**Effort**: Low | **Impact**: High | **Code Changes**: None

#### Implementation
Update `.claude/workflows/session_start_checklist.md`:

```markdown
## 2. Detect Case Stage and Present Options

### Stage Detection Logic
Check these indicators to determine case stage:

PRE-FILING indicators:
- No 02_PLEADINGS/01_Complaint/ folder
- 04_EVIDENCE/ has files but no pleadings
- case_timeline.md shows investigation phase

DISCOVERY indicators:
- 03_DISCOVERY/ folder exists and has recent files
- case_timeline.md shows discovery deadlines
- Responses or requests pending

MOTION PRACTICE indicators:
- 02_PLEADINGS/03_Motions/ has files from last 30 days
- case_timeline.md shows motion deadlines
- Opposition briefs in drafts

TRIAL PREP indicators:
- case_timeline.md mentions "trial scheduled"
- 08_REFERENCE/ has trial exhibits
- Witness preparation documents exist

### Present Stage-Appropriate Options

[Detailed for each stage - see full implementation below]
```

#### Pre-Filing Stage Questions
```
I see you're investigating a potential case. What would you like to work on?

1. Organize evidence from inbox
2. Research case viability (deep research)
3. Calculate potential damages
4. Check statute of limitations
5. Identify potential claims
6. Something else (tell me what)

Choose 1-6:
```

#### Discovery Stage Questions
```
You're in active discovery. What's your priority?

1. Respond to pending discovery requests (list them)
2. Draft new interrogatories/document requests
3. Organize opponent's document production
4. Prepare for depositions
5. Check discovery deadlines
6. Something else (tell me what)

Choose 1-6:
```

#### Motion Practice Stage Questions
```
I see recent motion activity. How can I help?

1. Draft new motion (specify type)
2. Respond to opponent's motion (which one?)
3. Research motion standards
4. Review draft before filing (fact-check)
5. Prepare for oral argument
6. Something else (tell me what)

Choose 1-6:
```

#### Trial Prep Stage Questions
```
Trial preparation mode. What do you need?

1. Organize trial exhibits
2. Prepare witness examination outlines
3. Draft jury instructions
4. Create trial brief
5. Review pre-trial checklist
6. Something else (tell me what)

Choose 1-6:
```

**Testing**: Run session start in various case states, verify correct questions presented.

---

### PHASE 2: Skills (Week 2-3)
**Effort**: Medium | **Impact**: High | **Code Changes**: Config only

#### Create `.claude/skills/` Directory Structure

```
.claude/skills/
├── pre_filing_investigation/
│   └── SKILL.md
├── discovery_management/
│   └── SKILL.md
├── motion_practice/
│   └── SKILL.md
├── trial_preparation/
│   └── SKILL.md
└── fact_verification/
    └── SKILL.md
```

#### Skill: Pre-Filing Investigation

**File**: `.claude/skills/pre_filing_investigation/SKILL.md`

```yaml
---
name: Case Investigation Assistant
description: Use when case folder is new (no complaint filed yet), user mentions investigating claims, or asks about case viability. Helps gather facts, identify claims, assess damages, check statutes of limitations.
allowed-tools: [Read, Glob, Grep, Write]
---

# Pre-Filing Investigation Workflow

You are assisting with a potential case that hasn't been filed yet.

## Your Role
- Help organize evidence systematically
- Identify potential legal claims
- Calculate damages
- Check statute of limitations
- Assess case viability

## Checklist for New Cases

### 1. Evidence Organization
- [ ] Check 00_NEW_DOCUMENTS_INBOX/ for new files
- [ ] Organize evidence into 04_EVIDENCE/ by type:
  - Contracts/agreements
  - Communications (emails, letters)
  - Financial records (statements, receipts)
  - Expert reports
- [ ] Create evidence index

### 2. Fact Gathering
- [ ] Identify all parties (plaintiffs, defendants)
- [ ] Create chronological timeline of events
- [ ] Document damages with supporting evidence
- [ ] Identify witnesses

### 3. Claims Analysis
- [ ] Research potential causes of action
- [ ] Check jurisdiction and venue requirements
- [ ] Verify statute of limitations for each claim
- [ ] Assess strength of each potential claim

### 4. Damages Calculation
- [ ] Economic damages (documented losses)
- [ ] Lost profits or opportunities
- [ ] Emotional distress claims
- [ ] Punitive damages potential
- [ ] Attorney fees recoverability

### 5. Strategic Assessment
- [ ] Likelihood of success
- [ ] Defendant's ability to pay
- [ ] Costs vs. potential recovery
- [ ] Settlement vs. trial probability

## When User Asks About Case Viability

Recommend: `/deep-research-prep` for comprehensive analysis

This generates prompt for Claude.ai Deep Research covering:
- All potential claims
- Element-by-element analysis
- Damages assessment
- Strategic recommendations
```

#### Skill: Discovery Management

**File**: `.claude/skills/discovery_management/SKILL.md`

```yaml
---
name: Discovery Workflow Assistant
description: Use when 03_DISCOVERY folder has active requests/responses, user mentions discovery deadlines, or asks about interrogatories/document requests/depositions. Manages discovery workflow and deadline tracking.
allowed-tools: [Read, Write, Glob, Grep]
---

# Discovery Phase Management

You are managing active discovery in a filed case.

## Your Role
- Track discovery deadlines
- Draft responses to discovery requests
- Prepare discovery requests to opponent
- Organize produced documents
- Prepare for depositions

## Discovery Deadline Tracking

**Check case_timeline.md for:**
- Discovery cutoff date
- Pending responses due
- Opponent's responses due
- Deposition schedules

**Alert user if:**
- Deadline within 7 days
- Response overdue
- Extension needed

## Responding to Discovery

### Interrogatories
1. Read opponent's interrogatories
2. Search evidence for answers (04_EVIDENCE/)
3. Draft responses with objections
4. Cite specific evidence for each answer
5. Flag answers needing client input

### Document Requests
1. Review requests for scope
2. Search case files for responsive documents
3. Draft objections (privilege, burden, relevance)
4. Prepare document production log
5. Identify documents needing review

### Requests for Admission
1. Analyze each request carefully
2. Research facts to verify accuracy
3. Draft admits/denies with specificity
4. Object where appropriate
5. Flag dangerous admissions for review

## Drafting Discovery Requests

### Strategy First
- What facts do we need to prove?
- What damages need documentation?
- What does opponent know?
- What impeachment material exists?

### Interrogatory Drafting
- Specific, not compound questions
- Follow up on evasive answers
- Request details on defenses
- Pin down opponent's theory

### Document Request Drafting
- Broad enough to get everything
- Specific enough to be enforceable
- Include time periods
- Define terms clearly

## Deposition Preparation

**When user mentions deposition:**
1. Review all discovery produced
2. Identify gaps in opponent's story
3. Draft examination outline
4. Prepare exhibits for deposition
5. Research impeachment materials
```

#### Skill: Motion Practice

**File**: `.claude/skills/motion_practice/SKILL.md`

```yaml
---
name: Motion Strategy Assistant
description: Use when user mentions filing/responding to motions, 02_PLEADINGS/03_Motions has recent activity, or asks about motion standards. Provides motion-specific strategic guidance using extended thinking.
---

# Motion Practice Strategy

You are assisting with motion practice (filing or responding to motions).

## Your Role - Strategic Motion Analysis

When user mentions motion:
1. **Trigger extended thinking mode** for deep analysis
2. Research applicable standards
3. Analyze strengths/weaknesses
4. Suggest strategic approach

## Common Motion Types

### Motion to Dismiss (12(b)(6))
**Standard**: Accept all factual allegations as true, dismiss only if no legal theory could succeed

**Research Checklist:**
- Elements of each claim
- Plausibility standard (*Twombly*, *Iqbal*)
- Applicable statute of limitations
- Jurisdictional requirements

**Strategy:**
- If plaintiff: Plead facts showing each element
- If defendant: Identify missing elements or legal bars

### Motion for Summary Judgment
**Standard**: No genuine dispute of material fact + entitled to judgment as matter of law

**Research Checklist:**
- Each element of claim/defense
- What facts are disputed vs. undisputed
- What law applies to undisputed facts
- Can reasonable jury find for opponent?

**Strategy:**
- If moving: Identify undisputed facts proving case
- If responding: Identify genuine factual disputes

### Motion to Compel Discovery
**Standard**: Discovery sought is relevant, proportional, not privileged

**Research Checklist:**
- Relevance to claims/defenses
- Proportionality factors
- Privilege assertions
- Prior court orders on similar issues

**Strategy:**
- If moving: Show relevance + opponent's lack of cooperation
- If responding: Demonstrate burden, privilege, or prior production

## Extended Thinking Trigger

**ALWAYS use "ultrathink" mode for:**
- Whether to file motion now vs. later
- Which motion has best chance of success
- How to respond to opponent's motion
- Strategic implications of motion outcome

Example:
```
User: "Should we file summary judgment now?"
[Trigger ultrathink mode]
[Deep reasoning through:]
- Discovery record completeness
- Disputed vs. undisputed facts
- Timing advantages
- Opponent's likely response
- Alternative strategies
```

## Motion Workflow

1. **Research Phase** (use ultrathink)
   - What is the standard?
   - What cases apply it?
   - What are strongest arguments?
   - What are weaknesses to address?

2. **Drafting Phase**
   - State standard clearly
   - Apply law to facts methodically
   - Anticipate counter-arguments
   - Cite to specific record evidence

3. **Review Phase** (MANDATORY)
   - Self-review for legal sufficiency
   - Citation verification
   - Fact verification against evidence
   - Opposing counsel attack simulation

4. **Filing Phase**
   - Check local rules (page limits, formatting)
   - Certificate of service
   - Proposed order (if required)
   - Electronic filing compliance
```

#### Skill: Trial Preparation

**File**: `.claude/skills/trial_preparation/SKILL.md`

```yaml
---
name: Trial Preparation Assistant
description: Use when case_timeline shows trial scheduled, user mentions trial prep, or asks about exhibits/witnesses/jury instructions. Comprehensive trial preparation workflow.
---

# Trial Preparation Workflow

You are preparing for trial.

## Your Role
- Organize trial exhibits
- Prepare witness examinations
- Draft jury instructions
- Create trial brief
- Manage pre-trial deadlines

## Pre-Trial Checklist

### Exhibit Management
- [ ] Number all exhibits
- [ ] Create exhibit list
- [ ] Prepare exhibit notebooks
- [ ] Get stipulations on authenticity
- [ ] Plan exhibit presentation order

### Witness Preparation
- [ ] List all witnesses (fact + expert)
- [ ] Draft direct examination outlines
- [ ] Draft cross-examination outlines
- [ ] Identify impeachment materials
- [ ] Prepare witness for testimony

### Jury Materials
- [ ] Draft proposed jury instructions
- [ ] Draft verdict form
- [ ] Research similar case jury charges
- [ ] Prepare voir dire questions
- [ ] Plan opening statement themes

### Trial Brief
- [ ] Statement of facts
- [ ] Legal issues and standards
- [ ] Argument on key issues
- [ ] Proposed findings of fact
- [ ] Proposed conclusions of law

### Pre-Trial Order Compliance
- [ ] Witness list filed
- [ ] Exhibit list filed
- [ ] Deposition designations filed
- [ ] Motions in limine filed
- [ ] Pre-trial conference attended

## Timeline Management

**Check case_timeline.md for:**
- Pre-trial conference date
- Deadline for exhibit lists
- Deadline for witness lists
- Trial date
- Post-trial briefing schedule

**Alert user if deadline within 14 days**
```

#### Skill: Fact Verification (Enhanced)

**File**: `.claude/skills/fact_verification/SKILL.md`

```yaml
---
name: Evidence Accuracy Checker
description: Use when user asks to fact-check a document, mentions verifying facts, or editing pleadings/motions. Checks every factual assertion against actual evidence files. Critical for Rule 11 compliance.
allowed-tools: [Read, Glob, Grep]
---

# Fact Verification Protocol

You are verifying factual accuracy to prevent Rule 11 sanctions.

## Your Role
- Check EVERY date, amount, quote, and factual claim
- Compare claims against actual evidence in 04_EVIDENCE/
- Flag unsupported assertions
- Prevent Rule 11 violations

## Systematic Verification Process

### 1. Extract All Factual Assertions
Identify:
- Specific dates mentioned
- Dollar amounts and percentages
- Direct quotes from documents
- Events described as occurring
- Claims about defendant's actions/knowledge
- Damage calculations

### 2. Map to Evidence Sources
For each fact, determine which evidence should support it:
- 04_EVIDENCE/01_Documents/ - Contracts, agreements
- 04_EVIDENCE/02_Communications/ - Emails, letters
- 04_EVIDENCE/03_Financial_Records/ - Statements, receipts
- 03_DISCOVERY/ - Discovery responses
- 05_CORRESPONDENCE/ - Correspondence with parties

### 3. Verify Each Assertion
Read the source document and confirm:
- Date is exactly correct (not transposed, wrong year)
- Amount matches precisely (no rounding errors)
- Quote is word-for-word accurate
- Event actually occurred as described
- Claim is supported by evidence

### 4. Categorize Discrepancies

**CRITICAL (Rule 11 Risk):**
- Unsupported factual assertions
- Claims contradicting evidence
- Fabricated or assumed information
- Misrepresented documents

**MAJOR (Credibility Risk):**
- Wrong dates affecting timeline
- Incorrect amounts
- Misquoted documents
- Party misidentification

**MINOR (Low Risk):**
- Typos not affecting meaning
- Formatting inconsistencies
- Rounding differences

### 5. Report Findings
Format:
```
FACT VERIFICATION RESULTS:

Total assertions checked: [X]
Fully verified: [X]
Discrepancies found: [X]

CRITICAL ISSUES (Rule 11 risk):
1. [Description of unsupported fact]
2. [Description of contradictory claim]

MAJOR ISSUES (Fix before filing):
1. [Wrong date/amount/quote]
2. [Another issue]

MINOR ISSUES (Optional fixes):
1. [Typo or formatting]

RECOMMENDATION: [Safe to file / Fix critical issues / Major revision needed]
```

## Auto-Activation Triggers

This skill auto-activates when:
- User edits files in 02_PLEADINGS/
- User mentions "fact-check" or "verify facts"
- User runs /review command
- Files being saved to pleadings folder (via hook)

## Integration with Hooks

When post-edit hook triggers on pleading files:
```bash
if [[ "$FILE" =~ 02_PLEADINGS.*\.md$ ]]; then
  # This skill auto-activates for fact verification
fi
```
```

**Testing Each Skill**:
1. Create test case scenarios for each stage
2. Verify skills auto-activate with relevant prompts
3. Confirm allowed-tools restrictions work
4. Test skill descriptions trigger correct activation

---

### PHASE 3: Hooks (Week 4)
**Effort**: Medium | **Impact**: High | **Code Changes**: Shell scripts

#### Create `.claude/hooks/` Directory

```
.claude/hooks/
├── post-edit.sh       # Runs after every file edit
├── pre-edit.sh        # Runs before file edits
├── user-prompt-submit.sh  # Runs when user submits prompt
└── README.md          # Hook documentation
```

#### Hook: Post-Edit Fact Verification

**File**: `.claude/hooks/post-edit.sh`

```bash
#!/bin/bash
# Post-edit hook: Run checks after file edits

FILE="$1"  # Edited file path
ACTION="$2"  # edit, create, delete

# Auto-fact-verify pleadings after edits
if [[ "$FILE" =~ 02_PLEADINGS.*\.(md|docx)$ ]]; then
    echo "[HOOK] Running fact verification on pleading..."
    python_path=$(cat .wepublic_defender/env_info.json | grep python_exe | cut -d'"' -f4)
    "$python_path" -m wepublic_defender.cli.run_agent \
        --agent fact_verify \
        --file "$FILE" \
        --mode guidance \
        --quiet
    echo "[HOOK] Fact verification complete"
fi

# Check discovery deadlines when editing discovery files
if [[ "$FILE" =~ 03_DISCOVERY.*\.md$ ]]; then
    echo "[HOOK] Checking discovery deadlines..."
    grep -A 5 "DISCOVERY\|Discovery" .wepublic_defender/case_timeline.md | \
        grep -E "deadline|due" || echo "No deadlines found"
fi

# Update session notes after significant edits
if [[ "$ACTION" == "create" ]] || [[ "$FILE" =~ FINAL ]]; then
    echo "[HOOK] Reminder: Update session_notes.md with work completed"
fi
```

#### Hook: Pre-Edit Protection

**File**: `.claude/hooks/pre-edit.sh`

```bash
#!/bin/bash
# Pre-edit hook: Block dangerous edits

FILE="$1"

# Prevent editing filed documents
if [[ "$FILE" =~ .*FILED.*\.(md|docx)$ ]]; then
    echo "[HOOK] ERROR: Cannot edit filed documents!"
    echo "This document has been filed with the court."
    echo "Create a new version or amended filing instead."
    exit 1
fi

# Warn when editing final versions
if [[ "$FILE" =~ .*_FINAL\.(md|docx)$ ]]; then
    echo "[HOOK] WARNING: Editing a FINAL version."
    echo "Consider creating a new version (_v2) instead."
    echo "Press Ctrl+C to cancel or Enter to continue..."
    read -t 5 || true  # 5 second timeout
fi

# Require fact verification before filing
if [[ "$FILE" =~ 02_PLEADINGS.*\.md$ ]] && [[ "$FILE" =~ .*READY.*TO.*FILE.* ]]; then
    if ! grep -q "FACT_VERIFIED" "$FILE"; then
        echo "[HOOK] ERROR: Document marked READY TO FILE but not fact-verified!"
        echo "Run fact_verify agent first: /review --fact-check"
        exit 1
    fi
fi
```

#### Hook: Session Notes Update Reminder

**File**: `.claude/hooks/user-prompt-submit.sh`

```bash
#!/bin/bash
# User prompt submit hook: Run checks when user submits prompts

PROMPT="$1"

# Check if session_notes.md needs updating after major operations
if echo "$PROMPT" | grep -qiE "agent|/review|/draft|/research"; then
    LAST_UPDATE=$(stat -c %Y .wepublic_defender/session_notes.md 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_UPDATE))

    # If session notes not updated in 10+ minutes
    if [ $DIFF -gt 600 ]; then
        echo "[HOOK] Reminder: session_notes.md not updated in 10+ minutes"
        echo "Update 'Currently Working On' section when starting tasks"
    fi
fi
```

#### Hook Documentation

**File**: `.claude/hooks/README.md`

```markdown
# WePublicDefender Hooks

Hooks automatically run at specific lifecycle events to enforce quality gates and workflow rules.

## Available Hooks

### post-edit.sh
Runs after every file edit.

**Triggers:**
- Auto-fact-verification on pleadings
- Discovery deadline checks
- Session notes update reminders

### pre-edit.sh
Runs before file edits to prevent mistakes.

**Blocks:**
- Editing filed documents
- Saving un-verified documents marked "READY TO FILE"

**Warns:**
- Editing FINAL versions (suggests creating new version)

### user-prompt-submit.sh
Runs when user submits prompts.

**Checks:**
- Session notes update reminders
- Cost alerts for expensive operations

## Enabling Hooks

Hooks are automatically enabled when `.claude/hooks/` directory exists with executable scripts.

## Debugging Hooks

Set verbose mode:
```bash
export CLAUDE_HOOKS_VERBOSE=1
```

Disable specific hook:
```bash
export CLAUDE_SKIP_POST_EDIT=1
```

## Hook Best Practices

- Keep hooks fast (< 2 seconds)
- Fail gracefully (don't break workflow)
- Provide clear error messages
- Log to `.wepublic_defender/logs/hooks.log`
```

**Testing Hooks**:
1. Test pre-edit hook blocks filed documents
2. Test post-edit hook runs fact verification
3. Test prompt submit hook shows reminders
4. Verify hooks don't break on errors

---

### PHASE 4: MCP Server (Week 5-7)
**Effort**: High | **Impact**: Medium | **Code Changes**: New Python module

#### Architecture

**MCP Server**: Provides structured access to case data for natural language queries.

**Location**: `wepublic_defender/mcp/evidence_server.py`

#### Implementation

```python
# wepublic_defender/mcp/evidence_server.py
"""
MCP Server for WePublicDefender Case Evidence Access

Provides natural language interface to case files and metadata.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import anthropic

class EvidenceServer:
    """MCP server providing access to case evidence and metadata."""

    def __init__(self, case_path: str):
        self.case_path = Path(case_path)
        self.evidence_path = self.case_path / "04_EVIDENCE"
        self.discovery_path = self.case_path / "03_DISCOVERY"
        self.timeline_path = self.case_path / ".wepublic_defender" / "case_timeline.md"

    def search_evidence(self, query: str) -> List[Dict]:
        """
        Search evidence folder using natural language query.

        Returns list of relevant files with excerpts.
        """
        results = []

        # Search all evidence files
        for evidence_file in self.evidence_path.rglob("*"):
            if evidence_file.is_file():
                try:
                    # For text files, search content
                    if evidence_file.suffix in ['.md', '.txt']:
                        content = evidence_file.read_text()
                        if query.lower() in content.lower():
                            # Extract context around match
                            lines = content.split('\n')
                            matches = [line for line in lines if query.lower() in line.lower()]
                            results.append({
                                "file": str(evidence_file.relative_to(self.case_path)),
                                "type": "text",
                                "matches": matches[:3]  # First 3 matches
                            })
                    # For PDFs/images, return filename if it matches
                    elif query.lower() in evidence_file.name.lower():
                        results.append({
                            "file": str(evidence_file.relative_to(self.case_path)),
                            "type": evidence_file.suffix[1:],
                            "note": "Filename match - manual review needed"
                        })
                except Exception as e:
                    continue

        return results

    def get_timeline_events(self, date_range: Optional[tuple] = None) -> List[Dict]:
        """
        Get events from case timeline, optionally filtered by date range.
        """
        if not self.timeline_path.exists():
            return []

        timeline_content = self.timeline_path.read_text()
        events = []

        # Parse markdown timeline format
        current_event = None
        for line in timeline_content.split('\n'):
            if line.startswith('### '):
                if current_event:
                    events.append(current_event)
                # Parse: ### YYYY-MM-DD HH:MM - TYPE - Description
                parts = line[4:].split(' - ', 2)
                if len(parts) >= 3:
                    current_event = {
                        "date": parts[0].strip(),
                        "type": parts[1].strip(),
                        "description": parts[2].strip(),
                        "details": []
                    }
            elif current_event and line.startswith('**'):
                # Parse detail lines
                if ':' in line:
                    key, value = line[2:].split(':', 1)
                    key = key.strip('*: ')
                    value = value.strip()
                    current_event[key.lower().replace(' ', '_')] = value

        if current_event:
            events.append(current_event)

        # Filter by date range if provided
        if date_range:
            start_date, end_date = date_range
            events = [e for e in events
                     if start_date <= e['date'] <= end_date]

        return events

    def check_deadline(self, deadline_type: Optional[str] = None) -> List[Dict]:
        """
        Check upcoming deadlines, optionally filtered by type.
        """
        events = self.get_timeline_events()
        today = datetime.now().strftime("%Y-%m-%d")

        # Filter for future events
        upcoming = [e for e in events if e['date'] >= today]

        # Filter by deadline type if specified
        if deadline_type:
            upcoming = [e for e in upcoming
                       if deadline_type.lower() in e.get('description', '').lower()
                       or deadline_type.lower() in e.get('type', '').lower()]

        # Sort by date
        upcoming.sort(key=lambda x: x['date'])

        # Add days until deadline
        for event in upcoming:
            event_date = datetime.strptime(event['date'][:10], "%Y-%m-%d")
            days_until = (event_date - datetime.now()).days
            event['days_until'] = days_until

        return upcoming

    def get_discovery_status(self) -> Dict:
        """
        Get status of all discovery items (requests sent, responses due, etc.)
        """
        status = {
            "requests_sent": [],
            "responses_due": [],
            "received_from_opponent": [],
            "pending_responses": []
        }

        if not self.discovery_path.exists():
            return status

        # Scan discovery folder structure
        for disc_file in self.discovery_path.rglob("*.md"):
            file_name = disc_file.name.lower()

            if "interrogator" in file_name or "document_request" in file_name:
                # Determine if sent or received
                if "to_opponent" in str(disc_file.parent):
                    status["requests_sent"].append(str(disc_file.relative_to(self.case_path)))
                elif "from_opponent" in str(disc_file.parent):
                    status["responses_due"].append(str(disc_file.relative_to(self.case_path)))

        # Check for deadlines in timeline
        deadlines = self.check_deadline("discovery")
        status["upcoming_deadlines"] = deadlines

        return status

    def verify_fact(self, claim: str) -> Dict:
        """
        Search for evidence supporting a specific factual claim.
        Returns evidence found and confidence level.
        """
        evidence_results = self.search_evidence(claim)

        return {
            "claim": claim,
            "evidence_found": len(evidence_results) > 0,
            "supporting_documents": [r['file'] for r in evidence_results],
            "confidence": "high" if len(evidence_results) >= 2 else "medium" if len(evidence_results) == 1 else "low",
            "details": evidence_results
        }


# MCP Server Configuration
def setup_mcp_server():
    """
    Setup MCP server configuration.

    Add to claude_desktop_config.json:
    {
      "mcpServers": {
        "wepublic_defender": {
          "command": "python",
          "args": ["-m", "wepublic_defender.mcp.evidence_server"],
          "env": {
            "CASE_PATH": "/path/to/case"
          }
        }
      }
    }
    """
    pass
```

#### MCP Tool Definitions

```python
# Tool definitions for MCP
TOOLS = [
    {
        "name": "search_evidence",
        "description": "Search case evidence folder for files matching query",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (keywords, dates, amounts, etc.)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_timeline_events",
        "description": "Get events from case timeline, optionally filtered by date range",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"}
            }
        }
    },
    {
        "name": "check_deadline",
        "description": "Check upcoming deadlines, optionally filtered by type (discovery, motion, trial, etc.)",
        "input_schema": {
            "type": "object",
            "properties": {
                "deadline_type": {"type": "string"}
            }
        }
    },
    {
        "name": "get_discovery_status",
        "description": "Get status of all discovery items (requests, responses, deadlines)",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "verify_fact",
        "description": "Search for evidence supporting a specific factual claim",
        "input_schema": {
            "type": "object",
            "properties": {
                "claim": {
                    "type": "string",
                    "description": "Factual claim to verify (date, amount, event, etc.)"
                }
            },
            "required": ["claim"]
        }
    }
]
```

#### Usage Examples

```python
# In Claude Code conversation:

User: "Do we have evidence of the January 2023 payment?"
Claude: [Calls MCP: search_evidence("January 2023 payment")]
MCP Returns: {
    "file": "04_EVIDENCE/03_Financial_Records/Statement_012023_9862.pdf",
    "type": "pdf",
    "note": "Filename match - manual review needed"
}
Claude: "Yes, we have Statement_012023_9862.pdf in financial records. Let me read it to find the payment details."

---

User: "What are our upcoming deadlines?"
Claude: [Calls MCP: check_deadline()]
MCP Returns: [
    {"date": "2025-10-25", "type": "DISCOVERY", "description": "Response to Interrogatories due", "days_until": 5},
    {"date": "2025-11-05", "type": "COURT_EVENT", "description": "Motion to Dismiss hearing", "days_until": 16}
]
Claude: "You have 2 upcoming deadlines:
1. [5 days] Oct 25: Response to Interrogatories due
2. [16 days] Nov 5: Motion to Dismiss hearing"

---

User: "Did defendant admit receiving the notice?"
Claude: [Calls MCP: search_evidence("admit receiving notice") + get_discovery_status()]
Claude: "Let me search discovery responses for admissions about notice..."
```

**Testing MCP Server**:
1. Set up test case with evidence files
2. Test each MCP tool function
3. Verify results are accurate
4. Test integration with Claude Code

---

### PHASE 5: Extended Thinking Integration (Week 8)
**Effort**: Low | **Impact**: Medium | **Code Changes**: Config updates

#### Strategy: Use Extended Thinking Selectively

Extended thinking is **expensive** (more tokens = more cost). Use strategically for complex decisions.

#### Implementation

**Update agent configurations to trigger extended thinking:**

**File**: `wepublic_defender/config/legal_review_settings.json`

```json
{
  "reviewAgentConfig": {
    "strategy_agent": {
      "models": ["gpt-5", "grok-4"],
      "effort": "high",
      "web_search": true,
      "extended_thinking": true,
      "thinking_budget": 10000
    },
    "opposing_counsel_agent": {
      "models": ["grok-4", "gpt-5"],
      "effort": "high",
      "web_search": true,
      "extended_thinking": true,
      "thinking_budget": 8000
    }
  }
}
```

#### Auto-Trigger Extended Thinking

**Update prompts to include "ultrathink" keyword when complexity detected:**

```python
# In wepublic_defender/core.py

def _build_prompt_with_thinking(self, agent_type: str, complexity_indicators: Dict) -> str:
    """Add extended thinking trigger for complex tasks."""

    # Complexity indicators that trigger extended thinking
    should_ultrathink = (
        agent_type in ["strategy", "opposing_counsel"] or
        complexity_indicators.get("multiple_claims") or
        complexity_indicators.get("novel_legal_issue") or
        complexity_indicators.get("high_stakes") or
        complexity_indicators.get("conflicting_authorities")
    )

    if should_ultrathink:
        return "ultrathink: " + base_prompt
    return base_prompt
```

#### Extended Thinking Use Cases

**ALWAYS use extended thinking for:**
1. **Case viability analysis** (file or not?)
2. **Motion strategy decisions** (file summary judgment now or wait?)
3. **Settlement evaluation** (accept offer or proceed to trial?)
4. **Opposing counsel attack simulation** (find all weaknesses)
5. **Complex legal standard application** (novel issue requiring deep reasoning)

**NEVER use extended thinking for:**
1. **Routine fact-checking** (date verification)
2. **Citation formatting** (shepardizing cases)
3. **Document organization** (file management)
4. **Procedural compliance** (checking page limits)

**Testing**:
1. Verify "ultrathink" keyword triggers extended thinking
2. Monitor token usage (should see "thinking tokens" in usage)
3. Compare output quality with/without extended thinking
4. Validate cost increase is justified by quality improvement

---

## Implementation Checklist

### Phase 1: Multiple Choice Questions
- [ ] Update session_start_checklist.md with stage detection
- [ ] Add pre-filing stage questions
- [ ] Add discovery stage questions
- [ ] Add motion practice stage questions
- [ ] Add trial prep stage questions
- [ ] Test with various case states

### Phase 2: Skills
- [ ] Create `.claude/skills/` directory
- [ ] Implement pre_filing_investigation skill
- [ ] Implement discovery_management skill
- [ ] Implement motion_practice skill
- [ ] Implement trial_preparation skill
- [ ] Implement fact_verification skill
- [ ] Test skill auto-activation
- [ ] Test allowed-tools restrictions

### Phase 3: Hooks
- [ ] Create `.claude/hooks/` directory
- [ ] Implement post-edit.sh hook
- [ ] Implement pre-edit.sh hook
- [ ] Implement user-prompt-submit.sh hook
- [ ] Write hooks README.md
- [ ] Test fact verification auto-trigger
- [ ] Test filed document protection
- [ ] Test session notes reminders

### Phase 4: MCP Server
- [ ] Create wepublic_defender/mcp/ directory
- [ ] Implement evidence_server.py
- [ ] Implement search_evidence function
- [ ] Implement get_timeline_events function
- [ ] Implement check_deadline function
- [ ] Implement get_discovery_status function
- [ ] Implement verify_fact function
- [ ] Write MCP tool definitions
- [ ] Test MCP server locally
- [ ] Create MCP configuration docs

### Phase 5: Extended Thinking
- [ ] Update settings.json with thinking configs
- [ ] Add ultrathink triggers to prompts
- [ ] Test extended thinking for strategy
- [ ] Test extended thinking for opposing counsel
- [ ] Monitor cost impact
- [ ] Document when to use vs. not use

---

## Success Metrics

### User Experience Improvements
- **Onboarding time**: Reduced from "confused about commands" to "guided through workflow"
- **Error prevention**: Auto-fact-checking catches Rule 11 issues before filing
- **Workflow efficiency**: Stage-appropriate options eliminate decision paralysis
- **Quality gates**: Hooks prevent common mistakes (editing filed docs, missing fact-checks)

### Technical Metrics
- **Skill activation accuracy**: >90% of skills activate in correct context
- **Hook reliability**: 100% of dangerous edits blocked
- **MCP query success**: >95% of evidence queries return relevant results
- **Extended thinking cost**: <20% increase in token usage for <10% of operations

### Business Value
- **Reduced sanctions risk**: Fact verification catches unsupported claims
- **Faster case resolution**: Proper stage workflows accelerate progress
- **Better legal outcomes**: Strategic analysis improves decision quality
- **Lower training cost**: New users productive faster with guided workflows

---

## User Experience: Before vs. After

### BEFORE (Current State)

```
User: [Opens Claude Code in case folder]

User: "I need help with my case"

Claude: "What would you like to do?"

User: "I don't know, what can you help with?"

Claude: "I can help with research, drafting, reviewing documents, organizing files..."

User: [Overwhelmed, doesn't know where to start]

User: "Can you just look at my case and tell me what needs to be done?"

Claude: "Let me check your files..."
[Reads several files manually]
"It looks like you're in discovery. You could respond to discovery requests, or..."

User: [Has to manually direct every step]
```

### AFTER (With New Features)

```
User: [Opens Claude Code in case folder]

Claude: [Auto-detects discovery phase via timeline + folder structure]
       [Discovery Management Skill auto-activates]
       [Checks upcoming deadlines via MCP]

"You're in active discovery with 2 pending responses due Oct 25 (in 5 days).

What's your priority?

1. Respond to Interrogatories Set 1 (due in 5 days)
2. Respond to Document Request 1 (due in 5 days)
3. Draft your own discovery requests
4. Organize opponent's document production
5. Check discovery deadline calendar
6. Something else (tell me what)

Choose 1-6:"

User: "1"

Claude: [Discovery Skill guides workflow]
       [MCP searches evidence for answers]

"Loading Interrogatories Set 1... I found 15 questions.

Searching evidence files for answers...
[MCP: search_evidence for each question]

Found evidence for:
- Questions 1-8: Bank statements in 04_EVIDENCE/03_Financial_Records
- Questions 9-12: Email correspondence in 04_EVIDENCE/02_Communications
- Questions 13-15: Need client input (no documentary evidence)

Should I draft responses for questions 1-12?"

User: "yes"

Claude: [Drafts responses with specific evidence citations]
       [Saves to 03_DISCOVERY/Responses/]
       [Post-edit hook auto-triggers fact verification]

"Draft complete. Auto-verified facts against evidence:
- All 12 responses supported by evidence
- All amounts match financial records exactly
- All dates verified against source documents

[OK] Ready to review before filing.

Would you like me to check for strategic objections?"
```

**Result**: User went from "I don't know what to do" to "responses drafted and fact-checked" with minimal decisions required.

---

## Integration Points

### With Existing Workflows

**session_start_checklist.md**:
- Add stage detection + multiple choice questions
- Integrate with Skills that auto-activate

**legal_document_workflow.md**:
- Hooks auto-trigger fact verification in review phase
- Skills provide stage-specific guidance
- MCP enables evidence queries during drafting

**CLAUDE.md orchestrator**:
- Update to mention Skills activation
- Document hook behavior
- Explain MCP data access

### With External Tools

**Claude.ai Deep Research**:
- Multiple choice questions offer "deep research" option for pre-filing
- Skills guide users to use deep research at appropriate stages

**External LLMs** (GPT-5, Grok-4):
- Extended thinking enhances strategy and opposing counsel agents
- MCP provides evidence context for more accurate analysis

---

## Cost Analysis

### Development Costs
- **Phase 1**: 2 hours (update docs only)
- **Phase 2**: 16 hours (create 5 skills)
- **Phase 3**: 12 hours (implement 3 hooks + testing)
- **Phase 4**: 40 hours (MCP server development + testing)
- **Phase 5**: 4 hours (config updates)
- **Total**: ~74 hours (~2 weeks of development)

### Operational Costs
- **Multiple choice questions**: $0 (no API calls)
- **Skills**: $0 (guidance mode, no API calls)
- **Hooks**: $0 (local execution only)
- **MCP queries**: $0 (local server, no API calls)
- **Extended thinking**: +10-20% token costs for 5-10% of operations
- **Net cost increase**: <2% average (extended thinking is selective)

### Value Delivered
- **Time savings**: 30-50% faster case workflow (guided vs. manual)
- **Error prevention**: Eliminate Rule 11 sanctions ($5K-50K+ saved per case)
- **Quality improvement**: Better legal analysis with extended thinking
- **Training reduction**: New users productive in days vs. weeks

**ROI**: High - Minimal cost increase for significant value delivery

---

## Risks and Mitigations

### Risk 1: Skills Don't Auto-Activate
**Mitigation**: Detailed descriptions + thorough testing of activation triggers

### Risk 2: Hooks Break Workflow
**Mitigation**: Fail gracefully, clear error messages, easy to disable

### Risk 3: MCP Server Failures
**Mitigation**: Fallback to manual file reading if MCP unavailable

### Risk 4: Extended Thinking Too Expensive
**Mitigation**: Selective use, monitor costs, make configurable

### Risk 5: Multiple Choice Questions Too Rigid
**Mitigation**: Always include "Something else (tell me what)" option

---

## Testing Strategy

### Unit Tests
- MCP server functions (search, timeline, deadlines)
- Hook script execution
- Stage detection logic

### Integration Tests
- Skills activation in various contexts
- Hooks triggering at correct events
- MCP queries during conversations
- Extended thinking cost monitoring

### User Acceptance Tests
- New user completes full case workflow
- Experienced user validates stage appropriateness
- Error scenarios handled gracefully

### Performance Tests
- MCP query response times (<1 second)
- Hook execution times (<2 seconds)
- Extended thinking not blocking workflow

---

## Documentation Updates Needed

### User-Facing Docs
- Add "How Skills Work" section to CLAUDE.md
- Document multiple choice question patterns
- Explain hook behavior (when they trigger, what they do)
- MCP server setup guide
- Extended thinking cost explanation

### Developer Docs
- Skills authoring guide
- Hook development guide
- MCP server API documentation
- Extended thinking configuration reference

---

## Future Enhancements (Post-MVP)

### Phase 6: AI-Powered Stage Detection
Use LLM to analyze case state and predict next best action

### Phase 7: Custom Skill Marketplace
Allow users to share/install community-created skills

### Phase 8: Advanced MCP Integrations
Connect to external legal databases (Westlaw, LexisNexis)

### Phase 9: Predictive Deadlines
Auto-calculate and track procedural deadlines

### Phase 10: Multi-Case Management
Skills and MCP work across multiple cases simultaneously

---

## Approval and Next Steps

**Proposed Timeline**:
- Week 1: Phase 1 (Multiple Choice Questions)
- Week 2-3: Phase 2 (Skills)
- Week 4: Phase 3 (Hooks)
- Week 5-7: Phase 4 (MCP Server)
- Week 8: Phase 5 (Extended Thinking)

**Resource Requirements**:
- 1 developer for 8 weeks
- Access to test cases for each stage
- Claude Code Pro/Team subscription for testing

**Success Criteria**:
- All 5 phases implemented and tested
- User can complete full case workflow guided by system
- No increase in error rates
- Positive user feedback on experience

**Approval Required From**:
- Technical lead (architecture review)
- Legal expert (workflow validation)
- Product owner (priority/timeline)

---

## References

- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Claude Code Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks-guide)
- [Model Context Protocol (MCP) Specification](https://docs.claude.com/en/docs/mcp)
- [Extended Thinking Documentation](https://docs.claude.com/en/docs/build-with-claude/extended-thinking)
- [WePublicDefender Legal Workflows](../.claude/workflows/legal_document_workflow.md)

---

**Document Status**: Draft for Review
**Last Updated**: 2025-10-20
**Next Review Date**: After PR merge

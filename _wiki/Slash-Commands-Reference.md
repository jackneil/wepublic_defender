# Slash Commands Reference

Slash commands are shortcuts that trigger specific WePublicDefender functions. Type these commands in Claude Code to execute them.

## Core Commands

### /check-env

**Purpose**: Verify your environment setup

**Usage**:
```
/check-env
```

**What it does**:
- Checks Python installation
- Verifies API keys are configured
- Tests WePublicDefender installation
- Reports any issues

**Output example**:
```
Environment Check:
✓ Python 3.11.5 found
✓ WePublicDefender installed
✓ OpenAI API key configured
✓ xAI API key configured
⚠ CourtListener token missing (optional)
✓ Case initialized

Status: Ready to use!
```

**When to use**:
- First time setup
- After installation
- When getting errors
- To verify API keys work

### /organize

**Purpose**: Organize documents from inbox into proper folders

**Usage**:
```
/organize
```

**What it does**:
- Reads all files in `00_NEW_DOCUMENTS_INBOX/`
- Identifies document types
- Moves to appropriate folders
- Logs all movements

**Output example**:
```
Organizing 8 documents from inbox...

✓ complaint.pdf → 02_PLEADINGS/01_Complaint/
✓ answer.pdf → 02_PLEADINGS/02_Answers/
✓ contract_2023.pdf → 04_EVIDENCE/contracts/
✓ email_thread.pdf → 05_CORRESPONDENCE/
✓ research_memo.docx → 06_RESEARCH/
✓ motion_draft.md → 07_DRAFTS_AND_WORK_PRODUCT/

Organization complete! 8 files organized.
Check .database/file_management_log.md for details.
```

**Options**:
- Always runs in guidance mode (free)
- No external API calls
- Safe to run multiple times

### /timeline

**Purpose**: View or update case timeline

**Usage**:
```
/timeline              # View timeline
/timeline add          # Add entry
/timeline update       # Update entry
```

**What it does**:
- Shows chronological case events
- Tracks filings and deadlines
- Maintains case history

**Output example**:
```
CASE TIMELINE (Last 5 entries)

2025-10-15 - Motion to Dismiss filed by defendant
2025-10-10 - Answer filed
2025-09-28 - Defendant served
2025-09-20 - Complaint filed
2025-09-15 - Demand letter sent

Full timeline in: .wepublic_defender/case_timeline.md
```

### /deep-research-prep

**Purpose**: Generate comprehensive research prompt for Claude.ai

**Usage**:
```
/deep-research-prep
```

**What it does**:
- Asks for case details
- Generates 20+ section research prompt
- Prepares for Claude.ai Deep Research
- Guides you through the process

**Output example**:
```
I'll generate a deep research prompt for Claude.ai

First, tell me about your case:
1. Type of case?
2. Main parties?
3. Key issues?
4. Jurisdiction?

[After you provide details]

Generated comprehensive research prompt!

Instructions:
1. Copy this entire prompt
2. Go to https://claude.ai
3. Enable Research mode (blue button)
4. Paste and send
5. Wait 5-10 minutes
6. Download results to inbox
7. Tell me when done
```

### /research

**Purpose**: Quick legal research on specific topics

**Usage**:
```
/research [topic]
```

**Examples**:
```
/research qualified immunity fourth circuit
/research statute of limitations breach contract SC
/research summary judgment standard
```

**What it does**:
- Researches specific legal question
- Provides relevant cases and statutes
- Focuses on your jurisdiction
- Quicker than deep research

**Output example**:
```
RESEARCH: Qualified Immunity - Fourth Circuit

Standard: Two-part test
1. Constitutional violation occurred
2. Right was clearly established

Key Cases:
• Pearson v. Callahan (2009) - order of analysis
• Smith v. Ray (4th Cir. 2021) - recent application
• Johnson v. Barnes (4th Cir. 2020) - clearly established

Recent Trend: Fourth Circuit applying more strictly

[Full analysis continues...]
```

### /strategy

**Purpose**: Get strategic recommendations

**Usage**:
```
/strategy
```

**What it does**:
- Analyzes current case status
- Identifies strengths/weaknesses
- Recommends next steps
- Suggests tactical decisions

**Output example**:
```
STRATEGIC ASSESSMENT

Case Strength: Moderate to Strong

Strengths:
• Strong documentary evidence
• Favorable jurisdiction (4th Cir.)
• Clear damages

Weaknesses:
• Statute of limitations issue
• Missing witness testimony

Immediate Recommendations:
1. File motion for summary judgment on liability
2. Depose key witness before deadline
3. Consider settlement discussions

Long-term Strategy:
• Focus on documentary evidence
• Prepare for possibility of partial summary judgment
• Keep settlement option open
```

### /draft

**Purpose**: Draft legal documents

**Usage**:
```
/draft [document type]
```

**Examples**:
```
/draft motion to dismiss
/draft interrogatories
/draft complaint
/draft response to motion for summary judgment
```

**What it does**:
- Asks for relevant details
- Drafts document with proper formatting
- Includes applicable law
- Suggests filing procedures

**Interactive process**:
```
You: /draft motion for extension

Claude: I'll draft that motion. Please provide:
1. How much additional time needed?
2. Reason for extension?
3. First request?
4. Opposing counsel's position?

You: 30 days, need time for discovery, yes first, haven't asked

Claude: Drafting motion for 30-day extension...
[Produces complete motion]
```

### /review

**Purpose**: Run adversarial review pipeline

**Usage**:
```
/review [filename]
/review [filename] --mode [guidance|external-llm]
/review [filename] --model [model-name]
```

**Examples**:
```
/review motion_to_dismiss.md
/review draft.md --mode external-llm
/review response.md --model gpt-5
```

**What it does**:
- Runs multi-phase review
- Checks citations
- Simulates opposing counsel
- Identifies issues to fix

**Modes**:
- `guidance` (default) - Free, provides checklist
- `external-llm` - Costs money, runs actual AI review

### /start

**Purpose**: Refresh Claude's understanding of your case

**Usage**:
```
/start
```

**What it does**:
- Reloads case context
- Checks for new files
- Updates understanding
- Offers relevant options

**When to use**:
- Beginning of session (automatic)
- After long break
- When Claude seems confused
- To see current options

## Utility Commands

### /pr

**Purpose**: Check PR status and manage pull requests

**Usage**:
```
/pr
```

**Note**: This is for developers contributing to WePublicDefender, not for legal case work.

## Command Options and Flags

### Common Flags

#### --mode

Controls execution mode:
```
--mode guidance      # Free, gives instructions
--mode external-llm  # Costs money, runs AI
```

#### --model

Specifies which AI model:
```
--model gpt-5        # Use only GPT-5
--model grok-4       # Use only Grok-4
--run-both          # Use all configured models
```

#### --verbose

Shows detailed output:
```
/review draft.md --verbose
```

#### --web-search

Enables web search (citations):
```
/review motion.md --web-search
```

## Plain English Alternatives

You don't need slash commands. These work too:

### Instead of /organize:
```
"Please organize my inbox"
"Sort the documents I just added"
"File these documents properly"
```

### Instead of /research:
```
"Research qualified immunity"
"Find cases about employment discrimination"
"What's the statute of limitations for breach of contract?"
```

### Instead of /draft:
```
"Draft a motion to dismiss"
"Write a letter to opposing counsel"
"Create interrogatories"
```

### Instead of /review:
```
"Review my motion for issues"
"Check if my citations are good"
"Attack this like opposing counsel would"
```

## Command Combinations

### Workflow Examples

#### New Documents Workflow
```
/organize                    # Sort new documents
/timeline add               # Update timeline
/strategy                   # Reassess strategy
```

#### Drafting Workflow
```
/research summary judgment   # Research law
/draft motion for summary judgment  # Draft
/review motion_sj.md --mode external-llm  # Review
```

#### Daily Check-in
```
/start                      # Refresh context
/organize                   # Handle new files
/timeline                   # Check deadlines
```

## Advanced Usage

### Chaining Commands

You can run multiple commands:
```
Please organize my files, then show me the timeline, then give me strategic recommendations
```

### Conditional Commands

```
If there are files in the inbox, organize them. Otherwise, show me what drafts need review.
```

### Scheduled Commands

```
Every time I start a session, check for deadlines within 7 days
```

## Troubleshooting Commands

### Command Not Found

**Issue**: `/command` not recognized

**Solutions**:
1. Restart Claude Code (commands load at startup)
2. Check case is initialized: `/check-env`
3. Run `wpd-init-case` if needed

### Command Fails

**Issue**: Command starts but errors

**Solutions**:
1. Check error message
2. Run `/check-env` to verify setup
3. Try with `--verbose` flag for details

### Wrong Output

**Issue**: Command works but output wrong

**Solutions**:
1. Check you're in right folder
2. Verify files are where expected
3. Restart Claude Code to refresh

## Creating Custom Workflows

You can combine commands into workflows:

### Morning Routine
```
"Run my morning routine: check for new files, organize them, show timeline, and give me today's priorities"
```

### Pre-Filing Check
```
"Prepare for filing: review the motion, verify citations, check deadlines, and create filing documents"
```

### Discovery Management
```
"Process discovery: organize new productions, update index, draft privilege log"
```

## Command History

Claude remembers what commands you've run:

```
What commands have I run today?
```

Response:
```
Session commands:
1. /check-env (9:15 AM)
2. /organize (9:20 AM)
3. /review motion.md (9:45 AM)
4. /strategy (10:30 AM)
```

## Best Practices

### Use Commands for Repetitive Tasks

Instead of explaining each time, use:
```
/organize
```

### Combine with Natural Language

```
/organize and then tell me what looks important
```

### Use Modes Appropriately

- Start with `guidance` mode (free)
- Use `external-llm` for final review
- Single model for quick checks
- Multiple models for critical filings

### Learn Your Favorites

Most used commands:
1. `/organize` - Daily filing
2. `/review` - Document review
3. `/strategy` - Decision making
4. `/research` - Quick lookups

## Summary

Slash commands are shortcuts, but you can always use plain English. They're designed to make common tasks faster, not to replace natural conversation with Claude.

The most important commands:
- `/check-env` - Verify setup
- `/organize` - File management
- `/review` - Document review
- `/research` - Legal research
- `/strategy` - Case planning

## Next Steps

- Try basic commands with [Getting Started](Getting-Started)
- Learn the [Review Pipeline](Review-Pipeline)
- Understand [Deep Research](Deep-Research-Workflow)
- Explore [File Organization](File-Organization)
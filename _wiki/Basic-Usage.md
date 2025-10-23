# Basic Usage Guide

This guide covers the most common tasks you'll do with WePublicDefender. Each section includes what to type and what to expect.

## Starting a Session

### Open Claude Code in Your Case Folder

1. Open terminal in your case folder
2. Type `claude` and press Enter
3. Claude automatically loads your case context

What you'll see:
```
Loading case context...
You have 2 documents in inbox.
Discovery response deadline in 5 days.

What would you like to work on?
[ ] Organize documents from inbox
[ ] Draft discovery response
[ ] Review existing drafts
[ ] Other
```

## Organizing Documents

### First Time Organization

When starting a new case with messy documents:

```
/organize
```

Claude will:
1. Read each document
2. Identify document type
3. Move to appropriate folder
4. Log what went where

Example output:
```
Organizing 15 documents from inbox...

✓ Moved complaint.pdf → 02_PLEADINGS/01_Complaint/
✓ Moved contract_2023.pdf → 04_EVIDENCE/contracts/
✓ Moved email_thread.pdf → 04_EVIDENCE/communications/
✓ Moved motion_to_dismiss.pdf → 02_PLEADINGS/03_Motions/
...

Organization complete! 15 files organized.
```

### Adding New Documents

Got new documents? Drop them in inbox and:

```
I received new documents from opposing counsel. Please organize them.
```

## Reviewing Documents

### Basic Review

Review a draft before filing:

```
/review my_motion.md
```

Or in plain English:

```
Review my motion to dismiss for legal issues
```

### Specifying Review Type

Just want citations checked:

```
Check citations in my response brief
```

Just want opposing counsel perspective:

```
Attack my motion like opposing counsel would
```

### Review Results

You'll see:
```
Running review pipeline...

CRITICAL ISSUES (Must Fix):
• Missing jurisdiction statement (¶1)
• Incorrect statute citation (¶5)

MAJOR ISSUES (Should Fix):
• Weak causation argument (¶8-10)
• Missing case law support (¶12)

MINOR ISSUES (Consider):
• Passive voice weakens argument (¶3)
• Formatting inconsistency (¶15)

Recommendations:
1. Add jurisdiction statement immediately after caption
2. Correct statute citation to 42 U.S.C. § 1983
3. Strengthen causation with additional facts
```

## Drafting Documents

### Simple Draft Request

```
/draft motion for extension of time
```

Claude will:
1. Ask for details (how long, why, etc.)
2. Draft the motion
3. Include proper formatting
4. Suggest filing procedures

### Drafting with Context

```
Draft a response to defendant's motion to dismiss. Focus on the jurisdiction issues they raised.
```

### Interactive Drafting

Claude asks questions:
```
Claude: I'll draft that motion. First, some questions:
1. How much additional time do you need?
2. What's the reason for the extension?
3. Is this your first extension request?
4. Has opposing counsel agreed?

You: 30 days, need more time for discovery, yes first request, haven't asked them yet
```

## Legal Research

### Quick Research

```
/research statute of limitations for breach of contract in South Carolina
```

Result:
```
RESEARCH SUMMARY: Breach of Contract - Statute of Limitations (SC)

Time Limit: 3 years from breach
Statute: S.C. Code § 15-3-530
Key Points:
• Runs from date of breach, not discovery
• Can be tolled by partial payment
• Written contracts only - different for oral

Relevant Cases:
• Johnson v. Smith - defining breach date
• Acme v. Jones - tolling provisions
```

### Deep Research

For comprehensive research:

```
/deep-research-prep
```

This creates a research prompt for Claude.ai's Deep Research feature.

## Checking Case Status

### View Timeline

```
/timeline
```

Shows:
```
CASE TIMELINE

Oct 15, 2025 - Complaint filed
Oct 20, 2025 - Defendant served
Nov 1, 2025 - Motion to dismiss filed
Nov 15, 2025 - Response due (IN 3 DAYS)
```

### Check Strategy

```
/strategy
```

Returns:
```
CURRENT STRATEGY ASSESSMENT

Case Strength: Moderate
Stage: Motion Practice

Immediate Priorities:
1. File response to motion to dismiss (due in 3 days)
2. Prepare discovery requests
3. Research additional claims

Recommendations:
• Focus on jurisdiction arguments in response
• Consider amending complaint if motion granted
• Start preparing interrogatories now
```

## Managing Costs

### Check Usage

```
Show me what I've spent today
```

Output:
```
TODAY'S API USAGE

Reviews: $3.42
- Motion review: $2.10
- Citation check: $1.32

Research: $0.85
- Statute research: $0.85

Total Today: $4.27
Month-to-date: $28.53
```

### Use Free Mode

```
Run review in guidance mode (free)
```

This gives you a checklist instead of running AI:
```
REVIEW CHECKLIST (Guidance Mode)

Check these yourself:
□ Jurisdiction stated in first paragraph
□ All parties properly named
□ Legal standard cited with cases
□ Each element addressed
□ Citations in proper format
□ No typos or grammar errors
```

## Common Workflows

### Workflow 1: New Document from Opposing Counsel

```
You: I just received a motion for summary judgment

Claude: I'll help you handle this. Let me:
1. Read and analyze the motion
2. Identify their key arguments
3. Check deadline for response
4. Suggest response strategy

You: Yes, do that

Claude: [Analyzes motion]

Key Arguments They're Making:
1. No genuine issue of material fact
2. Statute of limitations has run
3. Failure to state a claim

Response Deadline: November 30 (21 days)

Recommended Response Strategy:
1. File opposition focusing on fact disputes
2. Include declaration with evidence
3. Request oral argument
```

### Workflow 2: Preparing for Filing

```
You: I'm ready to file my motion. What do I need?

Claude: Pre-filing checklist:
1. Run full review pipeline
2. Verify all citations
3. Check local rules compliance
4. Prepare proposed order
5. Draft notice of motion
6. Check service requirements

Shall I run the review pipeline first?

You: Yes

Claude: [Runs review, fixes issues]

Review complete. Motion is ready. Now preparing:
- Notice of Motion
- Proposed Order
- Certificate of Service
```

### Workflow 3: Discovery Response

```
You: Help me respond to interrogatories

Claude: I'll help with discovery responses. First:
1. How many interrogatories?
2. What's the deadline?
3. Any you plan to object to?

You: 25 interrogatories, due in 10 days, several are too broad

Claude: I'll draft responses with appropriate objections.
For overbroad interrogatories, I'll:
- Object to scope
- Respond subject to objections
- Provide limited information

Starting with Interrogatory 1...
```

## Plain English Commands

You don't need special commands. Just say what you need:

### Examples That Work

```
"Help me understand this contract"
"What does this court order mean?"
"Is my motion strong enough?"
"Find cases about employment discrimination"
"Check if these citations are still good law"
"Organize my evidence folder"
"What should I do next?"
"Help me prepare for the hearing tomorrow"
```

### Claude Figures It Out

```
You: This judge keeps denying everything. What's going on?

Claude: Let me analyze the pattern of rulings.
[Reviews previous orders]

Pattern detected: This judge strictly enforces local rules.
Your motions may be missing:
- Local rule compliance statement
- Proposed orders
- Meet-and-confer certification

Recommendation: Review Local Rules 7.1-7.5 and ensure complete compliance.
```

## Getting Help

### When Confused

```
I don't understand what to do next
```

Claude will:
- Assess your case status
- Explain your options
- Recommend next steps

### When Something Breaks

```
I'm getting an error when I try to review
```

Claude will:
- Check your environment
- Diagnose the issue
- Fix it or explain how to fix it

### When You Need Examples

```
Show me an example of a motion for extension
```

Claude provides templates and examples.

## Tips for Success

### Be Specific

Instead of: "Review this"
Try: "Review my motion for procedural issues and missing arguments"

### Provide Context

Instead of: "Draft a letter"
Try: "Draft a letter to opposing counsel requesting 30-day extension for discovery"

### Ask for Explanations

```
Why does the review keep finding jurisdiction issues?
```

Claude explains legal concepts in plain English.

### Save Your Work

```
Save this as version 2 before making changes
```

### Track Progress

```
Update timeline: Filed motion for summary judgment today
```

## Next Steps

Now that you know basic usage:
- Learn about the [Review Pipeline](Review-Pipeline) in detail
- Explore [Slash Commands](Slash-Commands-Reference)
- Understand [Deep Research](Deep-Research-Workflow)
- Check [Cost Guide](Cost-Guide) to manage expenses
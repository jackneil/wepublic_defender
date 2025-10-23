# Session Start Automation

One of the most powerful features of WePublicDefender is that Claude automatically remembers your case when you start a new session. No more explaining everything from scratch every time!

## How It Works

When you open Claude Code in your case folder, Claude automatically:

1. **Reads your case history** - What you worked on before
2. **Checks for deadlines** - What's due soon
3. **Looks for new files** - Documents in your inbox
4. **Determines case stage** - Pre-filing, discovery, trial prep, etc.
5. **Offers relevant options** - Clickable choices based on your situation

## What You'll See

Instead of a blank terminal, Claude greets you with something like:

```
I see you're in active discovery. What's your priority?

[ ] Respond to pending discovery requests (deadline: Oct 25 - in 5 days!)
[ ] Draft new interrogatories/document requests
[ ] Organize opponent's document production
[ ] Prepare for depositions
[ ] Other

Click an option to get started.
```

Just click what you want to do!

## How Claude Knows Your Case Stage

Claude looks at your files and folders to understand where you are:

### Pre-Filing Stage
- No complaint filed yet
- Gathering evidence
- Researching viability
- Claude offers: Research options, damage calculations, evidence organization

### Discovery Stage
- Discovery documents in `03_DISCOVERY/`
- Recent discovery exchanges
- Claude offers: Discovery responses, new requests, deposition prep

### Motion Practice Stage
- Active motions in `02_PLEADINGS/03_Motions/`
- Recent motion filings
- Claude offers: Draft motions, responses, legal research

### Trial Prep Stage
- Trial date mentioned in timeline
- Exhibit lists being prepared
- Claude offers: Trial brief, jury instructions, witness outlines

## The Tracking System

Claude maintains two important files to remember your case:

### Session Notes (`.wepublic_defender/session_notes.md`)

This tracks:
- What you're currently working on
- What you completed last session
- Recent important findings
- Your last request (in case of crashes)

Example:
```markdown
## Currently Working On
- Drafting response to motion to dismiss

## Completed This Session
- Organized 15 documents from inbox
- Reviewed plaintiff's complaint
- Researched statute of limitations

## Recent Context
- Statute of limitations may be an issue
- Found strong negligence claim
- Opposing counsel filed motion to dismiss yesterday
```

### Case Timeline (`.wepublic_defender/case_timeline.md`)

This tracks major events:
- Documents filed with court
- Documents received
- Court orders
- Discovery exchanges
- Important deadlines

Example:
```markdown
### 2025-10-15 09:00 - DOCUMENT - Motion to Dismiss Filed
Status: Filed
Category: Pleading
File: 02_PLEADINGS/03_Motions/motion_to_dismiss.pdf
Notes: Filed via CM/ECF. Response due in 14 days.
```

## When Things Don't Load Automatically

Sometimes the automatic loading doesn't work. Here's what to do:

### Manual Refresh Command

Type this anytime to refresh Claude's understanding:
```
/start
```

This tells Claude to:
- Re-read your case files
- Check for new documents
- Update its understanding
- Offer fresh options

### When to Use Manual Refresh

- After adding many new documents
- When Claude seems confused
- After a long session (memory gets stale)
- When switching between different tasks

## Understanding the Options

When Claude presents options, they're intelligent based on your case:

### Deadline-Aware
If you have a motion response due in 3 days, that appears first with a warning.

### Stage-Appropriate
If you're in discovery, you get discovery options. If you're drafting a complaint, you get pre-filing options.

### Priority-Ordered
Most urgent tasks appear first, routine tasks last.

### Always Includes "Other"
Can't find what you need? Choose "Other" and tell Claude what you want.

## Customizing Behavior

### Skipping the Automation

If you prefer to dive straight into work:
```
Skip the suggestions, I want to [your specific task]
```

### Getting More Options

If the initial options don't fit:
```
Show me more options
```

Or:
```
I need help with something else
```

### Changing What Claude Tracks

You can tell Claude what to remember:
```
Add to session notes: Working on exhibit list for trial
```

Or:
```
Update timeline: Received discovery responses from defendant today
```

## Privacy and Security

### What Gets Saved

- Session notes stay in your case folder
- Timeline stays in your case folder
- Nothing is sent to cloud services automatically
- You control what information is tracked

### Clearing History

To start fresh (rarely needed):
```
Clear session notes and start fresh
```

This won't delete your case files, just the tracking.

## Common Scenarios

### Scenario 1: Continuing Yesterday's Work

You were drafting a motion yesterday. Today when you open Claude:

```
I see you were drafting a response to motion to dismiss.
Would you like to:
[ ] Continue drafting the response
[ ] Review what you've written so far
[ ] Research additional arguments
[ ] Something else
```

### Scenario 2: New Urgent Filing

Opposing counsel filed something new. Claude notices:

```
⚠️ New filing detected: Defendant's Motion for Summary Judgment
Response deadline: November 5 (14 days)

Would you like to:
[ ] Read and analyze the motion
[ ] Start drafting opposition
[ ] Research summary judgment standards
[ ] Request extension of time
```

### Scenario 3: Regular Check-in

No urgent deadlines, just daily work:

```
Good morning! Your case is in discovery phase.
No urgent deadlines this week.

What would you like to work on?
[ ] Review and organize recent document production
[ ] Draft next set of interrogatories
[ ] Prepare for upcoming depositions
[ ] Case strategy session
```

## Tips for Best Results

### Keep Your Inbox Clean
Move documents from `00_NEW_DOCUMENTS_INBOX/` regularly so Claude can track what's new.

### Update Important Events
Tell Claude about major events:
```
Update timeline: Motion hearing scheduled for Nov 15
```

### Use Descriptive Filenames
Instead of `document1.pdf`, use `2025-10-15_Defendant_Motion_to_Dismiss.pdf`

### Regular Organization
Run `/organize` periodically to keep files in the right places.

## Troubleshooting

### Claude Doesn't Remember Anything

**Solution**: Run `/start` to manually trigger the session start routine.

### Wrong Case Stage Detected

**Solution**: Tell Claude directly:
```
We're actually in discovery phase, not pre-filing
```

### Outdated Suggestions

**Solution**:
```
Refresh your understanding of the case status
```

### Too Many Options

**Solution**:
```
Just show me the most urgent tasks
```

## Advanced Features

### Crash Recovery

If Claude Code crashes while you're working, the session notes save your last action. When you restart:

```
I see you were working on: Reviewing plaintiff's motion
The session appears to have ended unexpectedly.
Would you like to continue where you left off?
```

### Multi-Session Awareness

Claude knows if you've been working a lot:

```
You've been working on this case for 3 hours today.
Recent work: Drafted 2 motions, reviewed 15 documents.
Consider taking a break, or would you like to continue?
```

### Intelligent Suggestions

Based on what you've done, Claude suggests what typically comes next:

```
You just finished drafting a motion to dismiss.
Typically, the next steps would be:
[ ] Run full review pipeline before filing
[ ] Create declaration to accompany motion
[ ] Draft proposed order
[ ] Prepare notice of motion
```

## Summary

Session Start Automation means:
- **No more repetition** - Claude knows your case
- **Intelligent suggestions** - Right options at the right time
- **Crash recovery** - Never lose your place
- **Deadline awareness** - Important dates front and center
- **Stage-appropriate help** - Relevant to where you are in litigation

The goal: Make it feel like you have a legal assistant who actually remembers your case and knows what needs to be done next.

## Next Steps

- Learn about the [Review Pipeline](Review-Pipeline)
- Master [Slash Commands](Slash-Commands-Reference)
- Understand [File Organization](File-Organization)
- Set up [Deep Research](Deep-Research-Workflow)
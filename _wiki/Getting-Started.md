# Getting Started with WePublicDefender

This guide will get you up and running with WePublicDefender in 5 minutes (assuming you've already completed setup).

## Prerequisites

Before starting, you should have:
- Claude Code installed and working
- WePublicDefender set up (see [Complete Beginner Setup](Complete-Beginner-Setup) if not)
- API keys configured
- Your case documents ready

## Quick Installation Check

Open your terminal in your case folder and run Claude Code:
```bash
claude
```

Then check your environment:
```
/check-env
```

If this shows your API keys and Python environment, you're ready!

## Your First Case Session

### Step 1: Initialize Your Case

If this is a brand new case folder:

```
/organize
```

This will:
- Create the standard legal folder structure
- Move any documents from the inbox to proper folders
- Set up case tracking files

### Step 2: Put Documents in Inbox

Place all your case documents in `00_NEW_DOCUMENTS_INBOX/`:
- Court documents
- Correspondence
- Evidence
- Contracts
- Everything related to your case

### Step 3: Let Claude Organize

Tell Claude to organize your documents:
```
/organize
```

Claude will:
- Read each document
- Determine what type it is
- Move it to the appropriate folder
- Keep track of what went where

### Step 4: Generate Initial Strategy

Get strategic recommendations:
```
/strategy
```

Claude will analyze your case and provide:
- Strength assessment
- Recommended claims
- Next steps
- Key deadlines
- Evidence needed

## Common Use Cases

### Review a Draft Motion

You've written a motion and want it reviewed:

```
/review 07_DRAFTS_AND_WORK_PRODUCT/motion_to_dismiss.md
```

This runs the full adversarial review pipeline:
1. Self-review for issues
2. Citation verification
3. Opposing counsel attack simulation
4. Final recommendations

### Research a Legal Topic

Need to research qualified immunity in the Fourth Circuit:

```
/research qualified immunity fourth circuit standard
```

### Draft a Document

Need to draft a response to a motion:

```
/draft response to motion to dismiss
```

Claude will:
1. Ask for key facts
2. Research applicable law
3. Draft the response
4. Offer to review it

### Deep Research for New Case

Starting a new case and need comprehensive research:

```
/deep-research-prep
```

This generates a research prompt for Claude.ai's Deep Research feature. Follow the instructions to get 50+ pages of legal research.

## Understanding the Pipeline

WePublicDefender uses an adversarial review pipeline. Here's what happens when you review a document:

1. **Self-Review**: Multiple AIs review for legal issues
2. **Citation Check**: Verifies all citations are still good law
3. **Opposing Counsel**: An AI attacks your document like opposing counsel would
4. **Consensus Building**: Finds issues all AIs agree on
5. **Iterative Fixes**: Fixes issues and re-reviews until clean

## Cost Management

### Checking Your Usage

See what you've spent:
```
Check my API usage
```

### Using Free Mode

Most commands have a free "guidance" mode:
```
Run self review in guidance mode on my motion
```

This gives you instructions instead of calling APIs.

### When to Use Paid Mode

Use external LLM mode for:
- Final document review before filing
- Citation verification with web search
- Opposing counsel simulation
- When you need multiple AI perspectives

## Session Management

### Claude Remembers Your Case

When you open Claude Code in your case folder, it automatically:
- Loads your case history
- Checks for deadlines
- Offers relevant next actions

No need to explain your case every time!

### Manual Refresh

If Claude seems confused or it's been a long session:
```
/start
```

This refreshes Claude's understanding of your case.

## What's Next?

### Immediate Next Steps

1. **Organize your documents**: `/organize`
2. **Run initial strategy**: `/strategy`
3. **Do deep research**: `/deep-research-prep`
4. **Review important documents**: `/review [filename]`

### Learn More

- [Session Start Automation](Session-Start-Automation) - How Claude remembers your case
- [Review Pipeline](Review-Pipeline) - Understanding adversarial review
- [Deep Research Workflow](Deep-Research-Workflow) - Comprehensive research guide
- [Slash Commands Reference](Slash-Commands-Reference) - All available commands

### Tips for Success

1. **Start with organization** - A well-organized case is easier to manage
2. **Use deep research early** - Better to know your case strength upfront
3. **Review before filing** - Always run the full pipeline on final documents
4. **Track your costs** - Check usage regularly to avoid surprises
5. **Ask Claude** - When in doubt, just describe what you need in plain English

## Troubleshooting Quick Reference

### Common Issues

**"Command not found"**
- Run `/check-env` to verify setup
- Restart Claude Code

**"API key error"**
- Check your `.env` file has the keys
- Verify your API accounts have credit

**"File not found"**
- Make sure you're in your case folder
- Use full file paths when needed

**"Claude seems confused"**
- Run `/start` to refresh context
- Restart Claude Code if needed

See [Troubleshooting](Troubleshooting) for detailed solutions.

## Getting Help

- **In Claude**: Just ask! "How do I draft a motion?"
- **Documentation**: You're reading it
- **GitHub Issues**: https://github.com/jackneil/wepublic_defender/issues

Remember: You're using sophisticated legal tech. Be patient with yourself as you learn!
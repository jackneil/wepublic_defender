# Deep Research Workflow

Deep Research is WePublicDefender's most powerful research feature. It uses Claude.ai's research capability to conduct comprehensive legal analysis with dozens of web searches in minutes.

## What is Deep Research?

Deep Research is different from regular research:

**Regular Research**: Quick lookup of specific legal questions
**Deep Research**: Comprehensive analysis of your entire case with 50+ interconnected searches

Think of it like hiring a research assistant who spends a full day researching every angle of your case and delivers a detailed report.

## When to Use Deep Research

### Perfect For:

- **Starting a new case** - Assess viability and strategy
- **Major motions** - Research for summary judgment, motion to dismiss
- **Complex legal questions** - Multiple theories and defenses
- **Case strategy planning** - Comprehensive analysis of options
- **Settlement evaluation** - Understanding case value

### Not Needed For:

- Simple procedural questions
- Quick statute lookups
- Basic citation checks
- Routine discovery responses

## Requirements

- **Claude Pro, Max, or Team account** (for Claude.ai access)
- **Web access** to https://claude.ai
- **10-15 minutes** for research to complete

## Step-by-Step Workflow

### Step 1: Generate Research Prompt

In Claude Code, type:
```
/deep-research-prep
```

Or if Claude suggests it:
```
You: I need to understand if I have a viable case

Claude: This appears to be a new case. Would you like me to generate a comprehensive deep research prompt?

You: Yes
```

### Step 2: Provide Case Details

Claude will ask for information:
```
Claude: I'll generate a deep research prompt. First, tell me:
1. What type of case is this?
2. Who are the parties?
3. What's the main dispute?
4. What state/federal jurisdiction?

You: Employment discrimination case. Me vs BigCorp. They fired me after I reported safety violations. Federal court in South Carolina.
```

### Step 3: Claude Generates Research Prompt

Claude creates a comprehensive prompt like:
```
# Deep Legal Research Request

## Case Overview
Employment discrimination and whistleblower retaliation case in D. South Carolina

## Research Objectives

### 1. Viable Claims Analysis
- Whistleblower protection under OSHA
- Retaliation under Title VII
- State law wrongful termination
- Public policy exceptions

### 2. Burden of Proof Requirements
- Prima facie case elements
- Burden-shifting framework
- Evidence requirements

### 3. Damages Assessment
- Economic damages (lost wages, benefits)
- Non-economic damages (emotional distress)
- Punitive damages availability
- Attorney's fees recovery

[... continues for 20+ sections ...]
```

### Step 4: Copy Entire Prompt

Select ALL text from start to end of the prompt. Copy to clipboard (Ctrl+C or Cmd+C).

### Step 5: Go to Claude.ai

1. Open browser
2. Go to https://claude.ai
3. Log in with your paid account

### Step 6: Enable Research Mode

Look at the bottom of the chat interface:

![Research Button Location]
- If button is WHITE → Click to enable
- Button turns BLUE → Research enabled
- Make sure "Web search" is also on

### Step 7: Paste and Send

1. Paste the entire prompt
2. Select model: **Claude Sonnet** (best for research)
3. Click Send

### Step 8: Wait for Research

Claude.ai will now:
```
Starting comprehensive research...
[Search 1/50] "whistleblower protection OSHA Fourth Circuit"
[Search 2/50] "retaliation burden of proof employment"
[Search 3/50] "South Carolina wrongful termination public policy"
...
```

This takes 5-15 minutes. Get coffee.

### Step 9: Download Results

When complete:
1. Click three dots menu (⋮) in top right
2. Select "Download conversation"
3. Save to: `YourCaseFolder/00_NEW_DOCUMENTS_INBOX/deep_research.md`

### Step 10: Return to Claude Code

Back in Claude Code terminal:
```
You: Done. I saved the research to inbox.

Claude: Found the research file. Analyzing findings...

KEY FINDINGS:
✓ Strong whistleblower claim under §1514A
✓ Viable retaliation claim
⚠ Statute of limitations concern (180 days for OSHA)
✓ Punitive damages possible

Generating GAMEPLAN.md with strategy...
```

## What Deep Research Analyzes

### Legal Viability
- Strength of each potential claim
- Required elements and your evidence
- Likely defenses and counters
- Precedent in your jurisdiction

### Procedural Requirements
- Statutes of limitations
- Filing requirements
- Jurisdictional issues
- Administrative prerequisites

### Strategic Considerations
- Best claims to pursue
- Claims to avoid
- Settlement leverage points
- Litigation risks

### Damage Analysis
- Available damage types
- Calculation methods
- Supporting evidence needed
- Similar case awards

### Defense Predictions
- What opposing counsel will argue
- Their strongest points
- Your vulnerabilities
- Counter-strategies

## Understanding Research Results

### The Research Output

Deep Research provides:
```markdown
## Claim 1: Whistleblower Retaliation

**Viability**: STRONG
**Key Statute**: 29 U.S.C. §1514A
**Circuit Precedent**: Favorable in 4th Circuit

**Elements You Must Prove**:
1. ✓ You engaged in protected activity (reporting violations)
2. ✓ Employer knew of the activity
3. ✓ You suffered adverse action (termination)
4. ? Causal connection (timing is close but need more)

**Supporting Cases**:
- Feldman v. Law Enforcement (4th Cir. 2019)
  - Similar facts, plaintiff won
  - Key: 2-month gap sufficient for causation

**Weaknesses**:
- Need documentation of safety reports
- Must file with OSHA within 180 days
```

### The Generated GAMEPLAN

Claude creates `GAMEPLAN.md`:
```markdown
# Case Strategy

## Immediate Actions (This Week)
1. File OSHA complaint (URGENT - approaching deadline)
2. Gather all safety report documentation
3. Contact witnesses from safety committee
4. Request personnel file from HR

## Claims to Pursue
1. Federal whistleblower (strongest)
2. Title VII retaliation (good)
3. State wrongful termination (backup)

## Claims to Avoid
- Defamation (too hard to prove)
- Intentional infliction (high bar in SC)

## Settlement Strategy
- Strong case worth $200-400K
- Will get stronger after discovery
- Consider mediation after depositions
```

## Tips for Better Research

### Be Specific with Facts

Good:
```
Reported OSHA violations on May 1, fired May 15, no prior discipline
```

Bad:
```
Reported some problems, got fired later
```

### Include Key Documents

Mention important documents:
```
I have emails showing I reported violations, termination letter says "restructuring"
```

### Specify Jurisdiction

Always include:
- Federal or state court
- Which state
- Which federal circuit
- Specific court if known

### Ask for Specific Analysis

You can add to the prompt:
```
Also research:
- Whether arbitration agreement is enforceable
- If punitive damages are available
- Class action potential
```

## Common Issues and Solutions

### Research Too Generic

**Problem**: Results don't seem specific to your case

**Solution**: Provide more facts when Claude asks. Include dates, specific claims, dollar amounts.

### Research Taking Too Long

**Problem**: Research running for 20+ minutes

**Solution**:
- Check if web search is enabled
- Try refreshing and restarting
- Break into smaller research requests

### Can't Download Results

**Problem**: No download option in Claude.ai

**Solution**: Copy-paste the entire response:
```
You: Here are the research results:
[Paste everything]
```

### Results Not Processing

**Problem**: Claude Code can't find research file

**Solution**:
```
The file is in 00_NEW_DOCUMENTS_INBOX/deep_research.md
```

## Cost Considerations

### Claude.ai Subscription

Deep Research requires paid Claude.ai account:
- **Pro** ($20/month) - Limited research
- **Max 5x** (~$100/month) - Good for most cases
- **Max 20x** (~$200/month) - Heavy research needs

### When It's Worth It

One deep research session can replace:
- 10+ hours of manual research
- Multiple consultations with lawyers
- Expensive legal research database subscriptions

## Advanced Techniques

### Iterative Research

After initial research:
```
Based on the research, generate a follow-up deep research prompt focusing on the whistleblower angle
```

### Comparative Research

```
Generate deep research comparing my case to Johnson v. BigCorp
```

### Jurisdiction-Specific Research

```
Generate deep research on how the Fourth Circuit specifically handles whistleblower cases
```

### Opposition Research

```
Generate deep research on how defendants typically attack these claims
```

## Integration with Other Features

### After Deep Research

1. **Update Strategy**: `/strategy` incorporates research findings
2. **Draft Documents**: `/draft` uses research for legal arguments
3. **Review Pipeline**: Reviews check against research findings
4. **Citation Verification**: Ensures cases from research are still good law

### Research-Informed Drafting

```
You: Draft motion to dismiss based on the deep research findings

Claude: Using research findings to draft:
- Emphasizing Fourth Circuit's favorable precedent
- Citing Feldman case from research
- Addressing timing issue identified
```

## Troubleshooting

### "Research Not Available"

You need paid Claude.ai account. Research isn't available on free tier.

### "Web Search Not Working"

1. Make sure Research mode is enabled (blue button)
2. Check "Web search" toggle is on
3. Try different browser

### "Results Are Confusing"

Ask Claude Code to summarize:
```
Explain the research findings in simple terms
```

### "Missing Important Issues"

You can run additional research:
```
The research missed the discrimination angle. Can you generate another prompt for that?
```

## Best Practices

### Start Early

Run deep research at the beginning of your case for best strategic planning.

### Save Everything

Keep research results in `06_RESEARCH/` for reference throughout case.

### Update Regularly

As case develops:
```
Generate updated deep research based on new developments
```

### Verify Critical Points

Deep research is comprehensive but verify critical citations:
```
/research Feldman v. Law Enforcement Fourth Circuit 2019
```

## Summary

Deep Research is your power tool for comprehensive legal analysis:
- **Saves days of research** in 10 minutes
- **Analyzes every angle** of your case
- **Provides actionable strategy** not just information
- **Costs fraction** of lawyer research time

Use it when starting your case, facing major motions, or needing comprehensive strategy updates.

## Next Steps

- Run your first deep research
- Read generated `GAMEPLAN.md`
- Use findings for [drafting](Slash-Commands-Reference#draft)
- Incorporate into [review pipeline](Review-Pipeline)
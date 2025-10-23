# Review Pipeline - The Adversarial AI System

The review pipeline is WePublicDefender's secret weapon. Instead of one AI reviewing your document, multiple AIs attack it from different angles until it's bulletproof.

## What is the Review Pipeline?

Think of it like this:
- **Traditional review**: One lawyer reads your document and gives feedback
- **WePublicDefender pipeline**: 5 different lawyers review it, argue about what's wrong, and keep reviewing until they all agree it's perfect

## How the Pipeline Works

### The Complete Pipeline Process

```
DOCUMENT GOES IN
    ↓
Phase 1: Self-Review (Multiple AIs review independently)
    ↓
Phase 2: Citation Verification (Check all legal citations)
    ↓
Phase 3: Opposing Counsel Attack (AI pretends to be other side)
    ↓
Phase 4: Fact Verification (Check claims against evidence)
    ↓
Phase 5: Final Validation
    ↓
Any changes made? → YES → Start over from Phase 1
                 ↓
                NO → DOCUMENT READY TO FILE
```

### Why It Loops Until Perfect

Legal documents are interconnected:
- Fix one issue → Might create another issue
- Change a citation → Might weaken an argument
- Strengthen one claim → Might contradict another

The pipeline keeps looping until a complete pass makes ZERO changes. Only then is it truly ready.

## The Five Phases Explained

### Phase 1: Self-Review

**What happens**: Multiple AIs independently review your document for legal issues.

**What they look for**:
- Missing legal elements
- Weak arguments
- Procedural errors
- Formatting issues
- Unclear writing
- Missing citations

**Example findings**:
```
CRITICAL: Missing jurisdiction statement in introduction
MAJOR: No legal standard provided for negligence claim
MINOR: Passive voice in paragraph 5 weakens argument
```

### Phase 2: Citation Verification

**What happens**: Every legal citation is checked to ensure it's still good law.

**What they look for**:
- Overruled cases
- Superseded statutes
- Incorrect citations
- Missing pin cites
- Wrong jurisdiction citations

**Example findings**:
```
WARNING: Smith v. Jones was overruled by Johnson v. State (2023)
ERROR: Citation format incorrect - needs pin cite
ISSUE: Citing 9th Circuit case as binding in 4th Circuit
```

### Phase 3: Opposing Counsel Attack

**What happens**: An AI pretends to be the opposing counsel and attacks your document.

**What they look for**:
- Weak arguments to exploit
- Missing defenses
- Procedural violations
- Fact disputes
- Alternative theories

**Example attack**:
```
"Your client waived this argument by not raising it initially"
"The arbitration clause in paragraph 47 makes this filing void"
"You've admitted facts that destroy your causation argument"
```

### Phase 4: Fact Verification

**What happens**: Claims in your document are checked against evidence.

**What they look for**:
- Unsupported factual claims
- Inconsistent dates/times
- Missing evidence citations
- Contradictions with evidence
- Exaggerated claims

**Example findings**:
```
UNSUPPORTED: "Defendant never responded" - but email shows response
INCORRECT: Date listed as June 15, evidence shows June 17
MISSING: No evidence cited for damages amount claimed
```

### Phase 5: Final Validation

**What happens**: Final check that document is ready for filing.

**What they look for**:
- All previous issues resolved
- Document internally consistent
- Proper formatting
- Complete and ready

## Understanding the Modes

### Guidance Mode (Free)

When you run in guidance mode:
```
/review my_motion.md --mode guidance
```

Claude gives you a checklist to review yourself:
- What to look for
- Common issues to check
- Questions to ask yourself

**Cost**: $0 - Claude guides you to do the review

### External-LLM Mode (Costs Money)

When you run in external-LLm mode:
```
/review my_motion.md --mode external-llm
```

Multiple AIs actually review your document:
- GPT-5 reviews it
- Grok-4 reviews it
- They compare findings
- You get specific issues to fix

**Cost**: $2-10 depending on document size

## Real Example: What You'll See

Here's an actual review session:

```
You: /review motion_to_dismiss.md

=== PIPELINE RUN #1 ===

PHASE 1: Self-Review
- Claude: Found 5 issues
- GPT-5: Found 8 issues
- Grok-4: Found 6 issues
CONSENSUS: 4 critical issues all models found
ACTION: Fixing critical issues...

PHASE 2: Citation Check
- 3 citations need verification
- 1 case was overruled
ACTION: Replacing bad citation...

PHASE 3: Opposing Counsel
- "You forgot arbitration waiver argument"
ACTION: Adding waiver section...

PHASE 4: Fact Verify
- Date wrong in paragraph 3
- Unsupported claim in paragraph 7
ACTION: Fixing facts...

PHASE 5: Final Check
Total changes: 11
⚠️ Changes made - must re-run pipeline

=== PIPELINE RUN #2 ===

PHASE 1: Self-Review - Found 1 minor issue
PHASE 2: Citations - All valid
PHASE 3: Opposing - No fatal flaws
PHASE 4: Facts - All verified
PHASE 5: Final - 1 change made

⚠️ Changes made - must re-run pipeline

=== PIPELINE RUN #3 ===

PHASE 1: Clean
PHASE 2: Clean
PHASE 3: Clean
PHASE 4: Clean
PHASE 5: Clean

✅ ZERO CHANGES - DOCUMENT READY TO FILE!

Total iterations: 3
Total issues fixed: 12
Total cost: $8.47
Equivalent review time by lawyer: ~3 hours ($1,200)
```

## When to Use the Pipeline

### Always Before Filing

Run the full pipeline on any document you're going to file with the court.

### After Major Edits

Changed significant portions? Run the pipeline to ensure consistency.

### When Stakes Are High

Motion for summary judgment? Response to motion to dismiss? Run the full pipeline.

### For Learning

Run it on your drafts to learn what issues you commonly miss.

## Cost Optimization

### Start with Guidance Mode

First, run in free guidance mode:
```
Run self-review in guidance mode
```

Fix obvious issues yourself, then run external-llm mode for final check.

### Run Individual Phases

Just need citations checked?
```
Run citation verification only
```

### Use Single Model

For less critical documents:
```
/review draft.md --model gpt-5
```

Uses only one AI instead of multiple (half the cost).

## Understanding Consensus

When multiple AIs review, consensus matters:

### 100% Consensus (All AIs Agree)
- **Critical issue** - must fix
- Example: "Missing jurisdiction statement"

### 60-80% Consensus (Most Agree)
- **Important issue** - should fix
- Example: "Weak causation argument"

### Single AI Finding
- **Possible issue** - consider fixing
- Example: "Could add alternative argument"

The system prioritizes fixes based on consensus level.

## Common Issues Found

### Procedural Errors
- Wrong filing deadlines
- Missing required elements
- Incorrect court rules
- Wrong jurisdiction citations

### Legal Argument Issues
- Missing legal standard
- Weak analogies
- Failure to distinguish opposing cases
- Incomplete arguments

### Citation Problems
- Overruled cases
- Wrong jurisdiction
- Missing pin cites
- Incorrect quotations

### Factual Issues
- Unsupported claims
- Wrong dates/times
- Missing evidence citations
- Contradictions

## The Iteration Pattern

Reviews typically follow this pattern:

1. **First run**: 10-20 issues found
2. **Second run**: 3-5 issues found
3. **Third run**: 0-1 issues found
4. **Fourth run**: Clean pass

Each iteration catches problems created by previous fixes.

## Best Practices

### Don't Skip Iterations

If the pipeline says "run again", run it again. Each iteration matters.

### Fix Critical Issues First

Focus on consensus critical issues before minor ones.

### Keep Evidence Handy

Fact verification needs access to your evidence files in `04_EVIDENCE/`.

### Save Versions

Before running pipeline:
```
Save current version as motion_v1.md
```

After fixes:
```
Save as motion_v2.md
```

### Review the Reviews

Read what each AI said, not just the consensus. Sometimes minority opinions matter.

## Advanced Features

### Web Search Integration

For citation verification with current law:
```
/review motion.md --web-search
```

Searches for recent cases that might affect your citations.

### Custom Review Agents

You can configure which AIs review:
```json
{
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-5", "grok-4", "claude-3", "gemini"]
    }
  }
}
```

More models = higher confidence but higher cost.

### Incremental Saves

Reviews are saved immediately to `.wepublic_defender/reviews/` so you don't lose work if something crashes.

## Troubleshooting

### Review Taking Too Long

**Problem**: Review has been running for 10+ minutes

**Solution**: Check background tasks with `/bashes` command. Large documents with web search can take 5-10 minutes.

### Different AIs Disagree Completely

**Problem**: No consensus on issues

**Solution**: This suggests document needs major restructuring. Consider starting fresh or getting human help.

### Cost Too High

**Problem**: Reviews costing $20+

**Solution**:
- Break document into sections
- Review sections separately
- Use guidance mode first
- Skip web search if not needed

### Can't Find Evidence Files

**Problem**: Fact verification fails to find evidence

**Solution**: Ensure evidence is in `04_EVIDENCE/` folder and filenames are descriptive.

## Tips for Success

### Write with the Pipeline in Mind

Knowing what the pipeline checks for helps you write better first drafts:
- Always include jurisdiction statement
- Always cite legal standards
- Always support facts with evidence
- Always use pin cites

### Use Plan Mode for Fixes

After review finds issues:
1. Type `/plan` to enter Plan Mode
2. Say "Fix the issues from the review"
3. Claude presents complete plan
4. Review plan before approving

### Trust the Consensus

If all AIs agree something is wrong, it's wrong. Don't argue with unanimous consensus.

### Learn from Patterns

If pipeline always finds same issues, you have a writing pattern to fix.

## Summary

The review pipeline is what makes WePublicDefender powerful:
- **Multiple perspectives** catch different issues
- **Iterative refinement** ensures consistency
- **Adversarial testing** finds weaknesses before opposing counsel does
- **Consensus building** prioritizes real issues
- **Continuous validation** ensures quality

Result: Documents that have been reviewed more thoroughly than most lawyer-drafted filings, at a fraction of the cost.

## Next Steps

- Learn [Slash Commands](Slash-Commands-Reference) to control the pipeline
- Understand [Cost Guide](Cost-Guide) for budget planning
- Read about [Deep Research](Deep-Research-Workflow) to improve your arguments
- Check [Troubleshooting](Troubleshooting) if you hit issues
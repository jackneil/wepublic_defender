# Cost Guide

Understanding the costs of using WePublicDefender helps you budget effectively and avoid surprises. This guide breaks down all costs and shows you how to optimize spending.

## Cost Overview

### One-Time Costs
- **Claude Code Subscription**: $100-200/month
- **Initial API Credits**: $20-50 to start

### Ongoing Costs
- **API Usage**: $5-50/month typical
- **Claude Subscription**: Monthly recurring

### Comparison
- **Lawyer Hour**: $200-600
- **Full Document Review**: $3-10 with WePublicDefender
- **ROI**: One saved lawyer hour pays for a month

## Subscription Costs

### Claude Code Plans

| Plan | Monthly Cost | What You Get | Good For |
|------|-------------|--------------|----------|
| Pro | $20 | Basic access, limited usage | Simple cases, light use |
| Max 5x | ~$100 | 5x more usage | Most cases |
| Max 20x | ~$200 | 20x more usage | Complex cases, heavy use |

**Which plan?**
- **Max 5x**: If you have <50 documents and work a few hours daily
- **Max 20x**: If you have 100+ documents or work all day
- **Pro**: Only if you're testing the waters

## API Costs

### OpenAI Pricing

**GPT-4o** (Best model):
- Input: $5.00 per 1M tokens
- Output: $15.00 per 1M tokens

**GPT-4o-mini** (Cheaper):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

**What's a token?**
- ~4 characters
- ~0.75 words
- 1 page ≈ 500 tokens

### xAI (Grok) Pricing

**Grok-4**:
- Input: $5.00 per 1M tokens
- Output: $15.00 per 1M tokens

### Real Document Costs

| Document Type | Size | Single Review | Full Pipeline |
|--------------|------|---------------|---------------|
| Motion (5 pages) | 2.5K tokens | $0.05 | $0.50 |
| Brief (20 pages) | 10K tokens | $0.20 | $2.00 |
| Contract (50 pages) | 25K tokens | $0.50 | $5.00 |
| Discovery (100 pages) | 50K tokens | $1.00 | $10.00 |

## Operation Costs

### Review Pipeline Costs

**Guidance Mode** (Free):
```
/review motion.md --mode guidance
Cost: $0.00
```

**Single Model**:
```
/review motion.md --model gpt-4o-mini
Cost: ~$0.10-0.50
```

**Full Pipeline** (Multiple models):
```
/review motion.md --mode external-llm
Cost: ~$2.00-10.00
```

### Cost Breakdown by Phase

1. **Self-Review**: $0.50-2.00
2. **Citation Check**: $0.50-2.00 (+$1-3 if web search)
3. **Opposing Counsel**: $0.50-2.00
4. **Fact Verify**: $0.30-1.00
5. **Final Review**: $0.20-1.00

**Total per iteration**: $2.00-8.00
**Typical document** (3 iterations): $6.00-24.00

### Research Costs

**Quick Research**:
```
/research statute of limitations
Cost: $0.10-0.50
```

**Deep Research**:
```
/deep-research-prep
Cost: $0 (uses Claude.ai subscription)
```

### Drafting Costs

**Simple Draft**:
```
/draft letter requesting extension
Cost: $0.20-1.00
```

**Complex Draft**:
```
/draft motion for summary judgment
Cost: $1.00-5.00
```

## Cost Tracking

### Check Current Usage

**Today's usage**:
```
Show me what I've spent today
```

**This month**:
```
Show me this month's API costs
```

**By operation**:
```
What did the last review cost?
```

### Usage Log Location

File: `.wepublic_defender/usage_log.csv`

Format:
```csv
timestamp,operation,model,tokens_in,tokens_out,cost
2025-10-15 09:30:00,review,gpt-4o,5000,2000,0.45
```

### Provider Dashboards

Check actual billing:
- **OpenAI**: https://platform.openai.com/usage
- **xAI**: https://console.x.ai/billing
- **Anthropic**: Check subscription page

## Cost Optimization Strategies

### Use Guidance Mode First

**Strategy**: Start free, then paid review

```
Step 1: /review draft.md --mode guidance    # $0.00
Step 2: Fix obvious issues yourself
Step 3: /review draft.md --mode external-llm # $3.00
```

**Savings**: 50-70% by fixing obvious issues first

### Use Cheaper Models for Drafts

**For non-critical work**:
```
/review early_draft.md --model gpt-4o-mini
```

**For final documents**:
```
/review final_motion.md --model gpt-4o
```

### Break Large Documents

Instead of reviewing 100-page document:
```
Review pages 1-25: $2.50
Review pages 26-50: $2.50
Review pages 51-75: $2.50
Review pages 76-100: $2.50
Total: $10.00

vs

Review all 100 pages: $15.00
```

### Skip Unnecessary Phases

**Just need citations checked?**
```
Run citation verification only
```

**Don't need web search?**
```
/review motion.md --no-web-search
```

### Batch Operations

**Good**: Review multiple documents at once
```
Review these three motions together
```

**Bad**: Review same document repeatedly
```
Review version 1, then version 2, then version 3
```

## Budget Planning

### Typical Case Budgets

**Simple Case** (1-2 months):
- Claude Max 5x: $100/month
- API costs: $30-50 total
- **Total**: $200-250

**Average Case** (3-6 months):
- Claude Max 5x: $100/month
- API costs: $30-50/month
- **Total**: $400-900

**Complex Case** (6-12 months):
- Claude Max 20x: $200/month
- API costs: $50-100/month
- **Total**: $1,500-3,600

### Daily Budgets

**Conservative** ($5/day):
- 1-2 document reviews
- Quick research
- Basic drafting

**Moderate** ($15/day):
- 3-5 document reviews
- Deep research
- Complex drafting

**Heavy** ($30/day):
- Full pipeline reviews
- Multiple drafts
- Extensive research

## Cost Control Settings

### Set Spending Limits

**OpenAI**:
1. Go to https://platform.openai.com/account/limits
2. Set monthly budget
3. Set alert threshold

**Configuration**:
```json
{
  "cost_control": {
    "max_cost_per_review": 10.00,
    "max_cost_per_day": 30.00,
    "warn_at_cost": 5.00
  }
}
```

### Alerts and Warnings

Claude warns you:
```
⚠️ This review will cost approximately $8.50
Proceed? (yes/no)
```

## Free Alternatives

### Always Free Operations

These never cost API fees:
- `/organize` - File organization
- `/timeline` - View/update timeline
- `/check-env` - Environment check
- Guidance mode for all commands
- Plain conversation with Claude Code

### Reducing Costs to Zero

Use only guidance mode:
```
All operations in guidance mode only
```

You'll get:
- Checklists instead of AI review
- Templates instead of AI drafting
- Instructions instead of automation

## Cost vs Value Analysis

### What You're Replacing

| Service | Lawyer Cost | WePublicDefender Cost | Savings |
|---------|------------|------------------------|---------|
| Document Review (3 hrs) | $900-1,800 | $5-10 | 99% |
| Legal Research (5 hrs) | $1,500-3,000 | $0-5 | 99% |
| Motion Drafting (8 hrs) | $2,400-4,800 | $10-20 | 99% |
| Citation Check (2 hrs) | $600-1,200 | $2-5 | 99% |

### ROI Examples

**Example 1**: Motion to Dismiss
- Lawyer quote: $3,000
- WePublicDefender: $15 (draft + review)
- Savings: $2,985

**Example 2**: Discovery Responses
- Lawyer quote: $5,000
- WePublicDefender: $30
- Savings: $4,970

## Tips for Managing Costs

### Daily Practices

1. **Check usage each morning**:
   ```
   What did I spend yesterday?
   ```

2. **Use guidance mode for drafts**

3. **Save external-llm for final reviews**

### Weekly Practices

1. **Review usage log**
2. **Check provider dashboards**
3. **Adjust settings if overspending**

### Red Flags

Watch for:
- Single operation >$20
- Daily spending >$50
- Repeated reviews of same document
- Web search on every operation

## When to Spend More

### Worth the Cost

- **Final documents** before filing
- **Critical motions** (summary judgment, dismissal)
- **Response deadlines** when time limited
- **Complex legal research**

### Not Worth It

- **Early drafts** (use guidance)
- **Simple letters**
- **Routine discovery**
- **Testing/learning**

## Billing Issues

### Common Problems

**"Insufficient credits"**:
- Add payment method
- Purchase more credits
- Check spending limits

**"Rate limit exceeded"**:
- Wait 60 seconds
- Use different model
- Check daily limits

**"Unexpected charges"**:
- Check usage log
- Review operations
- Verify not running duplicate reviews

## Getting Help with Costs

### Ask Claude

```
Why did that review cost $15?
How can I reduce my API costs?
Show me cheaper alternatives for this task.
```

### Check Documentation

- This Cost Guide
- [Configuration](Configuration) for settings
- [Performance Optimization](Performance-Optimization)

## Summary

### Key Takeaways

1. **Total monthly cost**: $150-300 typical
2. **Per document**: $2-10 for full review
3. **Guidance mode**: Always free alternative
4. **ROI**: Saves 95-99% vs lawyer costs

### Cost-Saving Checklist

- [ ] Use guidance mode first
- [ ] Break large documents
- [ ] Skip unnecessary web search
- [ ] Use cheaper models for drafts
- [ ] Batch similar operations
- [ ] Set spending limits
- [ ] Monitor daily usage

Remember: Even at maximum spending, you're paying less than one hour of lawyer time for a month of AI assistance.

## Next Steps

- Configure [cost controls](Configuration#cost-control-settings)
- Learn [optimization techniques](Performance-Optimization)
- Understand the [review pipeline](Review-Pipeline)
- Start with [basic usage](Basic-Usage)
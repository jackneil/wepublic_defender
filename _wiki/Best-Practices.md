# Best Practices

This guide provides proven strategies and recommendations for effectively using WePublicDefender in your legal case.

## Document Management Best Practices

### File Naming Conventions

**Always use consistent naming**:

✅ **Good**:
```
2025-10-15_Motion_to_Dismiss_v1.md
2025-10-15_Motion_to_Dismiss_v2.md
2025-10-15_Motion_to_Dismiss_FINAL.md
```

❌ **Bad**:
```
motion.docx
motion2.docx
motion_final_FINAL_v2.docx
```

### Version Control

**Never overwrite - always create new versions**:

1. Save original: `complaint_ORIGINAL.md`
2. Working drafts: `complaint_v1.md`, `complaint_v2.md`
3. After review: `complaint_v3_post_review.md`
4. Final version: `complaint_FINAL.md`

### Organization Discipline

**Daily organization routine**:
```
Morning:
1. /organize - Process inbox
2. Archive old drafts
3. Update case timeline

Evening:
1. Move today's work to proper folders
2. Update session notes
3. Check tomorrow's deadlines
```

## Review Pipeline Best Practices

### Progressive Review Strategy

**Start free, end thorough**:

```
Stage 1: Guidance mode self-check (free)
         Fix obvious issues yourself

Stage 2: Single model review ($2-5)
         Address major problems

Stage 3: Full pipeline before filing ($5-15)
         Comprehensive validation
```

### When to Use Each Mode

**Guidance Mode**:
- First drafts
- Learning what to look for
- Budget constraints
- Non-critical documents

**External-LLM Mode**:
- Final documents before filing
- Critical motions
- When stakes are high
- Citation verification

### Review Timing

**Best times to review**:
- After completing first draft
- Before sending to opposing counsel
- 24 hours before filing deadline
- After incorporating major changes

## Cost Management Best Practices

### Daily Budget Planning

**Set daily limits**:
```
Conservative ($5/day):
- Morning: Organize (free)
- Afternoon: One guidance review (free)
- Evening: One AI review ($3-5)

Moderate ($15/day):
- Multiple AI reviews
- Research tasks
- Document drafting
```

### Smart Model Selection

**Match model to task**:

| Task | Model | Cost | Why |
|------|-------|------|-----|
| Early drafts | gpt-4o-mini | Low | Good enough for structure |
| Final review | gpt-4o | Medium | Best reasoning |
| Web search | grok-4 | High | Real-time information |
| Quick checks | Single model | Low | Faster, cheaper |

### Track Everything

**Weekly cost review**:
```
Every Friday:
1. Check total week spending
2. Review cost per document
3. Identify expensive operations
4. Adjust next week's approach
```

## Legal Strategy Best Practices

### Research Before Drafting

**Always research first**:

```
Wrong: Draft → Research → Rewrite
Right: Research → Outline → Draft → Review
```

**Research workflow**:
1. `/deep-research-prep` for comprehensive analysis
2. `/research [specific topics]` for focused questions
3. Update `06_RESEARCH/` with findings
4. Reference research while drafting

### Citation Management

**Maintain citation log**:

`06_RESEARCH/CITATIONS_LOG.md`:
```markdown
## Verified Citations

### Smith v. Jones, 123 F.3d 456 (4th Cir. 2019)
- Verified: 2025-10-15
- Good law: Yes
- Proposition: Qualified immunity standard
- Used in: Motion to Dismiss ¶15

### Johnson v. State, 789 S.C. 123 (2020)
- Verified: 2025-10-14
- Good law: Yes
- Proposition: Negligence elements
- Used in: Complaint ¶¶23-25
```

### Argument Development

**Build arguments incrementally**:

1. Start with basic legal framework
2. Add supporting cases
3. Include factual support
4. Address counter-arguments
5. Review and strengthen

## Workflow Best Practices

### Morning Routine

**Start each day consistently**:

```
1. Open Claude Code in case folder
2. Let automation load context
3. Review presented options
4. Check deadlines
5. Plan day's priorities
```

### Document Processing Workflow

**For new documents from opposing counsel**:

```
1. Save to inbox
2. /organize
3. Quick review for urgency
4. Calendar response deadline
5. /research relevant law
6. Draft response
7. /review before filing
```

### Pre-Filing Checklist

**Before filing anything**:

- [ ] Run full review pipeline
- [ ] Verify all citations
- [ ] Check local rules compliance
- [ ] Confirm deadline
- [ ] Generate required attachments
- [ ] Prepare certificate of service

## Session Management Best Practices

### Keep Context Fresh

**Refresh regularly**:
- After 2-3 hours of work
- When switching between tasks
- After adding many documents
- If Claude seems confused

```
/start  # Refreshes context
```

### Update Tracking Files

**After every significant action**:

```
Update session notes: Completed motion draft
Update timeline: Filed response to motion to dismiss
```

### Use Plan Mode for Critical Work

**When to use Plan Mode**:
- Processing review results
- Making strategic decisions
- Implementing complex fixes
- Before major changes

```
/plan
[Claude presents plan]
[Review carefully]
[Approve or modify]
```

## Security Best Practices

### Protect Sensitive Information

**Never include in documents**:
- Social Security numbers (use XXX-XX-1234)
- Full account numbers (use ****1234)
- Personal addresses (unless required)
- Minor children's names

**Mark privileged documents**:
```
PRIVILEGED_attorney_client_communication.pdf
CONFIDENTIAL_settlement_discussion.md
```

### API Key Security

**Protect your API keys**:
- Never share `.env` file
- Don't commit to git
- Use unique keys per case
- Rotate keys if compromised
- Set spending limits

### Backup Critical Files

**Regular backups**:
```
Weekly:
- Copy entire case folder
- Export important documents
- Save to external drive/cloud
```

## Quality Control Best Practices

### Multi-Stage Review

**Never rely on single review**:

```
Stage 1: Self-review (you)
Stage 2: AI guidance mode
Stage 3: AI external review
Stage 4: Final human review
```

### Fact Verification

**Always verify facts against evidence**:

```
Claim: "Email sent on October 15"
Check: 04_EVIDENCE/emails/2025-10-15_email.pdf
Verify: Date, sender, content match
```

### Consistency Checking

**Maintain consistency across documents**:
- Same dates throughout
- Consistent party names
- Matching legal theories
- Aligned facts

## Performance Best Practices

### Optimize for Speed

**Process documents efficiently**:

1. Break large documents into sections
2. Review sections in parallel
3. Use appropriate models for each task
4. Cache frequently accessed research

### Reduce Token Usage

**Write concisely**:
- Remove redundant sections
- Use clear, direct language
- Avoid excessive quotations
- Summarize when appropriate

### Batch Similar Operations

**Group related tasks**:

```
Good: Review all motions together
Bad: Review one motion, do other work, review another motion
```

## Communication Best Practices

### With Claude

**Be specific**:

Instead of: "Review this"
Say: "Review my motion for jurisdiction issues and missing citations"

**Provide context**:
```
"This is a response to their motion to dismiss.
They're arguing lack of jurisdiction.
Focus on personal jurisdiction arguments."
```

### Document Headers

**Include key information**:

```markdown
# Motion to Dismiss
Case: Smith v. Jones
Case No: 1:24-cv-00123
Filed: [Date]
Response Due: [Date]
```

## Learning Best Practices

### Learn from Reviews

**Study review feedback**:
- What issues appear repeatedly?
- Which citations were problematic?
- What arguments were weak?

**Create personal checklist**:
```
My Common Issues:
- [ ] Include jurisdiction statement
- [ ] Add legal standard section
- [ ] Support with local cases
- [ ] Include prayer for relief
```

### Build Knowledge Base

**Document learnings**:

`06_RESEARCH/lessons_learned.md`:
```markdown
## What I've Learned

### Motion Practice
- Always cite local rules
- Include proposed order
- Meet and confer requirement

### This Judge's Preferences
- Prefers shorter briefs
- Wants pinpoint citations
- Strict on deadlines
```

## Collaboration Best Practices

### Working with Human Lawyers

**Prepare for lawyer review**:

1. Run full pipeline first
2. Create summary of issues found
3. Highlight areas needing expertise
4. Prepare specific questions

**Handoff document**:
```markdown
## For Lawyer Review

Document: Motion for Summary Judgment
AI Reviews: Complete
Issues Fixed: 12

Needs Human Review:
1. Strategic decision on Claim 3
2. Local counsel rule compliance
3. Judge's standing order requirements

Questions:
1. Should we include alternative arguments?
2. Is the damages calculation legally sufficient?
```

## Error Prevention Best Practices

### Common Mistakes to Avoid

**Never**:
- File without citation verification
- Ignore consensus critical issues
- Skip review on final documents
- Assume AI is always right
- File documents with track changes

**Always**:
- Verify facts against evidence
- Check deadlines twice
- Review local rules
- Keep human oversight
- Save versions before changes

## Summary Checklist

### Daily Best Practices
- [ ] Start with /organize
- [ ] Check deadlines
- [ ] Update tracking files
- [ ] Use appropriate review modes
- [ ] Monitor costs

### Document Best Practices
- [ ] Use consistent naming
- [ ] Create versions, don't overwrite
- [ ] Research before drafting
- [ ] Review before filing
- [ ] Verify all citations

### Cost Best Practices
- [ ] Set daily budget
- [ ] Use guidance mode first
- [ ] Choose appropriate models
- [ ] Track spending
- [ ] Batch operations

### Quality Best Practices
- [ ] Multi-stage review
- [ ] Verify facts
- [ ] Check consistency
- [ ] Learn from feedback
- [ ] Maintain human oversight

## Next Steps

- Implement [File Organization](File-Organization) system
- Learn [Review Pipeline](Review-Pipeline) stages
- Understand [Cost Guide](Cost-Guide)
- Explore [Advanced Features](Advanced-Features)
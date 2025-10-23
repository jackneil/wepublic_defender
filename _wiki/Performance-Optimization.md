# Performance Optimization

Strategies to make WePublicDefender faster and more cost-effective.

## Understanding Performance Bottlenecks

### What Takes Time in WePublicDefender

1. **External LLM API Calls** (3-30 seconds per call)
   - Self-review with multiple models: 5-15 seconds
   - Citation verification with web search: 10-30 seconds
   - Opposing counsel review: 5-15 seconds
   - Multiple models in parallel: Same time, but 2x cost

2. **Web Search Operations** (5-15 seconds per search)
   - Citation verification requires web access
   - Deep research uses extensive web searches
   - Each search adds latency

3. **Document Processing** (1-10 seconds)
   - Large PDFs take time to convert to images
   - Reading multi-page documents
   - Parsing complex legal citations

4. **Pipeline Iterations** (Multiplies all above)
   - Each pipeline run repeats all phases
   - Multiple iterations for quality mean more time
   - Trade-off: Speed vs. thoroughness

## Optimization Strategies

### 1. Use Guidance Mode When Possible

**Guidance mode is FREE and INSTANT** - no external API calls.

```bash
# Slow (costs money, takes time)
wpd-run-agent --agent self_review --file draft.md --mode external-llm

# Fast (free, instant)
wpd-run-agent --agent self_review --file draft.md --mode guidance
```

**When to use guidance:**
- Initial drafting
- File organization (always guidance-only)
- Quick reviews where you want to do the work yourself
- Learning workflows
- Budget-conscious reviews

**When external-llm is worth it:**
- Citation verification (needs web search)
- Opposing counsel attacks (adversarial perspective)
- Final pre-filing validation (catch what you missed)

### 2. Run Single Model Instead of Multiple

If agent config has multiple models, **all run in parallel** by default (2x cost, same time).

```bash
# Runs both GPT-5 and Grok-4 (2x cost)
wpd-run-agent --agent self_review --file draft.md --mode external-llm

# Run only one model (1x cost)
wpd-run-agent --agent self_review --file draft.md --mode external-llm --model gpt-5
```

**When single model is enough:**
- Non-critical documents
- Routine filings
- Early draft iterations
- Budget constraints

**When multiple models matter:**
- Critical motions before filing
- Dispositive pleadings
- High-stakes arguments
- Want adversarial consensus

### 3. Cache Citation Verification Results

WePublicDefender automatically caches verified citations in `06_RESEARCH/CITATIONS_LOG.md`.

**Before verifying citations:**
1. Check if case already verified recently
2. If yes and context unchanged → skip re-verification
3. Save 10-30 seconds per cached citation

**How caching works:**
- First verification: 10-30 seconds (web search)
- Subsequent uses: 0 seconds (read from cache)
- Cache includes: good law status, holding, quotes, pin cites

**Manual cache check:**
```bash
# Look for case in CITATIONS_LOG.md before running agent
grep -i "Smith v. Jones" 06_RESEARCH/CITATIONS_LOG.md
```

If found and recent, skip re-verification unless:
- Significant time passed (6+ months)
- Using citation for different proposition
- Concerned about recent developments

### 4. Batch Document Reviews

Instead of reviewing multiple documents separately, batch them:

```bash
# Slow: 3 separate agent calls
wpd-run-agent --agent self_review --file motion1.md --mode external-llm
wpd-run-agent --agent self_review --file motion2.md --mode external-llm
wpd-run-agent --agent self_review --file motion3.md --mode external-llm

# Faster: Combine into one document, review once
cat motion1.md motion2.md motion3.md > combined_review.md
wpd-run-agent --agent self_review --file combined_review.md --mode external-llm
```

**Cost savings:**
- Setup overhead: 1x instead of 3x
- Model loading: 1x instead of 3x
- Context sharing: Cross-document consistency checks

### 5. Optimize Pipeline Iterations

**The problem:** Pipeline re-validation can run 3-5 times before clean pass.

**Optimization:** Fix obvious issues BEFORE first pipeline run.

```
Bad approach:
1. Write draft blindly
2. Run pipeline → 15 issues found
3. Fix issues
4. Re-run pipeline → 5 issues found
5. Fix issues
6. Re-run pipeline → clean
Result: 3 full pipeline runs

Good approach:
1. Write draft carefully
2. Self-review in guidance mode → catch obvious issues
3. Fix them manually
4. Run pipeline → 2 issues found
5. Fix issues
6. Re-run pipeline → clean
Result: 2 full pipeline runs, saved one complete iteration
```

**Time saved:**
- 1 fewer pipeline run = 2-5 minutes saved
- Lower API costs
- Faster iterations

### 6. Use Targeted Reviews Instead of Full Pipeline

**Full pipeline:** Organization + Self-Review + Citations + Opposing + Final (5 phases)

**Targeted approach:** Only run phases you need.

```bash
# For early draft: Just self-review
wpd-run-agent --agent self_review --file draft_v1.md --mode guidance

# Before filing: Citations and final check
wpd-run-agent --agent citation_verify --file draft_v3.md --mode external-llm --web-search
wpd-run-agent --agent final_review --file draft_v3.md --mode guidance
```

**When to skip phases:**
- **Organization**: Skip if files already organized
- **Self-Review**: Skip if draft already reviewed multiple times
- **Citations**: Skip if no case law citations in document
- **Opposing**: Skip for routine/non-contentious filings
- **Final**: Never skip - always do final check

### 7. Pre-Process Large PDFs

**Problem:** Large PDFs take time to process directly.

**Solution:** Convert to images once, reference multiple times.

```bash
# Convert once (takes 30-60 seconds)
wpd-pdf-to-images "huge_credit_report.pdf"

# Reference many times (instant)
# Claude reads individual pages as needed
```

**Benefit:**
- One-time conversion cost
- Faster subsequent reads
- More granular control (read specific pages)

### 8. Leverage Claude Code 2.0.22+ Auto-Backgrounding

Long-running commands automatically background - no manual intervention needed.

**What this means:**
- Citation verification with web search: Runs in background automatically
- Multiple agents in parallel: All background automatically
- No timeout errors
- Check status with `/bashes` command

**Optimization:**
```bash
# Old way: Sequential, wait for each
wpd-run-agent --agent self_review --file draft.md --mode external-llm
# Wait...
wpd-run-agent --agent citation_verify --file draft.md --mode external-llm --web-search
# Wait...

# New way: Launch both, both auto-background, run in parallel
# Launch in separate terminal windows or use background flag
wpd-run-agent --agent self_review --file draft.md --mode external-llm &
wpd-run-agent --agent citation_verify --file draft.md --mode external-llm --web-search &
# Check both with /bashes command
```

**Time saved:** 50% when running 2 agents in parallel

### 9. Minimize Deep Research Scope

Deep Research on Claude.ai is thorough but time-intensive (5-10 minutes).

**Optimize by:**
- Use for initial case assessment only
- For follow-up questions, use quick `/research` in Claude Code
- Be specific in deep research prompts (narrow scope = faster)
- Reuse past deep research findings (check `06_RESEARCH/` first)

**Example:**
```bash
# Slow: New deep research session for related question
/deep-research-prep  # Generates prompt, go to Claude.ai, wait 10 min

# Fast: Quick targeted search in Claude Code
/research qualified immunity clearly established law Fourth Circuit
# Results in 30-60 seconds
```

### 10. Use Local LLM for Non-Critical Work (Advanced)

**Future optimization** (not yet implemented):

Configure local LLM (Llama 3 405B, Mistral, etc.) for:
- Guidance mode enhancements
- Initial drafting passes
- Non-legal document organization
- Cost-free iterations

**Trade-offs:**
- Zero API cost
- Slower inference (unless you have beefy GPU)
- Lower quality than GPT-5/Grok-4
- Good enough for draft iterations

## Performance Monitoring

### Check API Costs

```bash
# See detailed usage log
cat .wepublic_defender/usage_log.csv

# Get summary
wpd-usage-summary
```

**Look for:**
- High-cost operations you can replace with guidance mode
- Redundant agent calls
- Opportunities to cache results

### Measure Pipeline Time

Track how long full pipeline takes:

```bash
# Before optimization
time wpd-review-pipeline --file draft.md --mode external-llm
# Real: 8m 23s

# After optimization (guidance for self-review, single model for citations)
time wpd-review-pipeline --file draft.md --mode guidance --citations-only --model gpt-5
# Real: 2m 14s
```

**Savings: 6 minutes per pipeline run**

## Cost vs. Speed vs. Quality Trade-Offs

### High Speed, Low Cost, Good Quality
- Guidance mode for most tasks
- Single model for validation
- Targeted reviews only
- Manual fixes based on guidance

**Use for:** Routine filings, early drafts, non-critical documents

### Medium Speed, Medium Cost, High Quality
- Mix of guidance and external-llm modes
- Single model for most agents
- Full pipeline on final drafts
- Selective web search

**Use for:** Standard motions, discovery responses, most legal work

### Lower Speed, High Cost, Highest Quality
- External-llm mode for all agents
- Multiple models for consensus
- Full pipeline with multiple iterations
- Web search enabled
- Adversarial review

**Use for:** Dispositive motions, trial briefs, critical filings

## Real-World Optimization Example

### Before Optimization

```
Task: Review motion to dismiss before filing

1. Write draft (30 min)
2. Run full pipeline, all agents, external-llm, multiple models (8 min)
3. Fix 12 issues (20 min)
4. Re-run full pipeline (8 min)
5. Fix 4 issues (10 min)
6. Re-run full pipeline (8 min)

Total time: 84 minutes
Total cost: $18.50
```

### After Optimization

```
Task: Review motion to dismiss before filing

1. Write draft (30 min)
2. Self-review in guidance mode, fix obvious issues (5 min)
3. Run targeted pipeline: citations + opposing counsel, external-llm, single model (3 min)
4. Fix 3 issues (5 min)
5. Re-run targeted pipeline (3 min)
6. Final review in guidance mode (2 min)

Total time: 48 minutes
Total cost: $4.25

Savings: 36 minutes, $14.25
```

**Key changes:**
- Pre-caught obvious issues with guidance mode
- Targeted reviews instead of full pipeline
- Single model instead of multiple
- Guidance mode for final check

## Recommended Workflow by Document Type

### Routine Documents (Stipulations, Extensions, Notices)
- Guidance mode only
- Single quick review
- Cost: $0
- Time: 2-5 minutes

### Standard Filings (Discovery Responses, Routine Motions)
- Guidance mode for drafting and self-review
- External-llm with single model for citations only
- Cost: $1-3
- Time: 5-10 minutes

### Important Motions (Summary Judgment, Motions to Dismiss)
- Guidance mode for drafting
- Targeted external-llm reviews (self + citations + opposing)
- Single model, web search enabled
- Cost: $3-8
- Time: 10-20 minutes

### Critical Filings (Complaints, Trial Briefs, Appeals)
- Full pipeline, external-llm mode
- Multiple models for consensus
- Multiple iterations until clean pass
- Cost: $10-25
- Time: 20-45 minutes

## Summary: Quick Wins

1. Default to **guidance mode** - switch to external-llm only when needed
2. Use **single model** unless you need adversarial consensus
3. **Cache citations** - check CITATIONS_LOG.md before re-verifying
4. **Targeted reviews** - don't run full pipeline every time
5. **Pre-fix obvious issues** - reduces pipeline iterations
6. **Batch operations** - combine when possible
7. **Leverage auto-backgrounding** - run agents in parallel
8. **Monitor costs** - check usage_log.csv regularly

**Result:** 50-70% reduction in time and cost while maintaining quality.

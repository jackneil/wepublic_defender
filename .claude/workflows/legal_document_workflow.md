# Legal Document Workflow

**TRIGGER**: User is working on creating/reviewing legal documents for filing

**CRITICAL**: Follow `.claude/protocols/LEGAL_WORK_PROTOCOL.md` throughout this entire workflow.

This is the standard workflow for all legal document creation: research → draft → review → iterate → file.

## Standard Workflow Sequence

```
1. ORGANIZE → Ensure files are in proper directories
2. RESEARCH → Extensive research BEFORE drafting
3. DRAFT → Create initial document
4. REVIEW → Adversarial multi-AI review
5. POST-REVIEW ANALYSIS → **CRITICAL DECISION POINT**
6. REFINE → Implement decided changes
7. ITERATE → Repeat review until ready
8. FINALIZE → Move to appropriate directory, prepare for filing
```

## 1. Organize Phase

**Before starting any legal work:**

Check that files are organized:
- New documents in correct directories (not inbox)
- Related materials are together
- Evidence and exhibits properly filed

**If organization needed:**
- Run `/organize` on inbox files
- Clean up any scattered files
- Ensure directory structure is clean

## 2. Research Phase (MANDATORY - Never Skip)

**CRITICAL**: You MUST do extensive research BEFORE drafting. This is not optional.

### When to Use Deep Research vs Quick Research:

**Use `/deep-research-prep` (generates prompt for Claude.ai) when:**
- Starting a new case (need comprehensive viability/claims/damages assessment)
- Major filings requiring extensive case law research
- Complex legal standards that need thorough analysis
- Want to explore strategic approaches comprehensively
- Budget allows (Claude.ai deep research is very cost-effective)

**Use `/research [topic]` (quick Claude Code web search) when:**
- Need quick answer on specific narrow question
- Looking up procedural rule or deadline
- Verifying single case citation
- Following up on specific issue from previous research

### Research Quality Standards:

All research must identify:
- **Applicable law**: Statutes, regulations, case law
- **Legal standards**: What must be proven? What is the test?
- **Binding authority**: Cases from this jurisdiction/circuit
- **Persuasive authority**: Cases from other jurisdictions (if binding authority is sparse)
- **Contrary authority**: Cases that hurt our position (opponent will cite these)
- **Procedural requirements**: Filing deadlines, service rules, formatting requirements

**Save all research to `06_RESEARCH/`** with clear filenames:
- `summary_judgment_standards_SC.md`
- `breach_of_contract_elements_4th_circuit.md`
- `statute_of_limitations_fraud.md`

### When Research is Complete:

Update GAMEPLAN.md with:
- Legal issues identified
- Strength assessment
- Strategic approach based on research

## 3. Drafting Phase

### Before Drafting, Verify You Have:

- [ ] Completed research on legal standards
- [ ] Identified all required elements/factors
- [ ] Located supporting case law and statutes
- [ ] Reviewed opponent's arguments (if response/reply)
- [ ] Checked court rules for formatting/procedures
- [ ] Reviewed `.claude/protocols/LEGAL_WORK_PROTOCOL.md` for quality standards

### Choose Drafting Mode:

**Option A: Guidance Mode (default, free)**
```bash
<python_path> -m wepublic_defender.cli.run_agent --agent drafter --text "Draft [document type]" --mode guidance
```
- Returns comprehensive guidance prompt
- Claude Code does the drafting using the guidance
- $0.00 cost
- Recommended for most drafting

**Option B: External-LLM Mode (costs money)**
```bash
<python_path> -m wepublic_defender.cli.run_agent --agent drafter --text "Draft [document type]" --mode external-llm --file research_summary.md
```
- Calls external LLM(s) to draft
- Uses configured models from settings
- Costs API tokens
- Use when you want AI to draft autonomously

### Save Draft:

Save to `07_DRAFTS_AND_WORK_PRODUCT/drafts/` with clear filename:
- `MOTION_TO_DISMISS_v1.md`
- `RESPONSE_SUMMARY_JUDGMENT_v1.md`
- `COMPLAINT_v1.md`

**Use version numbers** (`_v1`, `_v2`, etc.) so you can track iterations.

## 4. Review Phase (MANDATORY - Never Skip)

**CRITICAL**: ALWAYS run adversarial review before filing. This is not optional.

### Targeted Review Approach (Recommended):

Run specific checks as needed. Claude orchestrates the workflow:

#### A. Self Review - Legal Sufficiency and Clarity

```bash
<python_path> -m wepublic_defender.cli.run_agent --agent self_review --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v1.md --mode guidance --verbose
```

**Checks:**
- All required elements addressed
- Legal standards correctly cited
- Arguments are clear and logical
- No procedural errors
- Tone is professional

**Results saved to:** `.wepublic_defender/reviews/self_review_[timestamp].json`

#### B. Citation Verification - Shepardize All Citations

```bash
<python_path> -m wepublic_defender.cli.run_agent --agent citation_verify --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v1.md --mode external-llm --web-search --verbose
```

**Checks:**
- All cases are good law (not overruled/reversed)
- Citations support the propositions cited for
- Quotes are accurate with pin cites
- Authority hierarchy is correct
- Better authority is not available

**Results saved to:** `.wepublic_defender/reviews/citation_verify_[timestamp].json`

**Updates:** `06_RESEARCH/CITATIONS_LOG.md` (so future reviews skip rechecking same cases)

#### C. Opposing Counsel Review - Adversarial Attack

```bash
<python_path> -m wepublic_defender.cli.run_agent --agent opposing_counsel --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v1.md --mode external-llm --web-search --verbose
```

**Checks:**
- Find weaknesses in arguments
- Identify contrary case law
- Challenge factual assertions
- Exploit procedural vulnerabilities
- Think like opponent's lawyer

**Results saved to:** `.wepublic_defender/reviews/opposing_counsel_[timestamp].json`

**This review is BRUTAL** - that's the point. Better to find problems now than after filing.

#### D. Fact Verification - Evidence Accuracy Check

```bash
<python_path> -m wepublic_defender.cli.run_agent --agent fact_verify --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v1.md --mode guidance --verbose
```

**Checks:**
- Every date against source documents
- All damage amounts against receipts/invoices
- Quotes accurate with context preserved
- Events match evidence timeline
- Claims supported by discovery
- Rule 11 compliance verified

**CRITICAL**: This phase checks EVERY factual assertion against actual evidence files in:
- `04_EVIDENCE/` - Primary evidence
- `03_DISCOVERY/` - Discovery responses
- `05_CORRESPONDENCE/` - Communications

**Results saved to:** `.wepublic_defender/reviews/fact_verify_[timestamp].json`

**Why this matters:** A single wrong date or unsupported fact can trigger Rule 11 sanctions. This phase catches discrepancies between what we claim and what evidence shows.

#### E. Final Review - Pre-Filing Compliance

```bash
<python_path> -m wepublic_defender.cli.run_agent --agent final_review --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_v1.md --mode guidance --verbose
```

**Checks:**
- Caption formatted correctly
- All required sections present
- Signature block complete
- Certificate of service included
- Page limits complied with
- Local rules followed
- No typos or formatting errors

**Results saved to:** `.wepublic_defender/reviews/final_review_[timestamp].json`

## 5. POST-REVIEW DECISION POINT ⚠️ **CRITICAL - DO NOT SKIP**

**This is the most important step in the entire workflow.**

### THE PROBLEM:

External LLMs will identify "concerns" and "weaknesses" in your draft. **DO NOT blindly accept or reject these concerns.**

LLMs can be:
- ✅ Correct - they spotted a real weakness
- ❌ Wrong - they misunderstood the law or facts
- ⚠️ Partially correct - they have a point, but wrong solution

### MANDATORY WORKFLOW AFTER RECEIVING LLM FEEDBACK:

#### Step 1: Read ALL Review Outputs

Read the JSON files in `.wepublic_defender/reviews/`:
- `self_review_[timestamp].json`
- `citation_verify_[timestamp].json`
- `opposing_counsel_[timestamp].json`
- `fact_verify_[timestamp].json`
- `final_review_[timestamp].json`

List every concern raised by the LLMs.

#### Step 2: Identify Concerns Requiring Research

For each LLM concern, ask:
- **Do we have research proving/disproving this concern?**
- **Do we need to research this issue further?**

Create research list:
```
LLM CONCERNS REQUIRING RESEARCH:
1. LLM says: "Motion may be time-barred under 28 U.S.C. § 1658"
   → Need to research: statute of limitations for this claim type

2. LLM says: "*Smith v. Jones* is distinguishable - different facts"
   → Need to research: Is Smith actually distinguishable? Find better case?

3. LLM says: "Missing element X in claim"
   → Need to research: Is element X actually required? Check elements.
```

#### Step 3: Conduct Research (If Needed)

For each research item:
- Do thorough web search
- Read statutes/cases carefully
- Save research to `06_RESEARCH/llm_concern_[topic].md`

**Research must answer:**
- Was the LLM correct about this concern?
- What does the law actually say?
- How do the cases actually hold?

#### Step 4: **STOP AND ANALYZE**

**After research is complete, STOP. Do not immediately start editing.**

**ALWAYS prompt user:**

> "Research complete. Before making changes to the draft, let's analyze the LLM feedback against our research findings to decide what changes to actually make.
>
> I've researched the concerns raised by the LLM reviews. Here's my analysis:"

#### Step 5: Compare LLM Feedback Against Research

For EACH LLM concern, document your analysis:

```markdown
## Analysis of LLM Feedback

### Concern 1: [LLM's concern]
**LLM said:** [quote the concern]

**Research findings:** [what you found]

**Assessment:**
- ✅ LLM was correct - research confirms the weakness
- ❌ LLM was wrong - research shows our approach is correct
- ⚠️ Partially correct - LLM had a point, but wrong fix

**Decision:**
- **Change to make:** [if LLM was right]
- **Keep as is because:** [if LLM was wrong]
- **Alternative approach:** [if middle ground]

**Reasoning:** [explain why, citing research]

---

### Concern 2: [LLM's concern]
[Repeat analysis format]
```

#### Step 6: Present Analysis to User

Show user your complete analysis:

> "Based on my research, here's what I found:
>
> **LLM Concerns That Were Valid:**
> 1. [Concern] - Research confirms this is a problem. We should [fix].
> 2. [Concern] - LLM was right. We need to [fix].
>
> **LLM Concerns That Were Invalid:**
> 1. [Concern] - Research shows this is incorrect because [reason]. Our original approach is sound.
> 2. [Concern] - LLM misunderstood [law/fact]. No change needed.
>
> **LLM Concerns Requiring Discussion:**
> 1. [Concern] - LLM has a point, but I found a better solution: [alternative]
>
> Should I proceed with making the valid changes?"

#### Step 7: Make Informed Decisions

Based on your analysis and user's input:

**Changes to implement:**
- LLM was right + research supports → Make the change
- Research suggests better solution → Implement better solution

**Keep original approach:**
- LLM was wrong + research contradicts → Keep as is
- LLM misunderstood context → Keep as is

**Alternative approaches:**
- Research suggests different fix than LLM suggested → Implement research-based fix

### Why This Step is CRITICAL:

**Bad approach (DON'T DO THIS):**
```
LLM says: "This argument is weak because [reason]"
You: "Okay, I'll change it."
```

**Good approach (DO THIS):**
```
LLM says: "This argument is weak because [reason]"
You: "Let me research that concern..."
[Research completed]
You: "Research shows the LLM was wrong - the argument is actually strong because [research findings]. Keeping original approach."
```

**Remember:**
- LLMs are tools, not oracles
- Research is ground truth
- Your judgment + research > LLM opinion
- User needs to understand WHY you're making (or not making) changes

### USER REMINDER:

Claude Code will NOT remember to do this step unless you prompt it. After LLM reviews complete, explicitly ask:

> "Let's analyze the LLM feedback against research before deciding what to change."

## 6. Refinement Phase

After post-review analysis, implement decided changes:

### If Changes Needed:

1. Create new version: `MOTION_v2.md`
2. Implement changes based on analysis (not blind LLM acceptance)
3. Document what changed and why
4. Save to drafts folder

### If No Changes Needed:

Document why:
```
Review complete - no changes needed.

LLM concerns analyzed:
- [Concern 1]: Research showed this is incorrect. Kept original approach.
- [Concern 2]: Valid concern but doesn't affect legal sufficiency. Noted for argument prep.

Draft is ready for final review.
```

## 7. Iteration Phase - Claude Orchestration

### Follow Agent Instructions for Pipeline Re-Validation

**CRITICAL**: After EVERY agent run, check the `claude_prompt` field for orchestration instructions.

#### The Golden Rule: If ANY Changes Made → Re-Run ENTIRE Pipeline

```python
# Pseudo-code for your orchestration logic:
total_changes = 0

# Track changes from each phase
if "must fix" in agent_prompt or "will need to replace" in agent_prompt:
    total_changes += extract_number_from_prompt()

# After ALL phases complete:
if total_changes > 0:
    print(f"⚠️ Pipeline made {total_changes} changes")
    print("MUST RESTART ENTIRE PIPELINE FROM PHASE 1")
    # GO BACK TO PHASE 1: Document Organization
else:
    print("✅ CLEAN PASS - No changes made")
    print("Document validated and ready for finalization")
```

#### What Agent Prompts Tell You:

**Prompts indicating changes made:**
- "Must fix X critical weaknesses. After fixing, you MUST re-run the ENTIRE pipeline"
- "Will need to replace X citations. After replacing, you MUST re-run the ENTIRE pipeline"
- "Found X issues. After fixing, you MUST re-run the ENTIRE pipeline"

**Prompts indicating clean pass:**
- "CLEAN PASS - NO CHANGES NEEDED"
- "All citations verified as good law"
- "No critical or major weaknesses"
→ BUT still check: "If ANY previous phases made changes, you MUST re-run entire pipeline"

#### Example Pipeline Orchestration:

```
=== PIPELINE RUN #1 ===
Phase 1: Self-Review → "Must fix 3 critical issues" → Changes: 3
Phase 2: Citations → "Replace 2 bad citations" → Changes: 2
Phase 3: Opposing → "Fix 1 critical weakness" → Changes: 1
Total Changes: 6 → RESTART FROM PHASE 1

=== PIPELINE RUN #2 ===
Phase 1: Self-Review → "Fix 1 major issue" → Changes: 1
Phase 2: Citations → "CLEAN PASS" → Changes: 0
Phase 3: Opposing → "CLEAN PASS" → Changes: 0
Total Changes: 1 → RESTART FROM PHASE 1

=== PIPELINE RUN #3 ===
Phase 1: Self-Review → "CLEAN PASS" → Changes: 0
Phase 2: Citations → "CLEAN PASS" → Changes: 0
Phase 3: Opposing → "CLEAN PASS" → Changes: 0
Total Changes: 0 → PROCEED TO FINALIZATION ✅
```

### Why Full Re-Validation Matters:

- **Cascade Effects**: Fixing jurisdiction might break standing arguments
- **Citation Dependencies**: New citations might not support revised arguments
- **Consistency**: Strengthening one argument might contradict another
- **Hidden Regressions**: Fixes often create new problems elsewhere

### Quality Gates (Only After Clean Pass):

**Document is ready for finalization only when:**
- Complete pipeline run with ZERO changes
- All agents report "CLEAN PASS"
- No fixes were applied in any phase
- Document follows LEGAL_WORK_PROTOCOL.md standards

## 8. Finalization Phase

### When Draft is Ready:

1. **Final version number**: Rename to `MOTION_FINAL.md`

2. **Convert to Word** (if required by court):
```bash
<python_path> -m wepublic_defender.cli.convert_to_word --file 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_FINAL.md --output 02_PLEADINGS/03_Motions/MOTION_TO_DISMISS_FINAL.docx
```

3. **Move to appropriate directory**:
- Motions → `02_PLEADINGS/03_Motions/`
- Responses → `02_PLEADINGS/05_Briefs/`
- Complaints → `02_PLEADINGS/01_Complaint/`

4. **Update GAMEPLAN.md**:
```markdown
## Status Update

[Date] - Completed draft of [document]
- Passed adversarial review (0 critical issues)
- All citations verified as good law
- Ready for filing
- Next step: [e.g., "File with court by deadline X"]
```

5. **Remind user**:

> "Document is ready for filing. **IMPORTANT REMINDER:**
>
> - Human lawyer must review and sign (AI assistance ≠ legal advice)
> - Verify court formatting requirements
> - Double-check filing deadline
> - Confirm service requirements
>
> Files ready:
> - Word version: 02_PLEADINGS/03_Motions/MOTION_TO_DISMISS_FINAL.docx
> - Markdown version: 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_FINAL.md
> - Review results: .wepublic_defender/reviews/"

## Common Workflow Mistakes to Avoid

**❌ DON'T:**
- Draft without research (recipe for sanctions)
- Accept LLM feedback blindly (LLMs can be wrong)
- Skip adversarial review (you'll regret it in court)
- File after only one review pass (iterate until clean)
- Forget to update GAMEPLAN.md (lose track of status)

**✅ DO:**
- Research extensively before drafting
- Analyze LLM feedback critically with research
- Run targeted reviews as needed (not always all 4)
- Iterate until quality gates are met
- Document decisions and reasoning
- Follow LEGAL_WORK_PROTOCOL.md throughout

## Emergency / Tight Deadline Workflow

If user has urgent deadline and can't do full workflow:

1. **Minimum viable review:**
   - Self review (guidance mode - free, quick)
   - Citation verify (external-llm with web search - catches bad law)
   - Final review (guidance mode - catches procedural errors)

2. **Skip opposing counsel if:**
   - No time for iteration
   - User accepts risk of weaker arguments

3. **Warning to user:**
   > "⚠️ Due to tight deadline, we're running abbreviated review. This increases risk of:
   > - Weaker arguments (no adversarial review)
   > - Missed strategic opportunities
   > - Higher chance of needing to amend
   >
   > For critical filings, recommend requesting extension to do full review."

## Integration with Other Workflows

This workflow integrates with:
- **Session start**: User says "I need to draft motion" → this workflow
- **Deep research**: Complete research first → then this workflow for drafting
- **Strategy**: Run strategy to decide what to file → then this workflow to create it
- **Organization**: Organize evidence first → reference in draft created via this workflow

## Remember

This is federal court litigation. Every mistake you miss becomes part of the permanent record. The workflow exists to catch mistakes before they become problems.

**The two most critical steps:**
1. Research extensively BEFORE drafting
2. Analyze LLM feedback critically AFTER reviewing

Skip either step and you risk sanctions, dismissal, or losing a winnable case.

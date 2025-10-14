# Citation Verification Guidance for Claude Code

## CRITICAL REQUIREMENTS (from LEGAL_WORK_PROTOCOL.md)

**Rule 3: Citations Must Be Perfect**
- Every case cited must be verified as good law (not overruled)
- Every statute must be current version
- Every rule citation must be accurate
- Pin cites to specific pages when quoting

**Post-Writing Verification:**
- Shepardize all cases (verify they're still good law)
- Double-check all statutory citations
- Verify all quotes are accurate
- Confirm procedural requirements met

**Prohibited Actions:**
- NEVER cite a case without reading it
- NEVER make up legal authority
- NEVER misrepresent what a case holds
- NEVER cite overruled cases

## Your Task

Verify all citations in the following document:

**Document Type:** {document_type}
**Case Context:**
- Jurisdiction: {jurisdiction}
- Court: {court}

**Document to Verify:**
```
{document_content}
```

## CITATION VERIFICATION PROCESS

### STEP 1: EXTRACT ALL CITATIONS

Go through the document and list every citation:

**Cases:**
1. Citation string: [Full citation]
2. Citation string: [Full citation]
[Continue for all cases]

**Statutes:**
1. Citation string: [Full citation]
2. Citation string: [Full citation]
[Continue for all statutes]

**Rules:**
1. Citation string: [Full citation]
2. Citation string: [Full citation]
[Continue for all rules]

### STEP 2: VERIFY EACH CASE CITATION

For EACH case, complete this analysis:

#### Case: {Case Name}, {Citation}

**1. Citation Format Verification**
- [ ] Proper Bluebook format
- [ ] Case name italicized
- [ ] Volume, reporter, page included
- [ ] Court and year in parentheses
- [ ] Pin cite included for quotes

**Correct Format:** *Case Name*, Vol. Reporter Page, Pinpoint (Court Year)
**Example:** *Smith v. Jones*, 450 F.3d 123, 125 (4th Cir. 2020)

**2. Good Law Verification (Shepardize)**

Use web search to verify:
- [ ] Case still exists and is correctly cited
- [ ] Case has not been overruled
- [ ] Case has not been superseded by statute
- [ ] Case is not on negative treatment
- [ ] Holding is accurately represented

**Search Terms to Use:**
- "{case name} overruled"
- "{case name} shepardize"
- "{case name} good law"
- "{citation} subsequent history"

**Status Check:**
- Good law: [Yes/No/Uncertain]
- Subsequent history: [None/Limited/Overruled/Questioned]
- Last verified: [Date]

**3. Authority Level**
- What court decided this case?
- Is it controlling or persuasive authority?
- Tier 1 (Controlling): Supreme Court, Circuit, State Supreme
- Tier 2 (Persuasive): Other circuits, district courts
- Tier 3 (Weak): Out-of-state, old cases

**4. Holding Verification**
- What does the case actually hold?
- Are we representing it accurately?
- Are we quoting it correctly?
- Does it support our proposition?

**5. Quote Accuracy (If Quoted)**

If we quote this case:
- [ ] Quote matches source word-for-word
- [ ] Pin cite is accurate
- [ ] Quote is not taken out of context
- [ ] Ellipses/brackets used correctly if edited
- [ ] Quote is properly attributed

**6. Application Analysis**
- How are we using this case?
- Does the holding support how we're using it?
- Are there distinguishing factors?
- Is there contrary authority we should address?

### STEP 3: VERIFY EACH STATUTE CITATION

For EACH statute, complete this analysis:

#### Statute: {Code} § {Section}

**1. Citation Format Verification**
- [ ] Proper code abbreviation
- [ ] Section symbol (§) used correctly
- [ ] Year included (if required)
- [ ] Subsection properly cited

**Correct Format:** Code § Section (Year)
**Example:** 42 U.S.C. § 1983 (2020)

**2. Current Version Verification**

Use web search to verify:
- [ ] This is the current version
- [ ] No recent amendments
- [ ] Section number is correct
- [ ] Text matches current law

**Search Terms:**
- "{statute} current version"
- "{code section} amended"
- "{statute name} {year}"

**3. Full Text Review**
- Read the entire section
- Note any subsections
- Check cross-references
- Verify our interpretation

**4. Related Sections**
- Are there related sections we should cite?
- Are there definitions sections?
- Are there exceptions or limitations?

**5. Accuracy of Representation**
- Are we quoting/paraphrasing correctly?
- Are we capturing the full requirement?
- Are we missing relevant parts?

### STEP 4: VERIFY EACH RULE CITATION

For EACH rule, complete this analysis:

#### Rule: {Rule Type} {Number}

**1. Citation Format Verification**
- [ ] Proper rule abbreviation (Fed. R. Civ. P., etc.)
- [ ] Rule number correct
- [ ] Subsection properly cited

**Correct Formats:**
- Fed. R. Civ. P. 12(b)(6)
- Fed. R. Evid. 401
- Local Rule 7.1

**2. Current Rule Verification**
- [ ] This is the current version
- [ ] No recent amendments
- [ ] Correct for this jurisdiction

**3. Local Rules Check**
- Are there local rules that modify this?
- Does this court have special requirements?
- Have we cited local rules where needed?

**4. Application Accuracy**
- Are we applying the rule correctly?
- Have we cited the right subsection?
- Are there related rules?

### STEP 5: CROSS-CHECK AGAINST DOCUMENT

**Proposition-Citation Matching:**

For each legal proposition in the document:
- [ ] Does it have a citation?
- [ ] Does the citation actually support it?
- [ ] Is the authority controlling or persuasive?
- [ ] Is a stronger authority available?

**Citation Signals:**

Check that citation signals are used correctly:
- [No signal]: Direct support for the proposition
- *See*: Implicit support, requires inference
- *See also*: Additional support
- *Cf.*: Comparison with different facts
- *But see*: Contrary authority
- *See generally*: Background material

**Id. Usage:**

Check *Id.* citations:
- [ ] Used only when immediately preceding cite is same source
- [ ] Includes new pin cite if different page
- [ ] Not used across different footnotes/paragraphs

### STEP 6: AUTHORITY HIERARCHY CHECK

**Verify We're Using Best Authority:**

For each proposition, check:
- [ ] Are we citing controlling authority when available?
- [ ] Is there newer authority?
- [ ] Is there Supreme Court authority?
- [ ] Is there {jurisdiction} or {circuit} authority?
- [ ] Are we using persuasive authority when we should cite controlling?

**Authority Priority (Use This Order):**
1. U.S. Supreme Court (if applicable)
2. {circuit} Court of Appeals (for federal issues)
3. {jurisdiction} Supreme Court (for state issues)
4. {court} (district court precedent)
5. Other circuits (persuasive only)
6. Other states (persuasive only)

## CITATION VERIFICATION OUTPUT FORMAT

```markdown
# Citation Verification Report

## Overall Assessment

**Total Citations:** {number}
- Cases: {number}
- Statutes: {number}
- Rules: {number}

**Verification Status:**
- Verified good law: {number}
- Issues found: {number}
- Critical problems: {number}

---

## CRITICAL CITATION ISSUES (Must Fix)

### Issue 1: Overruled Case Cited
- **Citation**: [Full citation]
- **Location**: [Paragraph/page in document]
- **Problem**: Case was overruled by [Case, Year]
- **Impact**: This invalidates our argument
- **Recommendation**: Find replacement authority or remove argument

[Continue for each critical issue]

---

## MAJOR CITATION ISSUES (Should Fix)

### Issue 1: Weak Authority Used
- **Citation**: [Full citation]
- **Location**: [Paragraph/page]
- **Problem**: Only persuasive authority, controlling authority available
- **Recommendation**: Replace with [Suggested case]

[Continue for each major issue]

---

## MINOR CITATION ISSUES (Format/Polish)

- Citation formatting error at [location]: [Description]
- Missing pin cite at [location]: [Citation]
- Incorrect use of *Id.* at [location]

[Continue for minor issues]

---

## DETAILED CITATION ANALYSIS

### Cases

#### 1. *Case Name*, Citation

**Good Law Status:** ✓ Verified
**Authority Level:** Tier 1 - Controlling ({circuit} Court of Appeals)
**Holding:** [Brief description]
**Our Use:** [How we use it]
**Accuracy:** ✓ Correctly represents holding
**Quote Accuracy:** ✓ Verified (if applicable)
**Recommendation:** Keep as cited

[Continue for each case]

### Statutes

#### 1. Code § Section

**Current Status:** ✓ Current version verified
**Our Use:** [How we apply it]
**Accuracy:** ✓ Correctly interprets statute
**Related Sections:** [List if any]
**Recommendation:** Keep as cited

[Continue for each statute]

### Rules

#### 1. Rule Citation

**Current Status:** ✓ Current version verified
**Local Rules:** [Any applicable local rules]
**Accuracy:** ✓ Correctly applies rule
**Recommendation:** Keep as cited

[Continue for each rule]

---

## MISSING CITATIONS

**Propositions Without Citations:**
1. [Location]: "[Quote of proposition]"
   - Needs citation for: [What needs support]
   - Suggested authority: [If known]

[Continue for each missing citation]

---

## AUTHORITY UPGRADE OPPORTUNITIES

**Cases Where Better Authority Available:**
1. Current: [Current citation]
   - Better option: [Suggested citation]
   - Why better: [Controlling vs. persuasive, newer, etc.]

[Continue for upgrade opportunities]

---

## SHEPARDIZING SUMMARY

| Citation | Good Law | Status | Notes |
|----------|----------|--------|-------|
| [Case 1] | Yes | Current | No issues |
| [Case 2] | No | Overruled | Replace |
| [Case 3] | Uncertain | Questioned | Verify further |

---

## RECOMMENDATIONS

### Priority 1 (Critical - Must Fix Before Filing)
1. Replace overruled case at [location] with [alternative]
2. Add missing citation at [location] for [proposition]

### Priority 2 (Should Fix for Stronger Brief)
1. Upgrade to controlling authority at [location]
2. Add pin cite at [location]

### Priority 3 (Polish)
1. Fix formatting errors: [List]
2. Correct citation signals: [List]

---

## FINAL VERIFICATION CHECKLIST

- [ ] All cases shepardized and verified as good law
- [ ] All statutes confirmed as current version
- [ ] All rules verified as current
- [ ] All quotes verified word-for-word
- [ ] All pin cites confirmed accurate
- [ ] All citation formats corrected
- [ ] All propositions have supporting citations
- [ ] Best available authority used
- [ ] Contrary authority addressed

---

## OVERALL RECOMMENDATION

**Citation Quality:** [Excellent / Good / Needs Work / Serious Issues]

**Filing Readiness (Citations Only):** [Ready / Minor fixes needed / Major revision needed]

**Key Actions Before Filing:**
1. [Most important fix]
2. [Second most important]
3. [Third most important]
```

## RED FLAGS - ESCALATE IMMEDIATELY

**Stop and alert user if:**
1. "Multiple cases are overruled or superseded"
2. "Key argument relies on case that's no longer good law"
3. "We're citing only persuasive authority when controlling exists"
4. "Multiple legal propositions lack citations"
5. "Quotes don't match source text"
6. "We're misrepresenting what cases hold"

## CITATION VERIFICATION CHECKLIST

Before submitting verification:

- [ ] I checked every single citation
- [ ] I shepardized all cases
- [ ] I verified all statutes are current
- [ ] I checked all quotes word-for-word
- [ ] I verified all pin cites
- [ ] I identified authority hierarchy issues
- [ ] I found all missing citations
- [ ] I provided specific, actionable recommendations

## REMEMBER

- **Every citation must be verified** - No exceptions
- **Good law status is critical** - Citing overruled cases is sanctions-worthy
- **Quotes must be exact** - Word-for-word accuracy required
- **Pin cites are mandatory** - For every quote
- **Best authority wins** - Always cite controlling when available

This is federal court. Citation errors can get you sanctioned.

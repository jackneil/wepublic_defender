# FACT VERIFICATION - Evidence-Based Review

You are performing FACT VERIFICATION to ensure every assertion in the document is supported by actual evidence files.

## YOUR MISSION

Check EVERY factual claim against the actual evidence in the case folder to prevent Rule 11 sanctions.

## DOCUMENT TO VERIFY

```
{document_content}
```

## VERIFICATION PROTOCOL

### Phase 1: Extract All Factual Assertions

Go through the document systematically and identify:
- **Dates**: Every specific date mentioned
- **Amounts**: All dollar amounts, percentages, quantities
- **Quotes**: Direct quotes attributed to documents
- **Events**: Specific events described as occurring
- **Claims about defendant**: Actions, knowledge, intent
- **Damages**: All damage claims and calculations
- **Communications**: References to emails, letters, calls
- **Timeline**: Sequence of events and chronology

### Phase 2: Evidence Mapping

For each factual assertion, determine:
1. Which evidence document should contain this fact
2. The likely location in case folders:
   - `04_EVIDENCE/` - Primary evidence documents
   - `03_DISCOVERY/` - Discovery responses and productions
   - `05_CORRESPONDENCE/` - Letters and communications
   - `00_NEW_DOCUMENTS_INBOX/` - Recent additions

### Phase 3: Systematic Verification

For each fact, verify:

**Dates**:
- [ ] Exact match in source document
- [ ] No transposition errors (month/day swap)
- [ ] Correct year
- [ ] Business days vs calendar days

**Amounts**:
- [ ] Exact dollar amount matches
- [ ] Currency specified correctly
- [ ] Decimal points correct
- [ ] Percentages calculated accurately

**Quotes**:
- [ ] Exact wording preserved
- [ ] Context not misleading
- [ ] Attribution correct
- [ ] Ellipses used properly

**Events**:
- [ ] Sequence correct
- [ ] All parties identified accurately
- [ ] Location accurate
- [ ] Duration/timing correct

### Phase 4: Categorize Discrepancies

**CRITICAL (Unsupported Facts - Rule 11 Risk)**:
- Facts with zero documentary support
- Claims that contradict evidence
- Fabricated or assumed information
- Misrepresented documents

**MAJOR (Wrong Information)**:
- Wrong dates (affects timeline/limitations)
- Wrong amounts (affects damages)
- Misquoted documents
- Incorrect party identification

**MINOR (Small Errors)**:
- Typos that don't affect meaning
- Formatting inconsistencies
- Rounding differences
- Style variations

## EVIDENCE REVIEW INSTRUCTIONS

1. **Check Primary Sources First**:
   - Original contracts, agreements
   - Bank statements, invoices
   - Official correspondence
   - Court filings

2. **Cross-Reference Multiple Sources**:
   - If fact appears in multiple places, verify consistency
   - Note any contradictions between sources
   - Identify most authoritative source

3. **Flag Missing Evidence**:
   - Facts that should have documentation but don't
   - Claims needing additional support
   - Damages lacking proof
   - Timeline gaps

## CRITICAL OUTPUT STRUCTURE

Your response MUST identify:

### Critical Issues (MUST FIX - Rule 11 Risk)
List each unsupported factual assertion that could trigger sanctions:
- State the assertion
- Note what evidence was searched
- Explain why it's unsupported
- Risk level if filed as-is

### Major Issues (SHOULD FIX - Credibility Risk)
List significant factual errors:
- Wrong dates affecting case
- Incorrect amounts
- Misquoted documents
- Party identification errors

### Minor Issues (Optional Fixes)
Small discrepancies that don't affect claims:
- Typos
- Formatting
- Rounding
- Style issues

### Evidence Gaps Requiring Action
Facts needing more documentation:
- What's missing
- Where to look
- Whether claim viable without it

## JURISDICTION CONTEXT
{jurisdiction}
{court}
{circuit}

Focus on evidence standards and requirements for this jurisdiction.

## YOUR ANALYSIS

Perform systematic fact verification following the protocol above. Be meticulous - the attorney's credibility and ability to avoid Rule 11 sanctions depends on your accuracy.

**Remember**:
- Every fact must trace to a document
- "Information and belief" must be clearly marked
- Assumptions are dangerous
- When in doubt, flag for review

After your analysis, explicitly state:
1. Total factual assertions checked
2. Number fully verified
3. Number partially supported
4. Number unsupported
5. Whether document is safe to file or needs corrections
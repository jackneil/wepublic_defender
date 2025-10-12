# /draft Command

Draft a legal document using AI assistance.

## Usage
```
/draft [document_type]
/draft Motion for Summary Judgment
/draft Discovery Request
/draft Response to Motion to Dismiss
```

## Process

1. **Gather Context**
   - Understand document type and purpose
   - Collect relevant facts from case files
   - Review applicable legal research
   - Check LEGAL_WORK_PROTOCOL.md standards

2. **Call DrafterAgent**
   - Use GPT-5 (no web search for initial draft)
   - Provide all context and requirements
   - Generate first draft

3. **Save Draft**
   - Save to 07_DRAFTS_AND_WORK_PRODUCT/drafts/
   - Use proper naming: `DOCUMENT_TYPE_DRAFT_v1.md`

4. **Suggest Next Steps**
   - Recommend running `/review` on the draft
   - Identify additional research needed
   - Note citations that need verification

## Example Output

```
Drafting: Motion for Summary Judgment on Count 1 (Breach of Contract)

Gathering context from case files...
✓ Loaded complaint from 02_PLEADINGS/01_Complaint/
✓ Loaded answer from 02_PLEADINGS/02_Answer/
✓ Loaded discovery responses from 03_DISCOVERY/04_Their_Responses/
✓ Loaded research on material breach from 06_RESEARCH/

Generating draft with GPT-5...

DRAFT COMPLETE (2,847 words)

SAVED TO: 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_FOR_SUMMARY_JUDGMENT_COUNT1_v1.md

NEXT STEPS:
1. Review draft for legal sufficiency
2. Verify all case citations (15 cases cited)
3. Run /review to check for issues before finalizing
4. Add exhibits and evidence references

CITATIONS TO VERIFY:
- Twombly v. Bell Atlantic, 550 U.S. 544 (2007)
- Jones v. Bank of America, 450 S.E.2d 123 (S.C. 2020)
- [... 13 more cases ...]

Cost: $0.45 (draft generation)

Run `/review 07_DRAFTS_AND_WORK_PRODUCT/drafts/MOTION_FOR_SUMMARY_JUDGMENT_COUNT1_v1.md` to review.
```

## Implementation

```python
from wepublic_defender import WePublicDefender

# Initialize with package config
defender = WePublicDefender()

draft = await defender.call_agent(
    "drafter",
    document="",
    document_type=document_type,
    case_details=load_case_details(),
    relevant_facts=load_relevant_facts(),
    research_summary=load_research()
)

# Save draft
filename = f"07_DRAFTS_AND_WORK_PRODUCT/drafts/{document_type}_v1.md"
with open(filename, 'w') as f:
    f.write(draft['content'])

print(f"SAVED TO: {filename}")
print(f"Cost: ${draft['cost']:.2f}")
```

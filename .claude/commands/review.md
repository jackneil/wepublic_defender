# /review Command

Run wepublic_defender adversarial review on a legal document.

## Usage
```
/review [file_path]
/review 07_DRAFTS_AND_WORK_PRODUCT/MOTION_TO_DISMISS.docx
```

## Process

1. **Load Document**
   - Verify file exists
   - Load content

2. **Initialize wepublic_defender**
   - Load settings from package config
   - Initialize API clients (OpenAI + xAI)
   - Set up token tracking

3. **Run Review Workflow**
   - Execute review loop (max 3 iterations)
   - Run parallel reviews (Self + Citation)
   - Run opposing counsel attack
   - Check consensus
   - Refine if needed

4. **Report Results**
   - Show issues found per iteration
   - Display final assessment
   - Show cost breakdown
   - Indicate if ready to file

## Example Output

```
Running adversarial review on MOTION_TO_DISMISS.docx...

=== ITERATION 1 ===
✓ Self Review (GPT-5): Found 5 issues
✓ Citation Verification (Grok 4 Fast): Found 2 citation errors
✓ Opposing Counsel Attack (Grok 4): Found 3 weaknesses

Total: 10 issues (2 CRITICAL, 5 MAJOR, 3 MINOR)
Status: NEEDS REVISION

Refining document...

=== ITERATION 2 ===
✓ Self Review: Found 1 issue
✓ Citation Verification: All citations verified
✓ Opposing Counsel Attack: Found 1 weakness

Total: 2 issues (0 CRITICAL, 1 MAJOR, 1 MINOR)
Status: NEEDS REVISION

Refining document...

=== ITERATION 3 ===
✓ Self Review: PASS
✓ Citation Verification: PASS
✓ Final Review: READY TO FILE

---
FINAL ASSESSMENT: ✓ READY TO FILE
Total Cost: $3.42
Iterations: 3
```

## Implementation

```python
from wepublic_defender import WePublicDefender

# Initialize with package config files
defender = WePublicDefender()

# Run adversarial review workflow
result = await defender.review_document(
    document_path=file_path,
    document_type="Motion to Dismiss",
    max_iterations=3
)

# Report results
print(f"Ready to file: {result['ready_to_file']}")
print(f"Total cost: ${result['total_cost']:.2f}")
print(defender.get_cost_report())
print(defender.get_detailed_cost_report())
```

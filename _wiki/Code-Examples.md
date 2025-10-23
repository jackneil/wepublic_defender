# Code Examples

This page provides practical code examples for common tasks in WePublicDefender. Each example includes context, code, and expected output.

## Basic Operations

### Initialize a New Case

```bash
# Navigate to your case folder
cd ~/Desktop/SmithVsJones

# Initialize the case structure
wpd-init-case

# Output:
# Creating case structure...
# ✓ Created 8 standard directories
# ✓ Initialized configuration files
# ✓ Installed Claude commands
# Case ready for use!
```

### Check Environment

```bash
wpd-check-env --verbose

# Output:
# Environment Check Results:
# ✓ Python: 3.11.5 (/Users/you/.conda/envs/wepublic_defender/bin/python)
# ✓ WePublicDefender: 1.0.0 installed
# ✓ OpenAI API Key: Configured (sk-proj-...NcT3)
# ✓ xAI API Key: Configured (xai-...abc)
# ⚠ CourtListener: Not configured (optional)
# ✓ Case initialized at: /Users/you/Desktop/SmithVsJones
#
# Status: READY (1 warning)
```

## Document Review Examples

### Guidance Mode Review (Free)

```python
# Python script example
from wepublic_defender.cli import run_agent

result = run_agent(
    agent="self_review",
    file="07_DRAFTS_AND_WORK_PRODUCT/motion_to_dismiss.md",
    mode="guidance"
)

print(result["claude_prompt"])
```

**Output**:
```
Review Checklist for motion_to_dismiss.md:

CRITICAL ITEMS TO CHECK:
□ Jurisdiction statement in first paragraph
□ All parties properly identified
□ Legal standard cited with supporting cases
□ Each element of claim addressed

PROCEDURAL REQUIREMENTS:
□ Certificate of service included
□ Local rule compliance statement
□ Page limits observed
□ Proposed order attached

[Continues with detailed checklist...]
```

### External-LLM Review

```bash
wpd-run-agent \
  --agent self_review \
  --file motion.md \
  --mode external-llm \
  --model gpt-4o \
  --verbose
```

**Output**:
```json
{
  "agent": "self_review",
  "timestamp": "2025-10-15T10:30:00Z",
  "structured": {
    "critical_issues": [
      {
        "location": "¶1",
        "issue": "Missing subject matter jurisdiction statement",
        "severity": "critical",
        "fix": "Add: 'This Court has jurisdiction under 28 U.S.C. § 1331'"
      }
    ],
    "major_issues": [...],
    "minor_issues": [...]
  },
  "cost": 2.34,
  "tokens": {"input": 4500, "output": 1200}
}
```

## Document Organization

### Organize Inbox Documents

```python
import os
from pathlib import Path

# List inbox contents
inbox_path = Path("00_NEW_DOCUMENTS_INBOX")
files = list(inbox_path.glob("*"))

print(f"Found {len(files)} files to organize:")
for f in files:
    print(f"  - {f.name}")

# Run organization
os.system("wpd-run-agent --agent organize --mode guidance")
```

**Output**:
```
Found 5 files to organize:
  - complaint.pdf
  - answer.pdf
  - motion_to_compel.docx
  - email_correspondence.msg
  - contract_exhibit_a.pdf

Organizing documents...
✓ complaint.pdf → 02_PLEADINGS/01_Complaint/
✓ answer.pdf → 02_PLEADINGS/02_Answers/
✓ motion_to_compel.docx → 02_PLEADINGS/03_Motions/
✓ email_correspondence.msg → 05_CORRESPONDENCE/
✓ contract_exhibit_a.pdf → 04_EVIDENCE/contracts/

Organization complete. Check .database/file_management_log.md
```

## Research Examples

### Quick Legal Research

```python
from wepublic_defender.research import quick_research

result = quick_research(
    topic="qualified immunity",
    jurisdiction="4th Circuit",
    max_results=5
)

for case in result["cases"]:
    print(f"{case['name']} ({case['year']})")
    print(f"  Key holding: {case['holding']}")
    print()
```

**Output**:
```
Pearson v. Callahan (2009)
  Key holding: Courts may address either prong of qualified immunity first

Smith v. Ray (4th Cir. 2021)
  Key holding: Right must be clearly established at time of violation

Johnson v. Barnes (4th Cir. 2020)
  Key holding: Specificity required for clearly established right
```

### Generate Deep Research Prompt

```python
from wepublic_defender.cli import deep_research_prompt

prompt = deep_research_prompt.generate(
    case_type="employment_discrimination",
    claims=["retaliation", "wrongful_termination"],
    jurisdiction="D. South Carolina",
    defendant="Large Corporation"
)

# Save for Claude.ai
with open("deep_research_prompt.txt", "w") as f:
    f.write(prompt)

print("Research prompt generated. Length:", len(prompt))
```

## Citation Management

### Verify Citations in Document

```python
from wepublic_defender.citations import CitationVerifier

verifier = CitationVerifier(
    use_courtlistener=True,
    check_quotes=True
)

# Verify all citations
results = verifier.verify_file("brief.md")

# Process results
for citation in results["citations"]:
    if citation["status"] == "invalid":
        print(f"❌ {citation['text']}")
        print(f"   Problem: {citation['issue']}")
    elif citation["status"] == "warning":
        print(f"⚠️ {citation['text']}")
        print(f"   Warning: {citation['warning']}")
    else:
        print(f"✓ {citation['text']}")
```

**Output**:
```
❌ Smith v. Jones, 123 F.3d 456 (4th Cir. 2019)
   Problem: Case overruled by Johnson v. State (2023)
⚠️ Anderson v. City, 789 F.2d 123 (9th Cir. 2018)
   Warning: 9th Circuit case not binding in 4th Circuit
✓ Pearson v. Callahan, 555 U.S. 223 (2009)
```

## Workflow Automation

### Daily Morning Routine

```python
#!/usr/bin/env python3
# daily_routine.py

import subprocess
from datetime import datetime

def run_morning_routine():
    print(f"Running morning routine - {datetime.now()}")

    # 1. Check environment
    subprocess.run(["wpd-check-env"])

    # 2. Organize inbox
    result = subprocess.run(
        ["wpd-run-agent", "--agent", "organize", "--mode", "guidance"],
        capture_output=True,
        text=True
    )

    files_organized = result.stdout.count("✓")
    print(f"Organized {files_organized} files")

    # 3. Check deadlines
    with open(".wepublic_defender/case_timeline.md") as f:
        content = f.read()
        # Parse for upcoming deadlines

    print("Morning routine complete!")

if __name__ == "__main__":
    run_morning_routine()
```

### Pre-Filing Review Pipeline

```python
def pre_filing_review(document_path):
    """Complete pre-filing review pipeline"""

    print(f"Starting pre-filing review for {document_path}")

    # Phase 1: Self-review
    print("Phase 1: Self-review...")
    result = run_agent("self_review", document_path, "external-llm")

    if result["critical_issues"]:
        print(f"Found {len(result['critical_issues'])} critical issues")
        # Fix critical issues
        fix_issues(document_path, result["critical_issues"])

    # Phase 2: Citation verification
    print("Phase 2: Citation verification...")
    result = run_agent("citation_verify", document_path, "external-llm")

    # Phase 3: Opposing counsel simulation
    print("Phase 3: Opposing counsel simulation...")
    result = run_agent("opposing_counsel", document_path, "external-llm")

    # Generate final report
    return generate_review_report(all_results)
```

## Custom Agent Examples

### Create Custom Review Agent

```python
from wepublic_defender.agents import BaseAgent

class LocalRulesAgent(BaseAgent):
    """Check compliance with local court rules"""

    def __init__(self, court="D.S.C."):
        super().__init__()
        self.court = court
        self.load_local_rules()

    def load_local_rules(self):
        """Load local rules for the court"""
        self.rules = {
            "page_limit": 15,
            "font_size": 12,
            "margins": 1.0,
            "certificate_required": True
        }

    def check_document(self, doc_path):
        """Check document against local rules"""
        violations = []

        # Check page count
        page_count = self.get_page_count(doc_path)
        if page_count > self.rules["page_limit"]:
            violations.append(f"Exceeds {self.rules['page_limit']} page limit")

        # Check for certificate
        if not self.has_certificate(doc_path):
            violations.append("Missing certificate of service")

        return violations
```

## Batch Processing

### Review Multiple Documents

```python
import asyncio
from pathlib import Path

async def review_document_async(doc_path):
    """Async document review"""
    proc = await asyncio.create_subprocess_exec(
        "wpd-run-agent",
        "--agent", "self_review",
        "--file", str(doc_path),
        "--mode", "guidance",
        stdout=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()

async def batch_review():
    """Review all documents in drafts folder"""
    drafts_folder = Path("07_DRAFTS_AND_WORK_PRODUCT")
    documents = list(drafts_folder.glob("*.md"))

    print(f"Reviewing {len(documents)} documents...")

    tasks = [review_document_async(doc) for doc in documents]
    results = await asyncio.gather(*tasks)

    for doc, result in zip(documents, results):
        print(f"\n{doc.name}:")
        print(result[:200] + "...")

# Run batch review
asyncio.run(batch_review())
```

## Cost Tracking

### Track Operation Costs

```python
import csv
from datetime import datetime, timedelta

def analyze_costs(days=7):
    """Analyze API costs for past N days"""

    costs_by_day = {}
    costs_by_operation = {}

    with open(".wepublic_defender/usage_log.csv") as f:
        reader = csv.DictReader(f)
        cutoff = datetime.now() - timedelta(days=days)

        for row in reader:
            timestamp = datetime.fromisoformat(row["timestamp"])
            if timestamp < cutoff:
                continue

            date = timestamp.date()
            operation = row["operation"]
            cost = float(row["cost"])

            costs_by_day[date] = costs_by_day.get(date, 0) + cost
            costs_by_operation[operation] = costs_by_operation.get(operation, 0) + cost

    print(f"Cost Analysis (Last {days} days)")
    print("=" * 40)

    print("\nDaily Costs:")
    for date, cost in sorted(costs_by_day.items()):
        print(f"  {date}: ${cost:.2f}")

    print(f"\nTotal: ${sum(costs_by_day.values()):.2f}")

    print("\nBy Operation:")
    for op, cost in sorted(costs_by_operation.items(), key=lambda x: x[1], reverse=True):
        print(f"  {op}: ${cost:.2f}")

# Run analysis
analyze_costs(7)
```

**Output**:
```
Cost Analysis (Last 7 days)
========================================

Daily Costs:
  2025-10-09: $3.45
  2025-10-10: $8.23
  2025-10-11: $2.10
  2025-10-12: $15.67
  2025-10-13: $4.89
  2025-10-14: $7.33
  2025-10-15: $5.21

Total: $46.88

By Operation:
  review: $28.45
  citation_verify: $12.33
  research: $6.10
```

## Error Handling

### Robust API Call with Retry

```python
import time
from typing import Optional

def call_api_with_retry(
    agent: str,
    file_path: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Optional[dict]:
    """Call API with exponential backoff retry"""

    for attempt in range(max_retries):
        try:
            result = run_agent(agent, file_path, "external-llm")
            return result

        except RateLimitError as e:
            if attempt == max_retries - 1:
                print(f"Max retries reached. Failed: {e}")
                return None

            wait_time = backoff_factor ** attempt
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)

        except APIError as e:
            print(f"API Error: {e}")
            return None

    return None
```

## Integration Examples

### Slack Notification Integration

```python
import requests

def send_slack_notification(webhook_url, message):
    """Send notification to Slack channel"""

    payload = {
        "text": message,
        "attachments": [
            {
                "color": "good",
                "fields": [
                    {
                        "title": "Case",
                        "value": "Smith v. Jones",
                        "short": True
                    },
                    {
                        "title": "Status",
                        "value": "Review Complete",
                        "short": True
                    }
                ]
            }
        ]
    }

    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200

# Usage
webhook = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
send_slack_notification(
    webhook,
    "Motion to Dismiss review complete. Found 3 issues to fix."
)
```

## Testing Examples

### Test Citation Verification

```python
import unittest
from wepublic_defender.citations import CitationVerifier

class TestCitationVerification(unittest.TestCase):

    def setUp(self):
        self.verifier = CitationVerifier()

    def test_valid_citation(self):
        """Test that valid citations pass"""
        citation = "Brown v. Board of Education, 347 U.S. 483 (1954)"
        result = self.verifier.verify_single(citation)
        self.assertEqual(result["status"], "valid")

    def test_invalid_format(self):
        """Test that invalid formats are caught"""
        citation = "Some Case from 2020"
        result = self.verifier.verify_single(citation)
        self.assertEqual(result["status"], "invalid_format")

    def test_overruled_case(self):
        """Test detection of overruled cases"""
        # Use a known overruled case
        citation = "Plessy v. Ferguson, 163 U.S. 537 (1896)"
        result = self.verifier.verify_single(citation)
        self.assertIn("overruled", result.get("warning", "").lower())

if __name__ == "__main__":
    unittest.main()
```

## Next Steps

- Try these examples in your case
- Modify for your specific needs
- Explore [API Reference](API-Reference) for more options
- See [Advanced Features](Advanced-Features) for complex workflows
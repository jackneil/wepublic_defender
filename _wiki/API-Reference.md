# API Reference

Complete API documentation for WePublicDefender's programmatic interfaces and command-line tools.

## Core CLI Commands

### wpd-check-env

Check environment and configuration status.

**Usage**:
```bash
wpd-check-env [options]
```

**Options**:
- `--verbose` - Detailed output
- `--fix` - Attempt to fix issues automatically

**Returns**:
- Environment status
- API key validation
- Installation status
- Case initialization status

**Example**:
```bash
$ wpd-check-env
✓ Python 3.11.5
✓ WePublicDefender installed
✓ API keys configured
✓ Case initialized
Status: Ready
```

### wpd-init-case

Initialize a new case directory structure.

**Usage**:
```bash
wpd-init-case [options]
```

**Options**:
- `--path PATH` - Case directory path (default: current)
- `--force` - Overwrite existing structure
- `--template TYPE` - Case template (default: standard)

**Creates**:
- Standard directory structure
- Configuration files
- Claude integration

**Example**:
```bash
$ wpd-init-case
Creating case structure...
✓ Directories created
✓ Configuration initialized
✓ Claude commands installed
Case ready!
```

### wpd-run-agent

Run AI agents for document review and analysis.

**Usage**:
```bash
wpd-run-agent --agent AGENT_NAME [options]
```

**Required Arguments**:
- `--agent` - Agent type: self_review, citation_verify, opposing_counsel, drafter, organize, fact_verify

**Options**:
- `--file FILE` - Input file path
- `--mode MODE` - Execution mode: guidance (free) or external-llm (paid)
- `--model MODEL` - Specific model to use
- `--run-both` - Run all configured models
- `--web-search` - Enable web search
- `--verbose` - Detailed output

**Examples**:
```bash
# Guidance mode (free)
wpd-run-agent --agent self_review --file draft.md --mode guidance

# External LLM mode
wpd-run-agent --agent citation_verify --file brief.md --mode external-llm --web-search

# Single model
wpd-run-agent --agent opposing_counsel --file motion.md --model gpt-4o
```

### wpd-pdf-to-images

Convert PDF to images for Claude processing.

**Usage**:
```bash
wpd-pdf-to-images PDF_PATH [options]
```

**Options**:
- `--output-dir DIR` - Output directory
- `--dpi DPI` - Image quality (default: 200)
- `--format FORMAT` - Image format: png, jpg (default: png)

**Example**:
```bash
$ wpd-pdf-to-images evidence.pdf --output-dir ./images --dpi 300
Converting PDF to images...
✓ Created 15 images in ./images/
```

### wpd-usage-summary

Display API usage and cost summary.

**Usage**:
```bash
wpd-usage-summary [options]
```

**Options**:
- `--period PERIOD` - Time period: today, week, month, all
- `--by-model` - Group by model
- `--by-operation` - Group by operation
- `--csv` - Export as CSV

**Example**:
```bash
$ wpd-usage-summary --period today
Today's Usage:
- Reviews: $3.42
- Research: $1.20
- Total: $4.62
```

## Python API

### Core Module

```python
from wepublic_defender import WePublicDefender

# Initialize
wpd = WePublicDefender(case_path="/path/to/case")

# Run operations
result = wpd.review_document("draft.md", mode="guidance")
```

### Agent Interface

```python
from wepublic_defender.agents import ReviewAgent

# Create agent
agent = ReviewAgent(
    models=["gpt-4o", "grok-4"],
    enable_web_search=True
)

# Run review
results = agent.review(
    file_path="motion.md",
    mode="external-llm"
)
```

### Document Handlers

```python
from wepublic_defender.document_handlers import DocumentOrganizer

# Organize documents
organizer = DocumentOrganizer(case_path=".")
results = organizer.organize_inbox()

# Process specific document
organizer.process_document("contract.pdf")
```

### LLM Client

```python
from wepublic_defender.llm_client import LLMClient

# Initialize client
client = LLMClient(
    provider="openai",
    model="gpt-4o",
    api_key="sk-..."
)

# Make request
response = client.complete(
    prompt="Review this legal text",
    temperature=0.3
)
```

## Agent Types

### self_review

Reviews documents for legal issues.

**Capabilities**:
- Identify missing elements
- Check legal standards
- Find procedural errors
- Assess argument strength

**Configuration**:
```json
{
  "self_review_agent": {
    "models": ["gpt-4o", "grok-4"],
    "focus_areas": ["legal_reasoning", "procedure"],
    "severity_threshold": "major"
  }
}
```

### citation_verify

Verifies legal citations.

**Capabilities**:
- Check if cases still good law
- Verify citation format
- Find subsequent history
- Validate quotations

**Configuration**:
```json
{
  "citation_verify_agent": {
    "models": ["gpt-4o"],
    "enable_web_search": true,
    "check_courtlistener": true
  }
}
```

### opposing_counsel

Simulates opposing counsel attacks.

**Capabilities**:
- Find weaknesses
- Identify counter-arguments
- Spot procedural defects
- Suggest opposing strategy

**Configuration**:
```json
{
  "opposing_counsel_agent": {
    "models": ["grok-4"],
    "aggressiveness": "high",
    "jurisdiction_aware": true
  }
}
```

### drafter

Drafts legal documents.

**Capabilities**:
- Generate pleadings
- Create motions
- Draft discovery
- Write correspondence

**Configuration**:
```json
{
  "drafter_agent": {
    "models": ["gpt-4o"],
    "style": "formal",
    "jurisdiction": "federal"
  }
}
```

### organize

Organizes documents (guidance only).

**Capabilities**:
- Identify document types
- Sort into folders
- Track movements
- Update indices

**Note**: Always runs in guidance mode.

### fact_verify

Verifies factual claims against evidence.

**Capabilities**:
- Check dates/times
- Verify amounts
- Validate claims
- Find contradictions

**Configuration**:
```json
{
  "fact_verify_agent": {
    "evidence_path": "04_EVIDENCE/",
    "strict_mode": true
  }
}
```

## Configuration Files

### .env

Environment variables and API keys.

```bash
# Required
OPENAI_API_KEY=sk-proj-...
XAI_API_KEY=xai-...

# Optional
COURTLISTENER_TOKEN=...
COURTLISTENER_USER_AGENT=WePublicDefender/1.0
ANTHROPIC_API_KEY=sk-ant-...
```

### legal_review_settings.json

Agent and model configuration.

```json
{
  "version": "1.0.0",
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-4o", "grok-4"],
      "temperature": 0.3,
      "max_tokens": 4096,
      "reasoning_effort": "high"
    }
  },
  "cost_control": {
    "max_cost_per_review": 10.00,
    "require_confirmation_above": 5.00
  }
}
```

### case_settings.json

Case-specific configuration.

```json
{
  "case_name": "Smith v. Jones",
  "case_number": "1:24-cv-00123",
  "court": "D. South Carolina",
  "jurisdiction": {
    "federal": true,
    "circuit": "4th",
    "state": "SC"
  }
}
```

### env_info.json

Python environment paths.

```json
{
  "python_exe": "/path/to/python",
  "conda_env": "wepublic_defender",
  "repo_path": "/path/to/wepublic_defender"
}
```

## Response Formats

### Agent Response

```json
{
  "agent": "self_review",
  "mode": "external-llm",
  "timestamp": "2025-10-15T09:30:00Z",
  "structured": {
    "critical_issues": [...],
    "major_issues": [...],
    "minor_issues": [...]
  },
  "claude_prompt": "Found 3 critical issues...",
  "cost": 2.45,
  "tokens": {
    "input": 5000,
    "output": 2000
  }
}
```

### Organization Result

```json
{
  "processed": 15,
  "movements": [
    {
      "source": "00_NEW_DOCUMENTS_INBOX/complaint.pdf",
      "destination": "02_PLEADINGS/01_Complaint/complaint.pdf",
      "type": "pleading",
      "timestamp": "2025-10-15T09:30:00Z"
    }
  ],
  "errors": []
}
```

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| ENV_001 | Missing API key | Add to .env file |
| ENV_002 | Invalid API key | Check key format |
| ENV_003 | No credits | Add payment method |
| FILE_001 | File not found | Check path |
| FILE_002 | Permission denied | Check permissions |
| AGENT_001 | Agent not found | Check agent name |
| AGENT_002 | Mode not supported | Use different mode |
| API_001 | Rate limit | Wait and retry |
| API_002 | Timeout | Check connection |

## Logging

### Log Levels

- `DEBUG` - Detailed debugging
- `INFO` - Normal operations
- `WARNING` - Potential issues
- `ERROR` - Errors that need attention
- `CRITICAL` - System failures

### Log Location

`.wepublic_defender/logs/wpd.log`

### Log Format

```
2025-10-15 09:30:00,123 - INFO - Running self_review on motion.md
2025-10-15 09:30:05,456 - DEBUG - Tokens used: 5000 in, 2000 out
2025-10-15 09:30:05,789 - INFO - Review complete, cost: $2.45
```

## Webhooks and Integrations

### GitHub Integration

```yaml
# .github/workflows/review.yml
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: wpd-run-agent --agent self_review --file ${{ github.event.pull_request.title }}
```

### Slack Notifications

```python
# Custom integration
from wepublic_defender.integrations import SlackNotifier

notifier = SlackNotifier(webhook_url="...")
notifier.send("Review complete", results)
```

## Rate Limits

### OpenAI
- Requests: 500/min
- Tokens: 90,000/min

### xAI (Grok)
- Requests: 60/min
- Tokens: 60,000/min

### Handling Rate Limits

```python
from wepublic_defender.utils import retry_with_backoff

@retry_with_backoff(max_retries=3)
def make_api_call():
    # Your API call
    pass
```

## Best Practices

### Error Handling

```python
from wepublic_defender.exceptions import APIError, FileError

try:
    result = wpd.review_document("draft.md")
except APIError as e:
    print(f"API error: {e}")
except FileError as e:
    print(f"File error: {e}")
```

### Async Operations

```python
import asyncio
from wepublic_defender.async_client import AsyncReviewAgent

async def review_multiple():
    agent = AsyncReviewAgent()
    tasks = [
        agent.review("doc1.md"),
        agent.review("doc2.md")
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### Custom Agents

```python
from wepublic_defender.agents import BaseAgent

class CustomAgent(BaseAgent):
    def process(self, input_data):
        # Custom processing
        return results
```

## Version History

- **1.0.0** - Initial release
- **1.1.0** - Added fact_verify agent
- **1.2.0** - Web search integration
- **1.3.0** - Multi-model support

## Support

- GitHub Issues: https://github.com/jackneil/wepublic_defender/issues
- Documentation: https://github.com/jackneil/wepublic_defender/wiki

## Next Steps

- Review [Configuration](Configuration) options
- Understand [Cost Guide](Cost-Guide)
- Learn [Basic Usage](Basic-Usage)
- Explore [Advanced Features](Advanced-Features)
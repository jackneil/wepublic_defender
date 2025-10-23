# Advanced Features

This guide covers advanced features for power users who want to maximize WePublicDefender's capabilities.

## Platform-Aware Hooks

### SessionStart Hook

Automatically runs when Claude Code starts in your case folder.

**Location**: `.claude/hooks/SessionStart`

**Default behavior**:
- Loads case context
- Checks for deadlines
- Offers relevant options

**Customization**:
```bash
# .claude/hooks/SessionStart
echo "Loading case: Smith v. Jones"
echo "Checking deadlines..."
echo "Run /start for full context"
```

### Custom Hooks

Create your own hooks for specific events:

```bash
# .claude/hooks/PreReview
echo "Running pre-review checks..."
python check_citations.py
```

## Multi-Model Configuration

### Parallel Model Execution

Run multiple models simultaneously for consensus:

```json
{
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-4o", "grok-4", "claude-3"],
      "parallel": true,
      "consensus_threshold": 0.8
    }
  }
}
```

### Model Specialization

Assign different models to different tasks:

```json
{
  "model_assignments": {
    "legal_reasoning": "gpt-4o",
    "fact_checking": "grok-4",
    "writing_style": "claude-3",
    "citations": "gpt-4o"
  }
}
```

### Custom Model Providers

Add new model providers:

```python
from wepublic_defender.providers import BaseProvider

class CustomProvider(BaseProvider):
    def __init__(self, api_key):
        self.api_key = api_key

    def complete(self, prompt, **kwargs):
        # Your implementation
        return response
```

## Citation Management System

### Advanced Citation Verification

```python
from wepublic_defender.citations import CitationVerifier

verifier = CitationVerifier(
    check_courtlistener=True,
    check_google_scholar=True,
    verify_quotes=True,
    check_pin_cites=True
)

results = verifier.verify_document("brief.md")
```

### Citation Caching

Avoid repeated lookups:

```json
{
  "citation_cache": {
    "enabled": true,
    "ttl_days": 30,
    "cache_location": ".wepublic_defender/citation_cache/"
  }
}
```

### Jurisdiction-Specific Rules

```json
{
  "citation_rules": {
    "federal": {
      "format": "bluebook",
      "parallel_citations": false
    },
    "south_carolina": {
      "format": "bluebook",
      "require_pinpoint": true
    }
  }
}
```

## Custom Workflows

### Pipeline Customization

Create custom review pipelines:

```json
{
  "custom_pipelines": {
    "quick_review": [
      "self_review",
      "citation_verify"
    ],
    "full_review": [
      "self_review",
      "citation_verify",
      "opposing_counsel",
      "fact_verify",
      "final_check"
    ],
    "pre_filing": [
      "self_review",
      "citation_verify",
      "local_rules_check",
      "formatting_check"
    ]
  }
}
```

### Conditional Workflows

```python
from wepublic_defender.workflows import ConditionalWorkflow

workflow = ConditionalWorkflow()
workflow.add_condition(
    if_true="document.length > 10000",
    then="break_into_sections",
    else="review_whole"
)
```

## Document Processing

### Template System

Create reusable document templates:

```yaml
# .wepublic_defender/templates/motion_to_dismiss.yaml
template:
  type: motion
  sections:
    - introduction
    - statement_of_facts
    - legal_standard
    - argument
    - conclusion

  boilerplate:
    introduction: |
      Defendant respectfully moves this Court...
    legal_standard: |
      Under Federal Rule 12(b)(6)...
```

### Batch Processing

Process multiple documents:

```python
from wepublic_defender.batch import BatchProcessor

processor = BatchProcessor()
results = processor.process_folder(
    "03_DISCOVERY/Productions/",
    operation="extract_key_facts"
)
```

### Document Comparison

```python
from wepublic_defender.compare import DocumentComparer

comparer = DocumentComparer()
changes = comparer.compare(
    "motion_v1.md",
    "motion_v2.md",
    highlight_legal_changes=True
)
```

## Integration Patterns

### API Integration

```python
from wepublic_defender.api import WePublicDefenderAPI

# Create API server
api = WePublicDefenderAPI(port=8080)

@api.route("/review", methods=["POST"])
def review_endpoint(request):
    document = request.json["document"]
    result = api.review(document)
    return jsonify(result)

api.run()
```

### Database Integration

```python
from wepublic_defender.database import CaseDatabase

db = CaseDatabase("sqlite:///case.db")
db.store_document("motion.md", metadata={
    "type": "motion",
    "date_filed": "2025-10-15"
})

motions = db.query(document_type="motion")
```

### Email Integration

```python
from wepublic_defender.email import EmailMonitor

monitor = EmailMonitor(
    imap_server="imap.gmail.com",
    username="you@example.com"
)

monitor.on_new_email(lambda email:
    wpd.process_attachment(email.attachments)
)
```

## Performance Optimization

### Caching Strategy

```json
{
  "cache_config": {
    "document_cache": true,
    "citation_cache": true,
    "research_cache": true,
    "ttl_hours": 24
  }
}
```

### Token Optimization

```python
from wepublic_defender.optimization import TokenOptimizer

optimizer = TokenOptimizer()
compressed = optimizer.compress_document(
    "large_document.md",
    preserve_legal_content=True
)
```

### Parallel Processing

```python
import asyncio
from wepublic_defender.async import AsyncReviewer

async def review_multiple():
    reviewer = AsyncReviewer()
    docs = ["doc1.md", "doc2.md", "doc3.md"]

    tasks = [reviewer.review(doc) for doc in docs]
    results = await asyncio.gather(*tasks)
    return results
```

## Security Features

### Encryption

```python
from wepublic_defender.security import Encryptor

encryptor = Encryptor(key="your-encryption-key")
encrypted = encryptor.encrypt_document("sensitive.md")
decrypted = encryptor.decrypt_document(encrypted)
```

### Audit Logging

```json
{
  "audit_config": {
    "log_all_operations": true,
    "log_api_calls": true,
    "log_file_access": true,
    "retention_days": 90
  }
}
```

### Access Control

```python
from wepublic_defender.access import AccessControl

access = AccessControl()
access.require_password_for([
    "delete_document",
    "modify_timeline",
    "export_case"
])
```

## Custom Agents

### Creating Custom Agents

```python
from wepublic_defender.agents import BaseAgent

class ContractReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.focus_areas = [
            "payment_terms",
            "termination_clauses",
            "liability_limits"
        ]

    def review(self, contract_path):
        # Custom review logic
        issues = self.find_issues(contract_path)
        return self.format_report(issues)
```

### Agent Chaining

```python
from wepublic_defender.chains import AgentChain

chain = AgentChain()
chain.add("self_review")
chain.add("custom_contract_review")
chain.add("risk_assessment")

result = chain.execute("contract.pdf")
```

## Advanced Research

### Research Automation

```python
from wepublic_defender.research import ResearchAutomation

researcher = ResearchAutomation()
researcher.research_topics([
    "qualified immunity fourth circuit",
    "section 1983 elements",
    "municipal liability"
])

report = researcher.generate_memo()
```

### Case Law Tracking

```json
{
  "case_tracking": {
    "monitor_cases": [
      "Smith v. Jones",
      "Johnson v. State"
    ],
    "alert_on_updates": true,
    "check_frequency": "daily"
  }
}
```

## Debugging Tools

### Verbose Mode

```bash
wpd-run-agent --agent self_review --file draft.md --debug --trace
```

### Performance Profiling

```python
from wepublic_defender.profiling import Profiler

with Profiler() as prof:
    result = wpd.review_document("large_brief.md")

prof.print_stats()
# Time: 45.3s
# Tokens: 25,000
# API Calls: 5
```

### Error Recovery

```python
from wepublic_defender.recovery import RecoveryManager

recovery = RecoveryManager()
recovery.enable_auto_save(interval_seconds=30)
recovery.enable_crash_recovery()

# If crash occurs, resume from last checkpoint
recovery.resume_if_crashed()
```

## Export and Reporting

### Case Export

```python
from wepublic_defender.export import CaseExporter

exporter = CaseExporter()
exporter.export_case(
    format="pdf",
    include_metadata=True,
    redact_sensitive=True
)
```

### Custom Reports

```python
from wepublic_defender.reports import ReportGenerator

generator = ReportGenerator()
report = generator.create_report(
    template="case_summary",
    data={
        "case_name": "Smith v. Jones",
        "documents_reviewed": 47,
        "issues_found": 12
    }
)
```

## Automation Scripts

### Daily Tasks

```python
# daily_routine.py
from wepublic_defender.automation import DailyRoutine

routine = DailyRoutine()
routine.check_deadlines()
routine.organize_inbox()
routine.update_timeline()
routine.generate_status_report()
```

### Scheduled Operations

```python
from wepublic_defender.scheduler import Scheduler

scheduler = Scheduler()
scheduler.every_day_at("09:00").do(check_deadlines)
scheduler.every_monday().do(weekly_review)
scheduler.run()
```

## Testing Frameworks

### Document Testing

```python
from wepublic_defender.testing import DocumentTester

tester = DocumentTester()
tester.test_citations("brief.md")
tester.test_formatting("motion.md")
tester.test_arguments("response.md")
```

### Mock Reviews

```python
from wepublic_defender.testing import MockReviewer

mock = MockReviewer()
mock.simulate_review(
    document="draft.md",
    issues_to_inject=["missing_jurisdiction", "bad_citation"]
)
```

## Best Practices

### Configuration Management

1. Keep settings in version control
2. Use environment-specific configs
3. Document custom settings
4. Regular config backups

### Performance Tips

1. Cache frequently accessed data
2. Use batch operations
3. Optimize token usage
4. Profile slow operations

### Security Recommendations

1. Encrypt sensitive documents
2. Use audit logging
3. Regular security updates
4. Access control for critical operations

## Troubleshooting Advanced Features

### Debug Custom Agents

```python
from wepublic_defender.debug import AgentDebugger

debugger = AgentDebugger()
debugger.trace_agent_execution("custom_agent", "test_doc.md")
```

### Performance Issues

```bash
# Profile slow operations
wpd-profile --operation review --file large_doc.md
```

### Integration Problems

Check logs in:
- `.wepublic_defender/logs/integration.log`
- `.wepublic_defender/logs/api.log`

## Next Steps

- Implement [Custom Workflows](#custom-workflows)
- Set up [Integration Patterns](#integration-patterns)
- Configure [Performance Optimization](#performance-optimization)
- Explore [API Reference](API-Reference)
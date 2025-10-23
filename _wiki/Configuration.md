# Configuration Guide

This guide explains how to configure WePublicDefender for your specific needs, from API keys to review settings.

## Configuration Files Overview

WePublicDefender uses several configuration files:

1. **`.env`** - API keys and credentials
2. **`.wepublic_defender/legal_review_settings.json`** - AI model configuration
3. **`.wepublic_defender/env_info.json`** - Python environment paths
4. **`.wepublic_defender/case_settings.json`** - Case-specific settings

## API Key Configuration

### The .env File

Your `.env` file stores API credentials. Create it in your case folder:

```bash
# Required API Keys
OPENAI_API_KEY=sk-proj-abc123...
XAI_API_KEY=xai-def456...

# Optional but Recommended
COURTLISTENER_TOKEN=ghi789...
COURTLISTENER_USER_AGENT=WePublicDefender/1.0

# Optional Additional Services
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

### Managing Multiple Cases

#### Option 1: Shared Keys (Recommended)

Keep a master `.env` template and copy to each case:
```bash
# Create master template
echo "OPENAI_API_KEY=..." > ~/wpd_keys.env

# Copy to new case
cp ~/wpd_keys.env /path/to/case/.env
```

#### Option 2: Environment Variables

Set system-wide (but less secure):
```bash
export OPENAI_API_KEY=sk-proj-...
export XAI_API_KEY=xai-...
```

### Security Best Practices

1. **Never commit `.env` to git** (it's gitignored by default)
2. **Use strong, unique API keys**
3. **Rotate keys periodically**
4. **Set spending limits** on API provider dashboards
5. **Store backup of keys** in password manager

## AI Model Configuration

### Review Settings File

`.wepublic_defender/legal_review_settings.json` controls which AI models are used:

```json
{
  "version": "1.0.0",
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-5", "grok-4"],
      "enable_web_search": false,
      "temperature": 0.3,
      "reasoning_effort": "high"
    },
    "citation_verify_agent": {
      "models": ["gpt-5"],
      "enable_web_search": true,
      "check_courtlistener": true
    },
    "opposing_counsel_agent": {
      "models": ["grok-4"],
      "aggressiveness": "high",
      "jurisdiction_aware": true
    }
  }
}
```

### Model Selection

#### Available Models

**OpenAI Models**:
- `"gpt-5"` - Best reasoning (doesn't exist yet, uses 4o)
- `"gpt-4o"` - Current best
- `"gpt-4o-mini"` - Faster, cheaper

**xAI Models**:
- `"grok-4"` - Latest Grok model
- `"grok-beta"` - Experimental features

#### Single vs Multiple Models

**Single model** (faster, cheaper):
```json
"models": ["gpt-5"]
```

**Multiple models** (adversarial review, more thorough):
```json
"models": ["gpt-5", "grok-4"]
```

### Agent-Specific Settings

#### Self Review Agent

Controls document review:
```json
"self_review_agent": {
  "models": ["gpt-5", "grok-4"],
  "focus_areas": [
    "legal_reasoning",
    "procedural_compliance",
    "factual_accuracy"
  ],
  "severity_threshold": "major"
}
```

#### Citation Verification

Controls citation checking:
```json
"citation_verify_agent": {
  "models": ["gpt-5"],
  "enable_web_search": true,
  "check_courtlistener": true,
  "verify_quotes": true,
  "check_subsequent_history": true
}
```

#### Opposing Counsel

Controls adversarial review:
```json
"opposing_counsel_agent": {
  "models": ["grok-4"],
  "strategy": "aggressive",
  "look_for": [
    "procedural_defects",
    "waived_arguments",
    "fact_disputes",
    "alternative_theories"
  ]
}
```

## Case-Specific Configuration

### Case Settings

`.wepublic_defender/case_settings.json` stores case details:

```json
{
  "case_name": "Johnson v. Acme Corp",
  "case_number": "1:25-cv-00123",
  "court": "S.D. South Carolina",
  "judge": "Hon. Jane Smith",
  "jurisdiction": {
    "federal": true,
    "circuit": "4th",
    "state": "SC"
  },
  "parties": {
    "plaintiff": "John Johnson",
    "defendant": "Acme Corp"
  },
  "case_type": "civil_rights",
  "stage": "discovery"
}
```

### Jurisdiction Settings

Affects citation preferences and procedural rules:

```json
"jurisdiction": {
  "federal": true,
  "circuit": "4th",
  "state": "SC",
  "prefer_local_rules": true,
  "citation_format": "bluebook"
}
```

## Environment Configuration

### Python Environment

`.wepublic_defender/env_info.json` stores Python paths:

```json
{
  "python_exe": "C:/Users/You/.conda/envs/wepublic_defender/python.exe",
  "conda_env": "wepublic_defender",
  "repo_path": "C:/Github/wepublic_defender"
}
```

### Updating Environment

To change Python environment:
```bash
# Find new Python path
conda activate new_env
python -c "import sys; print(sys.executable)"

# Update config
# Claude will update env_info.json
```

## Performance Settings

### Model Performance

Trade-off between quality and speed:

```json
"performance": {
  "reasoning_effort": "high",    // high, medium, low
  "temperature": 0.3,            // 0.0-1.0, lower = more focused
  "max_tokens": 4096,           // response length limit
  "timeout": 300                 // seconds before timeout
}
```

### Parallel Processing

Control parallel model execution:

```json
"execution": {
  "parallel_models": true,       // run models simultaneously
  "max_concurrent": 2,          // max models at once
  "retry_on_error": true,       // retry failed calls
  "max_retries": 3
}
```

## Cost Control Settings

### Budget Limits

Set spending limits:

```json
"cost_control": {
  "max_cost_per_review": 10.00,
  "max_cost_per_day": 50.00,
  "warn_at_cost": 5.00,
  "require_confirmation_above": 15.00
}
```

### Model Selection by Cost

Prefer cheaper models for routine work:

```json
"cost_optimization": {
  "use_cheap_models_for": ["drafts", "organization"],
  "use_expensive_models_for": ["final_review", "citations"],
  "cheap_models": ["gpt-4o-mini"],
  "expensive_models": ["gpt-5", "grok-4"]
}
```

## Web Search Configuration

### Search Settings

Control web search behavior:

```json
"web_search": {
  "enabled": true,
  "providers": ["courtlistener", "google"],
  "max_results": 10,
  "filter_date": "2020-01-01",
  "prefer_recent": true
}
```

### CourtListener Integration

Legal-specific search:

```json
"courtlistener": {
  "enabled": true,
  "courts": ["scotus", "ca4", "scd"],
  "case_types": ["civil", "criminal"],
  "date_filed_after": "2015-01-01"
}
```

## Notification Settings

### Deadline Warnings

Configure deadline notifications:

```json
"notifications": {
  "deadline_warning_days": [7, 3, 1],
  "check_on_startup": true,
  "highlight_urgent": true
}
```

## Custom Prompts

### System Prompts

Customize AI behavior:

```json
"custom_prompts": {
  "review_style": "Focus on Fourth Circuit precedent",
  "writing_style": "Formal, precise, avoid legalese",
  "citation_format": "Always include pin cites"
}
```

## Backup and Recovery

### Auto-Backup Settings

```json
"backup": {
  "enabled": true,
  "frequency": "daily",
  "location": "~/wpd_backups/",
  "keep_versions": 7
}
```

## Debugging Settings

### Verbose Output

For troubleshooting:

```json
"debug": {
  "verbose": true,
  "log_level": "DEBUG",
  "save_raw_responses": true,
  "log_api_calls": true
}
```

## Quick Configuration Commands

### Check Current Config

```bash
Show me my current configuration
```

### Update API Key

```bash
Update my OpenAI API key
```

### Change Models

```bash
Switch to using only GPT-5 for reviews
```

### Set Budget

```bash
Set maximum daily spending to $25
```

## Configuration Best Practices

### For New Users

Start with defaults:
1. Use provided `legal_review_settings.json`
2. Add API keys to `.env`
3. Run `/check-env` to verify

### For Simple Cases

Optimize for cost:
```json
{
  "models": ["gpt-4o-mini"],
  "enable_web_search": false
}
```

### For Complex Cases

Maximize thoroughness:
```json
{
  "models": ["gpt-5", "grok-4", "gemini-ultra"],
  "enable_web_search": true,
  "reasoning_effort": "high"
}
```

### For Time-Sensitive Work

Optimize for speed:
```json
{
  "models": ["gpt-4o-mini"],
  "parallel_models": false,
  "timeout": 60
}
```

## Troubleshooting Configuration

### API Key Not Working

1. Check `.env` format (no quotes around keys)
2. Verify key on provider's website
3. Check account has credits
4. Run `/check-env`

### Wrong Models Being Used

1. Check `.wepublic_defender/legal_review_settings.json`
2. Verify model names are correct
3. Check API keys for those providers

### Settings Not Taking Effect

1. Restart Claude Code after changes
2. Verify JSON syntax is valid
3. Check file is in correct location

## Migration from Older Versions

### Updating Settings Format

If upgrading from older version:
```bash
Migrate my settings to the latest format
```

Claude will update configuration files automatically.

## Next Steps

- Test configuration with [Basic Usage](Basic-Usage)
- Understand costs with [Cost Guide](Cost-Guide)
- Learn about [Advanced Features](Advanced-Features)
- Set up [Performance Optimization](Performance-Optimization)
# Quick Reference Guide

Fast lookup for common WePublicDefender operations.

## Essential Commands

```
/check-env              Check environment and API keys
/organize               Organize files from inbox
/timeline               View/update case timeline
/start                  Refresh session context
/deep-research-prep     Generate deep research prompt
/research [topic]       Quick legal research
/strategy               Get strategic recommendations
/draft [type]           Draft legal document
/review [file]          Run adversarial review
```

## Common Agent Commands

### Guidance Mode (Free)
```bash
wpd-run-agent --agent self_review --file draft.md --mode guidance
wpd-run-agent --agent drafter --text "Draft motion" --mode guidance
wpd-run-agent --agent organize --mode guidance
```

### External-LLM Mode (Costs Money)
```bash
wpd-run-agent --agent self_review --file draft.md --mode external-llm
wpd-run-agent --agent citation_verify --file draft.md --mode external-llm --web-search
wpd-run-agent --agent opposing_counsel --file draft.md --mode external-llm
```

## Directory Structure

```
00_NEW_DOCUMENTS_INBOX/  - Drop files here
01_CASE_OVERVIEW/        - Case summary, parties, timeline
02_PLEADINGS/            - Court filings
03_DISCOVERY/            - Discovery materials
04_EVIDENCE/             - Evidence files
05_CORRESPONDENCE/       - Letters and emails
06_RESEARCH/             - Legal research
07_DRAFTS_AND_WORK_PRODUCT/ - Working documents
08_REFERENCE/            - Court rules, templates
.wepublic_defender/      - System files
.database/               - File tracking
```

## Review Pipeline Phases

1. **Organization** - File organization check
2. **Self-Review** - Legal sufficiency review
3. **Citations** - Verify all citations still good law
4. **Opposing Counsel** - Adversarial attack simulation
5. **Final Review** - Pre-filing compliance check

**Rule:** If ANY phase finds issues, fix them and re-run ENTIRE pipeline.

## File Naming Conventions

```
MOTION_TO_DISMISS_v1.md          Draft version 1
MOTION_TO_DISMISS_v2.md          Draft version 2
MOTION_TO_DISMISS_FINAL.md       Final draft
2025-10-15_MotionToDismiss.pdf   Filed version
```

## Cost Quick Reference

### Typical Costs (Approximate)

| Task | Mode | Cost |
|------|------|------|
| File organization | Guidance only | $0 |
| Self-review | Guidance | $0 |
| Self-review | External-LLM (1 model) | $1-2 |
| Self-review | External-LLM (2 models) | $2-4 |
| Citation verification | External-LLM + web | $2-5 |
| Opposing counsel | External-LLM | $2-4 |
| Full pipeline | All external-LLM | $8-18 |
| Deep research | Claude.ai | $3-8 |

### Cost Optimization Tips

1. Use guidance mode for first drafts
2. Run single model instead of multiple
3. Cache citation verifications
4. Target specific phases instead of full pipeline
5. Pre-fix obvious issues before running pipeline

## Environment Variables

In your case folder's `.env` file:

```bash
OPENAI_API_KEY=sk-proj-...
XAI_API_KEY=xai-...
COURTLISTENER_TOKEN=...      # Optional
COURTLISTENER_USER_AGENT=WePublicDefender/1.0
```

## Key Files to Know

### Case Management
- `GAMEPLAN.md` - Strategic roadmap, deadlines
- `.wepublic_defender/session_notes.md` - Work tracking
- `.wepublic_defender/case_timeline.md` - Historical events

### Configuration
- `.env` - API keys
- `.wepublic_defender/legal_review_settings.json` - Agent config
- `.wepublic_defender/env_info.json` - Environment paths

### Tracking
- `.wepublic_defender/usage_log.csv` - API usage costs
- `.database/file_management_log.md` - File movements
- `06_RESEARCH/CITATIONS_LOG.md` - Citation cache

## Workflow Quick Starts

### Starting New Case
```
1. mkdir CaseName && cd CaseName
2. claude
3. [Paste automated setup from README]
4. Restart Claude
5. /organize
6. /strategy
7. /deep-research-prep
```

### Reviewing Draft Before Filing
```
1. /review path/to/MOTION_v3.md
2. Wait for all agents to complete
3. Review findings critically
4. Research LLM concerns if needed
5. Fix valid issues
6. Re-run /review until clean pass
7. Convert to Word and file
```

### Quick Research
```
1. /research [legal topic]
2. Claude does web search
3. Results saved to 06_RESEARCH/
4. Update CITATIONS_LOG.md if applicable
```

### Deep Research (Comprehensive)
```
1. /deep-research-prep
2. Copy generated prompt
3. Open https://claude.ai
4. Enable Research mode
5. Paste prompt
6. Wait 5-10 minutes
7. Download results to 00_NEW_DOCUMENTS_INBOX/
8. Tell Claude "Done"
9. Claude processes and generates GAMEPLAN
```

## Agent Modes Cheat Sheet

| Agent | Guidance | External-LLM | File Access | Web Search |
|-------|----------|--------------|-------------|------------|
| organize | ✓ | ✗ | Yes | No |
| self_review | ✓ | ✓ | No | Optional |
| citation_verify | ✓ | ✓ | No | Yes |
| opposing_counsel | ✓ | ✓ | No | Optional |
| fact_verify | ✓ | ✗ | Yes | No |
| final_review | ✓ | ✓ | No | No |
| drafter | ✓ | ✓ | No | No |
| strategy | ✓ | ✓ | No | Optional |
| research | ✓ | ✓ | No | Yes |

**✓ = Supported**, **✗ = Not supported**

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Command not found | Run `/check-env`, restart Claude |
| API key error | Check `.env` file, verify account has credit |
| File not found | Use full path or check working directory |
| Claude confused | Run `/start` to refresh context |
| High API costs | Switch to guidance mode, use single model |
| Timeout | Claude Code 2.0.22+ auto-backgrounds, use `/bashes` to check |
| Citations taking forever | Normal for web search (3-5 minutes) |

## Best Practices Checklist

### Before Drafting
- [ ] Completed research on legal issue
- [ ] Reviewed court rules and procedures
- [ ] Organized all evidence and discovery
- [ ] Updated GAMEPLAN.md with strategy

### Before Filing
- [ ] Ran full review pipeline
- [ ] All citations verified as good law
- [ ] Opposing counsel review completed
- [ ] Clean pass with zero changes
- [ ] Converted to proper format (.docx if required)
- [ ] Double-checked filing deadline
- [ ] Verified service requirements

### Session Management
- [ ] Session notes updated after each task
- [ ] Case timeline updated for major events
- [ ] GAMEPLAN reflects current status
- [ ] Usage costs tracked and reasonable

## Claude Code Features

### Tab Key
Press Tab to show/hide Claude's thinking process.

**When to show thinking:**
- Processing complex agent results
- Making important decisions
- Want to understand Claude's reasoning

### Plan Mode
Type `/plan` or Ctrl+P to enter Plan Mode.

**Use Plan Mode for:**
- Processing agent review results
- Making changes to important documents
- Organizing large file batches
- Reviewing strategic decisions

### /bashes Command
Check background task status.

**Use when:**
- Agent seems to be taking long time
- Running multiple agents in parallel
- Want to verify process didn't crash

## Git Integration

### Recommended .gitignore
```
.env
*.pdf
*.docx
.database/
.wepublic_defender/logs/
.wepublic_defender/usage_log.csv
```

### Useful Git Commands
```bash
git add GAMEPLAN.md 07_DRAFTS_AND_WORK_PRODUCT/
git commit -m "Completed motion v3 after review"
git log --oneline --graph
git diff HEAD~1 07_DRAFTS_AND_WORK_PRODUCT/MOTION_v3.md
```

## API Key Management

### Getting Keys

**OpenAI**: https://platform.openai.com/api-keys
**xAI**: https://console.x.ai/
**CourtListener**: https://www.courtlistener.com/api/

### Checking Balance

**OpenAI**: https://platform.openai.com/usage
**xAI**: Console dashboard

### Security

- Never commit `.env` to git
- Use different keys per case if needed
- Rotate keys if compromised
- Set spending limits in provider dashboards

## Performance Tips

1. **Default to guidance mode** - free and instant
2. **Single model** - unless you need consensus
3. **Cache citations** - check CITATIONS_LOG first
4. **Targeted reviews** - not always full pipeline
5. **Pre-fix obvious** - before running expensive agents
6. **Batch operations** - combine when possible
7. **Monitor costs** - check usage_log.csv regularly

## Common Patterns

### Iterative Draft Refinement
```
Draft v1 → Guidance self-review → Fix → v2
Draft v2 → External-LLM citations → Fix → v3
Draft v3 → External-LLM opposing → Fix → v4
Draft v4 → Full pipeline → Clean pass → FINAL
```

### Evidence-Heavy Case
```
1. Convert large PDFs to images (wpd-pdf-to-images)
2. Organize evidence carefully
3. fact_verify agent checks claims against evidence
4. Update CITATIONS_LOG with evidence references
```

### Multi-Document Case
```
1. Organize all documents first
2. Read case overview materials
3. Deep research for strategy
4. Draft documents one at a time
5. Cross-reference between documents
6. Final review of entire filing package
```

## Update Commands

```bash
# Update WePublicDefender
cd ~/github/wepublic_defender  # or C:\Github\wepublic_defender
git pull origin main
pip install -e . --upgrade

# Verify update
wpd-check-env
```

## Documentation Links

- [Home](Home) - Overview and introduction
- [Complete Beginner Setup](Complete-Beginner-Setup) - Detailed setup for beginners
- [Getting Started](Getting-Started) - Quick start guide
- [Installation Guide](Installation-Guide) - Detailed installation
- [Configuration](Configuration) - Configuration options
- [Basic Usage](Basic-Usage) - Common operations
- [Session Start Automation](Session-Start-Automation) - How Claude remembers
- [File Organization](File-Organization) - Directory structure
- [Review Pipeline](Review-Pipeline) - Understanding reviews
- [Deep Research Workflow](Deep-Research-Workflow) - Comprehensive research
- [Slash Commands Reference](Slash-Commands-Reference) - All commands
- [API Reference](API-Reference) - Complete API docs
- [Advanced Features](Advanced-Features) - Power user features
- [Performance Optimization](Performance-Optimization) - Speed and cost tips
- [Integration Patterns](Integration-Patterns) - Working with other tools
- [Best Practices](Best-Practices) - Professional standards
- [Code Examples](Code-Examples) - Real-world examples
- [Migration Guides](Migration-Guides) - Upgrade instructions
- [Glossary](Glossary) - Terms and definitions
- [Troubleshooting](Troubleshooting) - Common issues
- [Cost Guide](Cost-Guide) - Pricing breakdown

## Support

- **Ask Claude**: Describe what you need in plain English
- **Documentation**: This wiki
- **GitHub Issues**: https://github.com/jackneil/wepublic_defender/issues
- **Logs**: `.wepublic_defender/logs/wpd.log`

---

**Remember:** When in doubt, just ask Claude. The system is designed for natural language interaction.

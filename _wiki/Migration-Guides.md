# Migration Guides

How to upgrade WePublicDefender and migrate between versions.

## Current Version: 1.0.0

This page documents breaking changes and migration paths between major versions of WePublicDefender.

---

## Future Migrations

As WePublicDefender evolves, migration guides will be added here for:
- Version 1.x → 2.0
- Configuration format changes
- Directory structure updates
- Agent system improvements

---

## Initial Setup Migration

### From Manual Setup → Automated Setup

**If you set up WePublicDefender before the automated setup script existed:**

#### What Changed

Old manual setup required:
1. Manually cloning repo
2. Manually creating conda environment
3. Manually installing dependencies
4. Manually creating .env files
5. Manually running init-case

New automated setup (Step 1 in README):
- Claude does all of this automatically
- One copy-paste command handles everything
- Creates per-case .wepublic_defender/env_info.json

#### Migration Steps

**Option 1: Keep existing setup (no migration needed)**

If your current setup works, you don't need to migrate. Just:
1. Update to latest version: `git pull origin main`
2. Update dependencies: `pip install -e . --upgrade`
3. Continue using as before

**Option 2: Migrate to new automated structure**

1. **Backup your current case files:**
   ```bash
   # Copy to safe location
   cp -r /path/to/your/case /path/to/backup
   ```

2. **Note your current Python path:**
   ```bash
   which python  # or `where python` on Windows
   # Save this - you'll need it
   ```

3. **Run new automated setup in case folder:**
   - Open Claude Code in your case folder
   - Paste the Step 1 automated setup from README.md
   - Let Claude set everything up

4. **Migrate your API keys:**
   - Old location: Wherever you put them
   - New location: `.env` in case folder
   - Claude will prompt you for keys during setup

5. **Verify migration:**
   ```bash
   wpd-check-env
   # Should show all green checks
   ```

---

## Configuration File Migrations

### Legal Review Settings Format

**File:** `.wepublic_defender/legal_review_settings.json`

#### v1.0.0 → Future (when changed)

Currently, the format is:
```json
{
  "reviewAgentConfig": {
    "self_review_agent": {
      "models": ["gpt-5", "grok-4"],
      "temperature": 0.3,
      "max_tokens": 8000,
      "web_search": false
    }
  }
}
```

**If format changes in future versions, migration steps will be documented here.**

### Environment Variables Migration

**File:** `.env`

#### Adding New Required Variables

**When new environment variables are added:**

1. **Check what's new:**
   ```bash
   wpd-check-env
   # Will list any missing variables
   ```

2. **Add to your .env:**
   ```bash
   # Example for new variable
   NEW_VARIABLE=your_value_here
   ```

3. **Verify:**
   ```bash
   wpd-check-env
   ```

**Current required variables (v1.0.0):**
- `OPENAI_API_KEY` (required)
- `XAI_API_KEY` (required)
- `COURTLISTENER_TOKEN` (optional but recommended)

---

## Directory Structure Migrations

### Standard Directory Structure

**Current structure (v1.0.0):**
```
00_NEW_DOCUMENTS_INBOX/
01_CASE_OVERVIEW/
02_PLEADINGS/
03_DISCOVERY/
04_EVIDENCE/
05_CORRESPONDENCE/
06_RESEARCH/
07_DRAFTS_AND_WORK_PRODUCT/
08_REFERENCE/
.wepublic_defender/
.database/
```

**If structure changes in future versions, migration will be automatic:**
- New `wpd-migrate-structure` command
- Preserves existing files
- Creates new directories
- Updates file references

---

## Agent System Migrations

### Agent Naming Changes

**If agent names change in future versions:**

**Old workflow:**
```bash
wpd-run-agent --agent old_name --file draft.md
```

**New workflow:**
```bash
wpd-run-agent --agent new_name --file draft.md
```

**Migration:** Update your scripts/workflows to use new names.

**Backward compatibility:** Old names will be aliased for 1 major version.

### Agent Mode Changes

**Current modes (v1.0.0):**
- `guidance` - Free, returns prompt for Claude Code
- `external-llm` - Calls configured LLM(s)

**If new modes are added, they'll be documented here.**

---

## API Changes

### LLM Client API

**Current API (v1.0.0):**
```python
from wepublic_defender.llm_client import LLMClient

client = LLMClient()
result = client.call_model(
    model="gpt-5",
    messages=[{"role": "user", "content": "..."}],
    temperature=0.3
)
```

**If API changes, migration guide will show:**
- What changed
- How to update your code
- Deprecation timeline
- Migration script (if available)

---

## Database Schema Migrations

### File Management Index

**File:** `.database/file_management_index.json`

**Current schema (v1.0.0):**
```json
{
  "path/to/file.pdf": {
    "processed": true,
    "timestamp": "2025-10-15T10:30:00Z",
    "action": "moved",
    "destination": "04_EVIDENCE/file.pdf"
  }
}
```

**If schema changes:**
- Automatic migration on first run of new version
- Backup created: `.database/file_management_index.json.backup`
- Migration logged to `.wepublic_defender/logs/wpd.log`

---

## Breaking Changes Log

### v1.0.0 (Current)

**Initial release - no breaking changes yet.**

### Future Breaking Changes

**When breaking changes occur, they'll be documented here with:**
- What changed
- Why it changed
- How to migrate
- Workarounds if needed
- Deprecation timeline

**Example format:**
```
### v2.0.0 (Hypothetical)

**Breaking:** Agent configuration moved from legal_review_settings.json to agents.yml

**Why:** YAML is more readable and supports comments

**Migration:**
1. Run: wpd-migrate-config
2. Verify: wpd-check-env
3. Delete old legal_review_settings.json

**Backward compatibility:** v1.x configs supported until v3.0.0
```

---

## Deprecation Policy

### How Deprecations Work

1. **Announcement:** Feature marked deprecated in release notes
2. **Grace period:** Feature continues to work for 1 major version
3. **Warnings:** System prints deprecation warnings when feature used
4. **Removal:** Feature removed in next major version

**Example timeline:**
- v1.5: Feature deprecated, warning printed
- v2.0: Feature still works, louder warning
- v3.0: Feature removed entirely

### Current Deprecations

**None as of v1.0.0**

### Upcoming Deprecations

**Check GitHub releases for announcements:**
https://github.com/jackneil/wepublic_defender/releases

---

## Upgrading WePublicDefender

### Patch Updates (1.0.0 → 1.0.1)

**What's included:**
- Bug fixes
- Security patches
- Performance improvements
- No breaking changes

**How to upgrade:**
```bash
# Pull latest code
cd /path/to/wepublic_defender/repo
git pull origin main

# Update dependencies
conda activate wepublic_defender
pip install -e . --upgrade

# Verify
wpd-check-env
```

**Downtime:** None
**Migration required:** No

### Minor Updates (1.0.0 → 1.1.0)

**What's included:**
- New features
- Agent improvements
- New commands
- Possible configuration additions

**How to upgrade:**
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -e . --upgrade

# Check for new config options
wpd-check-env

# Review release notes
cat CHANGELOG.md
```

**Downtime:** None
**Migration required:** Usually no, sometimes new config needed

### Major Updates (1.0.0 → 2.0.0)

**What's included:**
- Breaking changes
- Major new features
- Significant refactoring
- Configuration format changes

**How to upgrade:**
1. **Read migration guide** (this page, updated for that version)
2. **Backup everything:**
   ```bash
   cp -r /path/to/case /path/to/backup
   ```
3. **Follow version-specific migration steps**
4. **Test thoroughly before using on live case**

**Downtime:** Plan for 30-60 minutes
**Migration required:** Yes

---

## Migration Troubleshooting

### Common Migration Issues

#### Issue: wpd-check-env fails after upgrade

**Symptoms:**
```
ERROR: Module 'wepublic_defender' not found
```

**Solution:**
```bash
# Reinstall package
pip install -e /path/to/wepublic_defender/repo --force-reinstall

# Verify
wpd-check-env
```

#### Issue: Agents not found after upgrade

**Symptoms:**
```
ERROR: Agent 'self_review' not found
```

**Solution:**
```bash
# Check agent list
ls wepublic_defender/prompts/agent_prompts/

# Verify installation
pip show wepublic_defender
```

#### Issue: Configuration file format errors

**Symptoms:**
```
ERROR: Invalid JSON in legal_review_settings.json
```

**Solution:**
1. Check syntax: https://jsonlint.com/
2. Compare to template in repo
3. Restore from backup if needed

#### Issue: Missing API keys after migration

**Symptoms:**
```
WARNING: OPENAI_API_KEY not found
```

**Solution:**
1. Check .env file exists in case folder
2. Verify keys are present
3. Re-run `wpd-check-env` to update

### Getting Migration Help

**If migration fails:**

1. **Check logs:**
   ```bash
   cat .wepublic_defender/logs/wpd.log
   ```

2. **Search existing issues:**
   https://github.com/jackneil/wepublic_defender/issues

3. **Create new issue:**
   - Include version numbers (old and new)
   - Attach error messages
   - Describe what you tried
   - Include relevant log excerpts

4. **Ask Claude Code:**
   ```
   I'm having trouble migrating from v1.0 to v2.0. The error is [paste error]. Can you help me debug this?
   ```

---

## Rollback Procedures

### If Migration Goes Wrong

**Rollback to previous version:**

1. **Stop using new version:**
   ```bash
   cd /path/to/wepublic_defender/repo
   git log --oneline  # Find commit of old version
   ```

2. **Checkout old version:**
   ```bash
   git checkout <old-version-tag>
   # Example: git checkout v1.0.0
   ```

3. **Reinstall old version:**
   ```bash
   pip install -e . --force-reinstall
   ```

4. **Restore old config (if needed):**
   ```bash
   cp .wepublic_defender/legal_review_settings.json.backup .wepublic_defender/legal_review_settings.json
   ```

5. **Verify rollback:**
   ```bash
   wpd-check-env
   ```

### Preserve Work During Rollback

**Important:** Case files are separate from code version.

Your work is safe in:
- `00_NEW_DOCUMENTS_INBOX/` through `08_REFERENCE/`
- `.wepublic_defender/` (reviews, logs, configs)
- `GAMEPLAN.md`, session notes, timeline

**Rolling back code version does NOT delete case files.**

---

## Best Practices for Upgrades

1. **Read release notes BEFORE upgrading**
2. **Backup case folder before major upgrades**
3. **Test in non-critical case first**
4. **Upgrade during non-deadline times**
5. **Verify all features work after upgrade**
6. **Check usage logs for issues**

---

## Future Migration Topics

As WePublicDefender evolves, this guide will expand to cover:

- Multi-tenant case management migrations
- Cloud deployment migrations
- Enterprise feature migrations
- Custom agent migrations
- Integration API migrations

Check back after each major release for updated migration guides.

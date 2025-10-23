# Troubleshooting Guide

This guide helps you fix common problems with WePublicDefender. Each section includes the problem, likely causes, and step-by-step solutions.

## Quick Diagnostic

Before troubleshooting specific issues, run:
```
/check-env
```

This checks:
- Python installation
- API keys
- WePublicDefender installation
- Case initialization

## Installation Issues

### "Command not found: claude"

**Problem**: Typing `claude` gives error

**Solutions**:

1. **Claude Code not installed**:
   - Go to https://www.anthropic.com/pricing
   - Sign up for appropriate plan
   - Download and install Claude Code
   - Restart terminal

2. **PATH not updated**:
   - Close terminal completely
   - Open new terminal
   - Try again

3. **Wrong terminal**:
   - On Windows, use PowerShell or Command Prompt
   - On Mac, use Terminal
   - On Linux, use any terminal

### "No module named wepublic_defender"

**Problem**: Python can't find WePublicDefender

**Solutions**:

1. **Not installed**:
   ```
   pip install -e /path/to/wepublic_defender
   ```

2. **Wrong environment**:
   ```
   conda activate wepublic_defender
   ```

3. **Installation corrupted**:
   ```
   cd /path/to/wepublic_defender
   git pull
   pip install -e . --force-reinstall
   ```

### Python Version Errors

**Problem**: "Python 3.11+ required"

**Solutions**:

1. **Check current version**:
   ```
   python --version
   ```

2. **Install correct version**:
   - Windows: Download from python.org
   - Mac: `brew install python@3.11`
   - Linux: `sudo apt install python3.11`

3. **Use specific version**:
   ```
   python3.11 -m wepublic_defender.cli.check_env
   ```

## API Key Problems

### "API key not found"

**Problem**: Can't find API keys

**Solutions**:

1. **Check .env file exists**:
   ```
   Is there a .env file in my case folder?
   ```

2. **Create .env file**:
   ```
   Create .env file with my API keys
   ```

3. **Format issues**:
   ```
   OPENAI_API_KEY=sk-proj-...  # No quotes!
   XAI_API_KEY=xai-...         # No spaces!
   ```

### "Invalid API key"

**Problem**: API key not accepted

**Solutions**:

1. **Verify key is correct**:
   - Check for extra spaces
   - Ensure complete key copied
   - No quotes around key

2. **Test on provider website**:
   - OpenAI: https://platform.openai.com/playground
   - xAI: https://console.x.ai/

3. **Check account status**:
   - Payment method added?
   - Credits available?
   - Key not revoked?

### "Rate limit exceeded"

**Problem**: Too many API calls

**Solutions**:

1. **Wait and retry**:
   ```
   Wait 60 seconds and try again
   ```

2. **Use different model**:
   ```
   /review --model gpt-4o-mini
   ```

3. **Check usage**:
   - OpenAI: https://platform.openai.com/usage
   - xAI: https://console.x.ai/usage

## Command Issues

### Slash commands not working

**Problem**: `/organize` not recognized

**Solutions**:

1. **Restart Claude Code**:
   ```
   Press Ctrl+C
   Type: claude
   ```

2. **Reinitialize case**:
   ```
   Run wpd-init-case
   ```

3. **Check commands installed**:
   ```
   List files in .claude/commands/
   ```

### Commands hang or timeout

**Problem**: Command runs forever

**Solutions**:

1. **Check background processes**:
   ```
   /bashes
   ```

2. **Kill stuck process**:
   ```
   Press Ctrl+C
   ```

3. **Check API status**:
   - OpenAI status: https://status.openai.com/
   - xAI status: Check Twitter/X

## File and Path Issues

### "File not found"

**Problem**: Can't find documents

**Solutions**:

1. **Check current directory**:
   ```
   What folder am I in?
   ```

2. **Use full paths**:
   ```
   /review C:/Users/Me/Case/draft.md
   ```

3. **Check file exists**:
   ```
   List files in 07_DRAFTS_AND_WORK_PRODUCT/
   ```

### "Permission denied"

**Problem**: Can't read/write files

**Solutions**:

1. **Windows - Run as admin**:
   - Right-click PowerShell
   - Run as Administrator

2. **Mac/Linux - Use sudo**:
   ```
   sudo wpd-init-case
   ```

3. **Check file ownership**:
   ```
   Who owns these files?
   ```

### Path separator issues

**Problem**: Paths not working on Windows

**Solutions**:

1. **Use forward slashes in commands**:
   ```
   /review C:/Users/Me/Case/draft.md
   ```

2. **Let Claude handle paths**:
   ```
   Review the draft in my drafts folder
   ```

## Review Pipeline Issues

### Review takes too long

**Problem**: Review running 10+ minutes

**Solutions**:

1. **Check if still running**:
   ```
   /bashes
   ```

2. **Large document**:
   - Break into sections
   - Review separately

3. **Web search enabled**:
   - Takes longer with web search
   - Normal: 3-5 minutes
   - Disable if not needed

### Review costs too much

**Problem**: Single review costs $20+

**Solutions**:

1. **Use guidance mode first**:
   ```
   /review draft.md --mode guidance
   ```

2. **Use single model**:
   ```
   /review draft.md --model gpt-4o-mini
   ```

3. **Break document up**:
   - Review sections separately
   - Focus on critical parts

### Different AIs disagree completely

**Problem**: No consensus on issues

**Solutions**:

1. **Document needs rewrite**:
   - Major structural issues
   - Start fresh

2. **Check document format**:
   - Is it readable?
   - Proper markdown?

3. **Get human help**:
   - Some issues need real lawyer

## Organization Issues

### Files won't organize

**Problem**: `/organize` not moving files

**Solutions**:

1. **Check inbox has files**:
   ```
   List files in 00_NEW_DOCUMENTS_INBOX/
   ```

2. **Files already organized**:
   - Check `.database/file_management_index.json`
   - System won't move twice

3. **Reset organization**:
   ```
   Reset file organization tracking and try again
   ```

### Files in wrong folders

**Problem**: Documents misplaced

**Solutions**:

1. **Move manually**:
   ```
   Move contract.pdf from inbox to 04_EVIDENCE/contracts/
   ```

2. **Rename for clarity**:
   ```
   Rename to: 2025-10-15_Employment_Contract.pdf
   ```

3. **Re-organize everything**:
   ```
   Reset organization and start over
   ```

## Session and Memory Issues

### Claude doesn't remember case

**Problem**: Asks for info repeatedly

**Solutions**:

1. **Refresh context**:
   ```
   /start
   ```

2. **Check tracking files**:
   ```
   Show me session_notes.md
   ```

3. **Long session**:
   - Restart Claude Code
   - Context gets stale

### Lost work after crash

**Problem**: Claude crashed mid-task

**Solutions**:

1. **Check session notes**:
   ```
   What was I working on? Check session notes.
   ```

2. **Check auto-saves**:
   - Reviews saved in `.wepublic_defender/reviews/`
   - Drafts in `07_DRAFTS_AND_WORK_PRODUCT/`

3. **Recovery mode**:
   ```
   Recover from crash and continue where I left off
   ```

## Cost and Usage Issues

### Can't track spending

**Problem**: Don't know costs

**Solutions**:

1. **Check usage log**:
   ```
   Show me today's API usage
   ```

2. **View usage file**:
   ```
   Open .wepublic_defender/usage_log.csv
   ```

3. **Provider dashboards**:
   - OpenAI: https://platform.openai.com/usage
   - xAI: https://console.x.ai/usage

### Hitting spending limits

**Problem**: API calls rejected

**Solutions**:

1. **Increase limits**:
   - OpenAI: Settings → Billing → Limits
   - Add more credits

2. **Use cheaper models**:
   ```
   Switch to gpt-4o-mini for reviews
   ```

3. **Use guidance mode**:
   ```
   All commands in guidance mode (free)
   ```

## Platform-Specific Issues

### Windows Issues

#### PowerShell execution policy

**Problem**: Scripts won't run

**Solution**:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Unicode characters crash

**Problem**: Special characters cause errors

**Solution**:
- Avoid emojis in documents
- Use plain text
- Stick to ASCII characters

### Mac Issues

#### Conda not found

**Problem**: conda commands fail

**Solution**:
```bash
echo 'export PATH="/opt/miniconda3/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Permission errors

**Problem**: Can't install packages

**Solution**:
```bash
sudo chown -R $(whoami) ~/github
```

### Linux Issues

#### Python version conflicts

**Problem**: System Python interfering

**Solution**:
```bash
# Use virtual environment
python3.11 -m venv ~/wpd_env
source ~/wpd_env/bin/activate
```

## Getting Help

### Self-Help First

1. **Run diagnostic**:
   ```
   /check-env
   ```

2. **Check the logs**:
   ```
   Show me the error in .wepublic_defender/logs/wpd.log
   ```

3. **Ask Claude**:
   ```
   I'm getting this error: [paste error]
   ```

### When to Get Human Help

Get human help when:
- Installation completely fails
- API keys confirmed correct but still failing
- Claude Code won't start at all
- File system corruption
- Losing money to failed API calls

### How to Report Issues

When reporting issues:

1. **Include environment info**:
   ```
   /check-env output
   ```

2. **Include error message**:
   - Complete error text
   - What you were doing
   - What file you were working on

3. **Include versions**:
   - Claude Code version
   - Python version
   - Operating system

### GitHub Issues

File issue at: https://github.com/jackneil/wepublic_defender/issues

Include:
- Problem description
- Steps to reproduce
- Error messages
- Environment info

## Prevention Tips

### Regular Maintenance

1. **Update regularly**:
   ```
   Update WePublicDefender to latest version
   ```

2. **Check environment**:
   ```
   Weekly: /check-env
   ```

3. **Clean up**:
   ```
   Archive old drafts
   Empty large inbox folders
   ```

### Best Practices

1. **Save versions**: Don't overwrite, create new versions
2. **Regular breaks**: Restart Claude Code every few hours
3. **Monitor costs**: Check usage daily
4. **Backup work**: Keep copies of important documents

## Emergency Recovery

### If everything breaks:

1. **Save your case files** (most important!)

2. **Fresh start**:
   ```
   Create new case folder
   Copy documents over
   Re-run setup
   ```

3. **Reinstall**:
   ```
   Uninstall and reinstall WePublicDefender
   ```

4. **Get help**:
   - File GitHub issue
   - Check if others have same problem
   - Wait for fix

Remember: Your documents are safe even if the system breaks. The worst case is you have to reinstall - your case files remain untouched.

## Next Steps

- Return to [Getting Started](Getting-Started)
- Check [Installation Guide](Installation-Guide)
- Review [Configuration](Configuration)
- See [Cost Guide](Cost-Guide)
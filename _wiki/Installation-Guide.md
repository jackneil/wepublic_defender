# Installation Guide

This guide provides detailed installation instructions for WePublicDefender across different operating systems and scenarios.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Install (Copy-Paste Method)](#quick-install-copy-paste-method)
3. [Manual Installation](#manual-installation)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Environment Setup](#environment-setup)
6. [API Configuration](#api-configuration)
7. [Verification](#verification)
8. [Updating WePublicDefender](#updating-wepublic_defender)
9. [Uninstallation](#uninstallation)
10. [Troubleshooting Installation](#troubleshooting-installation)

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Required for AI API calls
- **Python**: 3.11 or higher (installed automatically)

### Required Accounts

- **Claude Code**: Subscription (Max 5x or higher recommended)
- **OpenAI**: Account with API access
- **xAI**: Account with API access
- **CourtListener**: Optional but recommended

## Quick Install (Copy-Paste Method)

The easiest way to install is using the automated setup command.

### Step 1: Open Terminal in Case Folder

Create a folder for your case and open a terminal there:

**Windows**:
- Create folder (e.g., `C:\Users\You\Desktop\MyCase`)
- Open File Explorer to that folder
- Click address bar, type `cmd`, press Enter

**Mac/Linux**:
- Create folder (e.g., `~/Desktop/MyCase`)
- Open Terminal
- Type `cd ~/Desktop/MyCase`

### Step 2: Start Claude Code

```bash
claude
```

### Step 3: Paste Setup Command

Copy and paste this entire command into Claude:

```
You are my coding assistant. Please perform a central setup for WePublicDefender that I can reuse across cases.

1) Create a stable base folder if missing and print it when done:
   - Windows: C:/Github
   - macOS:  ~/github
   - Linux:  ~/github

2) Check and install prerequisites automatically (do NOT ask me to install anything):
   - Verify Git and Python 3.11+; if missing, install them using the appropriate method for my OS.
   - If `conda` is not available, install Miniconda silently.
   - Print versions for confirmation.

3) Clone or update the repository:
   - Repo URL: https://github.com/jackneil/wepublic_defender.git
   - Target: <BASE_DIR>/wepublic_defender
   - If missing: git clone
   - If present: pull latest main

4) Create a Python environment named "wepublic_defender" (Conda preferred). Then install the package:
   - pip install -e <BASE_DIR>/wepublic_defender

5) Run environment check and handle any missing tools/packages:
   - Command: wpd-check-env

6) Collect my API keys and save them to a reusable template:
   - Prompt for OpenAI, xAI, and CourtListener keys
   - Create .env file with keys

7) Initialize THIS case and prepare guidance:
   - Run: wpd-init-case
   - Create standard directories
   - Copy configuration files

8) Save paths for reuse:
   - Store Python path and repo location
   - Save to .wepublic_defender/env_info.json

9) Tell me to restart Claude Code for commands to work
```

### Step 4: Follow Prompts

Claude will:
- Install all requirements
- Ask for your API keys
- Set up your case folder
- Tell you to restart

### Step 5: Restart Claude Code

Press Ctrl+C (or Cmd+C on Mac), then type `claude` again.

## Manual Installation

For users who prefer manual control or when automated setup fails.

### Step 1: Install Prerequisites

#### Python 3.11+

**Windows**:
```powershell
# Download from python.org
# Or use winget:
winget install Python.Python.3.11
```

**Mac**:
```bash
# Using Homebrew:
brew install python@3.11
```

**Linux**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

#### Git

**Windows**:
```powershell
winget install Git.Git
```

**Mac**:
```bash
brew install git
```

**Linux**:
```bash
sudo apt install git
```

### Step 2: Clone Repository

```bash
# Create base directory
mkdir -p ~/github  # Mac/Linux
# or
mkdir C:\Github    # Windows

# Clone repository
cd ~/github  # or C:\Github on Windows
git clone https://github.com/jackneil/wepublic_defender.git
```

### Step 3: Create Python Environment

Using Conda (recommended):
```bash
conda create -n wepublic_defender python=3.11
conda activate wepublic_defender
```

Using venv:
```bash
python3.11 -m venv wpd_env
source wpd_env/bin/activate  # Mac/Linux
# or
wpd_env\Scripts\activate     # Windows
```

### Step 4: Install Package

```bash
cd wepublic_defender
pip install -e .
```

### Step 5: Initialize Case

```bash
cd /path/to/your/case
wpd-init-case
```

## Platform-Specific Instructions

### Windows

#### Using PowerShell

1. **Open PowerShell as Administrator**:
   - Right-click Start button
   - Select "Windows PowerShell (Admin)"

2. **Allow script execution**:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install Chocolatey (package manager)**:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

4. **Install dependencies**:
   ```powershell
   choco install python git miniconda3 -y
   ```

#### Path Issues on Windows

If commands aren't found:
1. Close all terminals
2. Restart computer
3. Check PATH environment variable includes Python and Conda

### macOS

#### Using Homebrew

1. **Install Homebrew**:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**:
   ```bash
   brew install python@3.11 git
   brew install --cask miniconda
   ```

3. **Initialize Conda**:
   ```bash
   conda init zsh  # or bash if using bash
   ```

#### Permission Issues on Mac

If you get permission errors:
```bash
sudo chown -R $(whoami) ~/github
```

### Linux (Ubuntu/Debian)

#### Package Installation

```bash
# Update package list
sudo apt update

# Install Python and Git
sudo apt install python3.11 python3.11-venv git

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

## Environment Setup

### Creating the Environment

The environment isolates WePublicDefender's dependencies from your system.

#### Option 1: Conda (Recommended)

```bash
conda create -n wepublic_defender python=3.11
conda activate wepublic_defender
```

#### Option 2: venv

```bash
python3.11 -m venv ~/wpd_env
source ~/wpd_env/bin/activate  # Mac/Linux
```

### Installing Dependencies

```bash
pip install -e /path/to/wepublic_defender
```

### Saving Environment Info

Create `.wepublic_defender/env_info.json`:
```json
{
  "python_exe": "/path/to/python",
  "conda_env": "wepublic_defender",
  "repo_path": "/path/to/wepublic_defender"
}
```

## API Configuration

### Creating .env File

In your case folder, create `.env`:

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-...your-key-here...

# xAI Grok
XAI_API_KEY=xai-...your-key-here...

# CourtListener (optional)
COURTLISTENER_TOKEN=...your-token...
COURTLISTENER_USER_AGENT=WePublicDefender/1.0
```

### Getting API Keys

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Add payment method in Billing

#### xAI
1. Go to https://console.x.ai/
2. Create API key
3. Add payment method

#### CourtListener
1. Go to https://www.courtlistener.com/api/
2. Register for free account
3. Get API token

### Testing API Keys

```bash
wpd-check-env
```

This verifies all keys are working.

## Verification

### Check Installation

Run these commands to verify everything works:

```bash
# Check environment
wpd-check-env

# Check Python
python --version

# Check Git
git --version

# Check WePublicDefender
python -m wepublic_defender.cli.check_env
```

### Test Basic Functionality

```bash
# Initialize case
wpd-init-case

# Check organization
wpd-run-agent --agent organize --mode guidance
```

## Updating WePublicDefender

### Automatic Update

In Claude Code:
```
Update WePublicDefender to latest version
```

### Manual Update

```bash
cd ~/github/wepublic_defender  # or C:\Github\wepublic_defender
git pull origin main
pip install -e . --upgrade
```

## Uninstallation

### Remove WePublicDefender

```bash
# Uninstall package
pip uninstall wepublic_defender

# Remove repository
rm -rf ~/github/wepublic_defender  # Mac/Linux
# or
rmdir /s C:\Github\wepublic_defender  # Windows

# Remove environment
conda env remove -n wepublic_defender
```

### Keep Case Files

Your case files in your case folder are not affected by uninstallation.

## Troubleshooting Installation

### "Command not found"

**Problem**: Commands like `wpd-check-env` not found

**Solutions**:
1. Ensure environment is activated
2. Reinstall with `pip install -e .`
3. Check PATH includes Python scripts directory

### "Permission denied"

**Problem**: Can't install or write files

**Solutions**:
- Windows: Run as Administrator
- Mac/Linux: Use `sudo` for system-wide install
- Install in user directory instead

### "Python version error"

**Problem**: Wrong Python version

**Solutions**:
1. Install Python 3.11+
2. Use `python3.11` explicitly
3. Update conda environment

### "Git not found"

**Problem**: Git commands fail

**Solutions**:
1. Install Git for your OS
2. Restart terminal after installation
3. Add Git to PATH

### API Key Errors

**Problem**: API keys not working

**Solutions**:
1. Check `.env` file format
2. Verify keys are correct (no extra spaces)
3. Ensure accounts have credit
4. Test keys on provider websites

### Conda Issues

**Problem**: Conda commands not working

**Solutions**:
1. Run `conda init` for your shell
2. Restart terminal
3. Reinstall Miniconda

## Getting Help

If installation fails:

1. **Check error messages** - They often explain the problem
2. **Ask Claude** - Describe the error in Claude Code
3. **Check GitHub Issues** - Others may have had same problem
4. **File new issue** - Include your OS and error messages

Remember: Installation is the hardest part. Once it's working, everything else is easier!

## Next Steps

After successful installation:
1. Read [Getting Started](Getting-Started)
2. Learn about [Session Start Automation](Session-Start-Automation)
3. Understand [File Organization](File-Organization)
4. Try the [Basic Usage](Basic-Usage) examples
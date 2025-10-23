# Complete Beginner Setup Guide

This guide assumes you know nothing about programming, terminals, or command lines. We'll walk through everything step by step, explaining what each thing does and why you need it.

## Table of Contents

1. [What You're About to Install](#what-youre-about-to-install)
2. [Step 1: Get Claude Code](#step-1-get-claude-code)
3. [Step 2: Understanding the Terminal](#step-2-understanding-the-terminal)
4. [Step 3: Create Your Case Folder](#step-3-create-your-case-folder)
5. [Step 4: Open Terminal in Your Case Folder](#step-4-open-terminal-in-your-case-folder)
6. [Step 5: Start Claude Code](#step-5-start-claude-code)
7. [Step 6: The Magic Setup Command](#step-6-the-magic-setup-command)
8. [Step 7: Getting API Keys](#step-7-getting-api-keys)
9. [Step 8: Restart Claude Code](#step-8-restart-claude-code)
10. [Common Mistakes and How to Fix Them](#common-mistakes-and-how-to-fix-them)
11. [What Success Looks Like](#what-success-looks-like)
12. [Your First Steps After Setup](#your-first-steps-after-setup)

---

## What You're About to Install

Before we start, let's understand what you're installing:

1. **Claude Code** - This is like Microsoft Word, but for talking to AI. You type commands, Claude (the AI) does stuff for you.

2. **WePublicDefender** - This is the legal assistant software that helps with your case.

3. **API Keys** - These are like passwords that let the software talk to different AI companies (OpenAI, xAI, etc).

Think of it like setting up a new phone - you need the phone (Claude Code), the apps (WePublicDefender), and your accounts (API keys).

---

## Step 1: Get Claude Code

### What is Claude Code?

Claude Code is a program made by Anthropic (the AI company) that lets you talk to their AI assistant Claude in a more powerful way than just using the website. It's like the difference between texting someone vs having them actually help you organize your files.

### Getting Claude Code

1. **Go to Anthropic's pricing page**: https://www.anthropic.com/pricing

2. **Choose a plan**:
   - **Claude Pro** ($20/month) - Might work for simple cases
   - **Claude Max 5x** (~$100/month) - Good for most cases
   - **Claude Max 20x** (~$200/month) - For complex cases with lots of documents

   **Which one?** If your case has less than 50 documents and you won't use it all day, start with Max 5x.

3. **Sign up and pay** - Yes, this costs money. But one hour with a lawyer costs more than a whole month of this.

4. **Install Claude Code**:
   - After signing up, you'll get instructions to install Claude Code
   - Download the installer for your computer (Windows, Mac, or Linux)
   - Run the installer - just click "Next" on everything
   - It will install like any other program

5. **Sign in to Claude Code**:
   - Open Claude Code (look for it in your Start Menu or Applications)
   - It will ask you to sign in
   - Use the same email/password you used when signing up

---

## Step 2: Understanding the Terminal

### What is a Terminal?

A terminal (also called command prompt or PowerShell on Windows) is a text-based way to control your computer. Instead of clicking on things, you type commands.

Think of it like texting your computer instructions instead of pointing at things.

### Why Do We Need It?

Claude Code works through the terminal. When you type something in the terminal while Claude Code is running, Claude sees it and can respond or take action.

### How to Open a Terminal

**On Windows:**
1. Press the Windows key (the one with the Windows logo)
2. Type "PowerShell"
3. Click on "Windows PowerShell" when it appears
4. A black or blue window will open with text

**On Mac:**
1. Press Command + Space (opens Spotlight search)
2. Type "Terminal"
3. Press Enter
4. A white or black window will open with text

**On Linux:**
- Right-click on your desktop and select "Open Terminal"
- Or press Ctrl + Alt + T

### What Does a Terminal Look Like?

It's a window with text that looks something like this:

**Windows:**
```
PS C:\Users\YourName>
```

**Mac/Linux:**
```
YourName@YourComputer:~$
```

This is called the "prompt" - it's waiting for you to type something.

---

## Step 3: Create Your Case Folder

### What is a Case Folder?

This is a regular folder on your computer where you'll keep all your case files - your evidence, drafts, research, everything.

### Creating Your Case Folder

1. **Open File Explorer** (Windows) or **Finder** (Mac)

2. **Go to your Desktop** (or wherever you want to keep your case)

3. **Right-click in an empty space**

4. **Select "New Folder"** (Windows) or **"New Folder"** (Mac)

5. **Name it something memorable** like:
   - `CapitalOneCase`
   - `MyLegalCase`
   - `JohnsonVsAcmeCorp`

   **Important**: Don't use spaces! Use `CapitalOneCase` not `Capital One Case`

6. **Put ALL your case documents in this folder**:
   - Contracts
   - Emails
   - Letters
   - Evidence
   - Everything related to your case

---

## Step 4: Open Terminal in Your Case Folder

This is the trickiest part for beginners, but I'll make it easy.

### On Windows (Easiest Method)

1. **Open File Explorer**
2. **Navigate to your case folder** (the one you just created)
3. **Click on the address bar** (where it shows the path like `C:\Users\YourName\Desktop\CapitalOneCase`)
4. **Type `cmd` and press Enter**
5. A black terminal window opens already in your case folder!

### On Windows (Alternative Method)

1. **Open PowerShell** (Windows key, type "PowerShell", press Enter)
2. **Type this command** (replace with your actual folder path):
   ```
   cd C:\Users\YourName\Desktop\CapitalOneCase
   ```
3. **Press Enter**

### On Mac

1. **Open Terminal** (Command + Space, type "Terminal", press Enter)
2. **Type `cd ` (with a space after cd)**
3. **Drag your case folder from Finder into the Terminal window**
4. **Press Enter**

### How to Know You're in the Right Place

After doing this, your terminal should show your case folder name somewhere in the prompt:

**Windows:**
```
C:\Users\YourName\Desktop\CapitalOneCase>
```

**Mac:**
```
YourName@Mac:~/Desktop/CapitalOneCase$
```

If you see your case folder name, you're in the right place!

---

## Step 5: Start Claude Code

Now that your terminal is in your case folder, let's start Claude Code.

1. **In the terminal, type**:
   ```
   claude
   ```

2. **Press Enter**

3. **You should see** something like:
   ```
   Claude Code v1.0.0
   Ready to assist you
   >
   ```

If you see an error like "command not found", Claude Code isn't installed properly. Go back to Step 1.

---

## Step 6: The Magic Setup Command

This is where the magic happens. You're going to copy and paste one big command that sets up everything automatically.

### The Setup Command

1. **Copy this entire block** (select it all and press Ctrl+C or Cmd+C):

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
   - If missing: git clone https://github.com/jackneil/wepublic_defender.git <BASE_DIR>/wepublic_defender
   - If present: pull latest main

4) Create a Python environment named "wepublic_defender" (Conda preferred; install Miniconda first if needed). If Conda is not possible, use a local venv in the repo. Then install the package:
   - pip install -e <BASE_DIR>/wepublic_defender

5) Run environment check from the repo root and handle any missing tools/packages:
   - Command: wpd-check-env

6) Collect my API keys and save them to a reusable template (don't ask me to set environment variables):
   - Show me these links to create keys if I need them:
     • OpenAI: https://platform.openai.com/api-keys
     • xAI Grok: https://console.x.ai/
     • CourtListener (optional): https://www.courtlistener.com/api/
   - Prompt me to paste values, then write a starter .env template we can reuse for cases with:
     OPENAI_API_KEY=...
     XAI_API_KEY=...
     COURTLISTENER_TOKEN=... (optional)

7) Initialize THIS case (the folder where my terminal is open) and prepare guidance:
   - Run: wpd-init-case in the current working directory (do not create a new folder)
   - Ensure standard directories exist and .wepublic_defender/ is created
   - Copy CLAUDE.md and LEGAL_WORK_PROTOCOL.md into this case folder
   - Copy default per-case settings into .wepublic_defender/
   - If a .env is missing here, help me create it by reusing the keys you collected

8) Tell me clearly what to do next, pointing to CLAUDE.md:
   - "Open CLAUDE.md in this folder and follow it step-by-step to organize your case files (it includes the init/checklists). When done, come back here to run reviews."

9) Persist paths so I don't have to copy anything:
   - Store the absolute path to the created environment's Python executable and env name
   - Store the central repo path you cloned
   - Save these to .wepublic_defender/env_info.json in this case folder with keys:
     { "python_exe": "...", "conda_env": "...", "repo_path": "..." }

10) After setup completes, tell me to RESTART Claude Code:
   - The init command installs slash commands to .claude/commands/
   - Claude Code only loads commands at startup, not during a session
   - Tell me: "Exit Claude Code (Ctrl+C) and run 'claude' again in this folder"
   - After restart, commands like /deep-research-prep will work
```

2. **Paste it into Claude Code** (right-click in the terminal or press Ctrl+V or Cmd+V)

3. **Press Enter**

### What Happens Next

Claude will now:
- Install Python (programming language needed for WePublicDefender)
- Install Git (tool for downloading code)
- Download WePublicDefender
- Set up all the folders
- Ask you for API keys (we'll cover this next)

This will take 5-10 minutes. You'll see a lot of text scrolling by - that's normal!

---

## Step 7: Getting API Keys

During setup, Claude will ask you for API keys. These are like passwords that let WePublicDefender talk to different AI services.

### What are API Keys?

Think of API keys like your Netflix password - they let the software use AI services that cost money. Each AI company has their own key.

### Getting Your API Keys

You need at least 2 keys (OpenAI and xAI). The third one (CourtListener) is optional but helpful.

#### OpenAI Key (Required)

1. **Go to**: https://platform.openai.com/api-keys
2. **Sign up or log in** (you can use Google/Microsoft/Apple to sign up)
3. **Click "Create new secret key"**
4. **Give it a name** like "WePublicDefender"
5. **Copy the key** - it looks like `sk-proj-abc123...` (very long)
6. **IMPORTANT**: Save this somewhere safe! You can't see it again!
7. **Add payment method**:
   - Go to Billing
   - Add a credit card
   - Set a monthly budget of $50 (you probably won't use this much)

#### xAI Grok Key (Required)

1. **Go to**: https://console.x.ai/
2. **Sign up** (you might need a Twitter/X account)
3. **Create an API key**
4. **Copy the key**
5. **Add payment method** (similar to OpenAI)

#### CourtListener Key (Optional but Recommended)

1. **Go to**: https://www.courtlistener.com/api/
2. **Create a free account**
3. **Get your API token**
4. **Copy the token**

### Entering Your Keys

When Claude asks for keys during setup:

1. **Claude will say** something like "Please paste your OpenAI API key:"
2. **Paste your key** (right-click or Ctrl+V)
3. **Press Enter**
4. **Repeat for each key**

If you don't have a key yet, just press Enter to skip it. You can add it later.

---

## Step 8: Restart Claude Code

After setup completes, Claude will tell you to restart. This is important!

### How to Restart

1. **Press Ctrl+C** (Windows/Linux) or **Cmd+C** (Mac)
   - This stops Claude Code

2. **Type `claude` again**

3. **Press Enter**
   - Claude Code starts fresh with everything loaded

### Why Restart?

Claude Code loads special commands at startup. The setup installed new commands (like `/organize` and `/review`). Without restarting, these commands won't work.

---

## Common Mistakes and How to Fix Them

### "Command not found" Errors

**Problem**: When you type `claude` or other commands, it says "command not found"

**Solution**:
- Claude Code isn't installed or isn't in your PATH
- Try closing and reopening your terminal
- On Windows, try restarting your computer
- Reinstall Claude Code if needed

### "Permission denied" Errors

**Problem**: Getting errors about permissions

**Solution**:
- On Windows: Run PowerShell as Administrator (right-click, "Run as administrator")
- On Mac/Linux: Add `sudo` before commands (it will ask for your password)

### API Key Errors

**Problem**: "Invalid API key" or "Authentication failed"

**Solution**:
- You copied the key wrong (missed some characters)
- The key expired or was revoked
- You haven't added payment method to your OpenAI/xAI account
- Create a new key and try again

### Can't Find Your Case Folder

**Problem**: Terminal is in the wrong folder

**Solution**:
- Type `pwd` (Mac/Linux) or `cd` (Windows) to see where you are
- Navigate to your case folder using the `cd` command
- Or close terminal and start over with Step 4

### Claude Code Won't Start

**Problem**: Typing `claude` does nothing or gives an error

**Solution**:
- Make sure you're logged in to Claude Code
- Check your subscription is active
- Reinstall Claude Code
- Contact Anthropic support

---

## What Success Looks Like

When everything is set up correctly:

1. **Your terminal** shows you're in your case folder:
   ```
   C:\Users\You\Desktop\YourCase>
   ```

2. **Claude Code is running**:
   ```
   Claude Code v1.0.0
   Ready to assist
   >
   ```

3. **You can use commands** like:
   ```
   /check-env
   ```
   And Claude responds with information about your setup

4. **Your case folder** has these new folders:
   - `00_NEW_DOCUMENTS_INBOX/`
   - `01_CASE_OVERVIEW/`
   - `02_PLEADINGS/`
   - And several more...

5. **Hidden folders** (you might not see these normally):
   - `.wepublic_defender/` (configuration)
   - `.claude/` (Claude's commands)

---

## Your First Steps After Setup

Congratulations! You've set up WePublicDefender. Here's what to do next:

### 1. Put Your Documents in the Inbox

Move ALL your case documents into the `00_NEW_DOCUMENTS_INBOX/` folder:
- Contracts
- Emails
- Court documents
- Evidence
- Everything!

### 2. Ask Claude to Organize

In Claude Code, type:
```
/organize
```

Claude will sort all your documents into the right folders automatically.

### 3. Get Initial Strategy

Type:
```
/strategy
```

Claude will analyze your case and suggest next steps.

### 4. Start Your Deep Research

Type:
```
/deep-research-prep
```

Claude will create a research prompt. Follow the instructions to get comprehensive legal research.

---

## Getting Help

### If Something Goes Wrong

1. **First**: Type `/check-env` to see if everything is set up
2. **Second**: Check the [Troubleshooting](Troubleshooting) page
3. **Third**: Ask Claude - just describe your problem in plain English
4. **Last Resort**: Create an issue on GitHub (Claude can help you do this)

### Remember

- It's okay to make mistakes - you can't break anything permanently
- Claude is there to help - just ask if you're confused
- The more you use it, the easier it gets
- You're doing something very technical - be patient with yourself

---

## What's Next?

Now that you're set up:
1. Read [Getting Started](Getting-Started) for a quicker overview
2. Learn about [Session Start Automation](Session-Start-Automation)
3. Understand the [Review Pipeline](Review-Pipeline)
4. Check out [Slash Commands Reference](Slash-Commands-Reference)

**Most importantly**: Start using it! The best way to learn is by doing.

---

**You did it!** You've successfully set up a sophisticated legal AI system. That wasn't so hard, was it? Now go fight those corporations!
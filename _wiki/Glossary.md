# Glossary

Technical and legal terms used in WePublicDefender documentation, explained in plain English.

## A

**Agent**
: A specialized AI module that performs specific tasks (review, drafting, organizing). Think of it as a specialist lawyer - one focuses on citations, another on strategy.

**API (Application Programming Interface)**
: How different software programs talk to each other. Your API keys let WePublicDefender talk to OpenAI and other AI services.

**API Key**
: A password that lets WePublicDefender use AI services. Like a Netflix password, but for AI.

**Arbitration Clause**
: A contract term requiring disputes to be resolved by arbitration instead of court. Often a barrier to lawsuits.

## B

**Backoff**
: Waiting progressively longer between retries when something fails. Like knocking on a door, waiting, then waiting longer before knocking again.

**Bash**
: The command-line shell used in terminals. The black window where you type commands.

**Brief**
: A written legal argument submitted to court. Despite the name, rarely brief.

## C

**Case Folder**
: The directory on your computer containing all files for one legal case.

**Citation**
: Reference to a legal authority (case, statute, rule). Format: *Smith v. Jones*, 123 F.3d 456 (4th Cir. 2019).

**Citation Verification**
: Checking that legal citations are still valid law and haven't been overruled.

**CLI (Command Line Interface)**
: Text-based way to control software. Type commands instead of clicking buttons.

**Claude**
: The AI assistant made by Anthropic that powers WePublicDefender's orchestration.

**Claude Code**
: Anthropic's desktop application that lets Claude interact with your files and run commands.

**Complaint**
: The document that starts a lawsuit, stating your claims against the defendant.

**Consensus**
: When multiple AI models agree on an issue. Higher consensus = higher confidence.

**CourtListener**
: Free legal database API for verifying citations and finding cases.

## D

**Deep Research**
: Comprehensive legal research using Claude.ai that performs 50+ web searches automatically.

**Defendant**
: The party being sued (person or company you're taking to court).

**Discovery**
: Pre-trial phase where parties exchange information and evidence.

**Draft**
: Working version of a document, not yet final.

## E

**Environment**
: The Python setup where WePublicDefender runs. Like a workspace for the software.

**Evidence Folder** (`04_EVIDENCE/`)
: Where all your evidence documents are stored - contracts, emails, photos, etc.

**External-LLM Mode**
: Running actual AI models (costs money). As opposed to guidance mode (free).

## F

**Fact Verification**
: Checking that claims in your document match the evidence you have.

**Federal Court**
: U.S. court system handling federal law, constitutional issues, and disputes between states.

**Filing**
: Officially submitting a document to the court.

## G

**Git**
: Version control system used to download and update WePublicDefender.

**GPT (Generative Pre-trained Transformer)**
: OpenAI's AI model family (GPT-4, GPT-5, etc.).

**Grok**
: xAI's AI model with real-time web access.

**Guidance Mode**
: Free mode that gives you instructions instead of running AI. Like a checklist instead of automation.

## H

**Hook**
: Code that runs automatically when something happens (like when Claude Code starts).

## I

**Inbox** (`00_NEW_DOCUMENTS_INBOX/`)
: Folder where you drop new documents before organizing them.

**Interrogatories**
: Written questions one party sends to another during discovery.

**Iteration**
: One round of review and fixes. Pipeline often takes 2-3 iterations to get clean.

## J

**JSON**
: File format for configuration. Looks like: `{"key": "value"}`.

**Jurisdiction**
: Court's authority to hear a case. Also refers to which court/circuit/state.

## L

**Legal Standard**
: The rule or test the court applies. Example: "12(b)(6) motion to dismiss standard."

**LLM (Large Language Model)**
: The AI technology behind ChatGPT, Claude, etc. The "brain" doing the thinking.

**Local Rules**
: Specific rules for a particular court beyond federal/state rules.

## M

**Markdown (.md)**
: Simple text format for documents. Uses * for bullets, # for headings.

**Migration**
: Moving from one version to another or transferring data between systems.

**Motion**
: Formal request to the court for a ruling or order.

**Motion to Dismiss**
: Request to throw out a case without trial, usually for legal deficiency.

## N

**Node**
: A point in the system or network. Often refers to a step in the pipeline.

## O

**Opposing Counsel**
: The other side's lawyer. Also an agent that simulates their attacks.

**Organization**
: Sorting documents into proper folders automatically.

## P

**PATH**
: List of folders your computer checks when you type a command.

**Pipeline**
: Series of review stages run in sequence. Like an assembly line for document review.

**Plaintiff**
: The party bringing the lawsuit (usually you if using WePublicDefender).

**Pleadings**
: Formal documents filed with court stating claims and defenses.

**PowerShell**
: Windows command-line interface. The terminal on Windows.

**Prompt**
: Instructions given to AI. The text you send to get AI to do something.

**Pro Se**
: Representing yourself without a lawyer (Latin: "for oneself").

**Python**
: Programming language WePublicDefender is built with.

## Q

**Qualified Immunity**
: Legal doctrine protecting government officials from lawsuits unless they violated clearly established law.

## R

**Repository (Repo)**
: Storage location for code. WePublicDefender's repo is on GitHub.

**Review Pipeline**
: Multi-stage document review process with different AI models.

## S

**Session**
: One continuous period of work in Claude Code.

**Session Notes**
: File tracking what you're working on, used for crash recovery.

**Slash Command**
: Commands starting with / that trigger specific actions (like /organize).

**State Court**
: Court system for state law issues (contracts, state crimes, etc.).

**Summary Judgment**
: Request for court to rule without trial based on undisputed facts.

## T

**Terminal**
: Text-based interface for controlling your computer. The black window with text.

**Token**
: Unit of text for AI processing. Roughly 4 characters or 0.75 words.

**Tracking Files**
: Files that remember your case progress and work history.

## U

**Unicode**
: Character encoding that includes emojis and special characters. Can cause issues on Windows.

## V

**Venue**
: Specific court location where case is filed.

**Version Control**
: System for tracking changes to files over time.

**Virtual Environment**
: Isolated Python installation for one project. Keeps WePublicDefender separate from other Python programs.

## W

**Web Search**
: AI's ability to search the internet for current information.

**Working Directory**
: The folder your terminal is currently "in". Where commands execute.

## Legal Terms

**Burden of Proof**
: What you must prove to win. In civil cases, usually "preponderance of evidence" (more likely than not).

**Cause of Action**
: Legal theory giving you the right to sue.

**Damages**
: Money awarded for harm suffered.

**Due Process**
: Constitutional right to fair legal proceedings.

**Injunction**
: Court order requiring or prohibiting specific action.

**Liability**
: Legal responsibility for harm.

**Negligence**
: Failure to exercise reasonable care, causing harm.

**Precedent**
: Earlier court decision that guides current cases.

**Prima Facie**
: Evidence sufficient to prove something unless rebutted.

**Pro Bono**
: Legal work done for free (Latin: "for the public good").

**Statute of Limitations**
: Time limit for filing a lawsuit.

**Tort**
: Civil wrong causing harm (like negligence, defamation).

## Abbreviations

**API**: Application Programming Interface
**CLI**: Command Line Interface
**CSV**: Comma-Separated Values
**D.**: District (as in D.S.C. = District of South Carolina)
**F.3d**: Federal Reporter, Third Series
**JSON**: JavaScript Object Notation
**LLM**: Large Language Model
**PDF**: Portable Document Format
**S.C.**: South Carolina (state reporter)
**S.Ct.**: Supreme Court Reporter
**U.S.**: United States Reports
**U.S.C.**: United States Code

## File Extensions

**.md**: Markdown file (text with formatting)
**.pdf**: PDF document
**.docx**: Microsoft Word document
**.json**: Configuration file
**.csv**: Spreadsheet data
**.txt**: Plain text file
**.py**: Python code file
**.env**: Environment variables file

## Common Error Messages

**"API key not found"**
: WePublicDefender can't find your OpenAI/xAI password. Check .env file.

**"Rate limit exceeded"**
: Too many requests too quickly. Wait a minute and try again.

**"Command not found"**
: Terminal doesn't recognize the command. Check spelling or PATH.

**"Permission denied"**
: You don't have access to that file/folder. Run as administrator or check ownership.

**"Module not found"**
: Python package missing. Usually fixed by reinstalling WePublicDefender.

## Next Steps

- Return to [Getting Started](Getting-Started)
- Check [Troubleshooting](Troubleshooting) for error solutions
- Review [Basic Usage](Basic-Usage) for practical examples
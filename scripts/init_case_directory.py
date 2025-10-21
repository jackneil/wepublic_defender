#!/usr/bin/env python3
"""
Initialize standard directory structure for legal case management.
Run this after cloning we_public_defender repo into a case folder.
"""

import os
import platform
from pathlib import Path

# Standard directory structure
DIRECTORIES = [
    "00_NEW_DOCUMENTS_INBOX",
    "01_CASE_OVERVIEW",
    "02_PLEADINGS/01_Complaint",
    "02_PLEADINGS/02_Answer",
    "02_PLEADINGS/03_Motions",
    "02_PLEADINGS/04_Orders",
    "02_PLEADINGS/05_Briefs",
    "02_PLEADINGS/06_Amendment",
    "03_DISCOVERY/01_Our_Requests",
    "03_DISCOVERY/02_Their_Requests",
    "03_DISCOVERY/03_Our_Responses",
    "03_DISCOVERY/04_Their_Responses",
    "03_DISCOVERY/05_Deposition_Transcripts",
    "04_EVIDENCE/01_Documents",
    "04_EVIDENCE/02_Communications",
    "04_EVIDENCE/03_Financial_Records",
    "04_EVIDENCE/04_Expert_Reports",
    "05_CORRESPONDENCE/01_With_Opposing_Counsel",
    "05_CORRESPONDENCE/02_With_Court",
    "05_CORRESPONDENCE/03_Internal",
    "06_RESEARCH/01_Case_Law",
    "06_RESEARCH/02_Statutes",
    "06_RESEARCH/03_Secondary_Sources",
    "07_DRAFTS_AND_WORK_PRODUCT/drafts",
    "07_DRAFTS_AND_WORK_PRODUCT/outlines",
    "07_DRAFTS_AND_WORK_PRODUCT/scripts",
    "08_REFERENCE/court_rules",
    "08_REFERENCE/forms",
    "08_REFERENCE/templates",
]

# README templates for key directories
README_TEMPLATES = {
    "00_NEW_DOCUMENTS_INBOX/README.md": """# New Documents Inbox

Place new documents here for organization.

Claude will help organize these files into the appropriate directories.

Run `/organize` command to categorize and move files.
""",
    "01_CASE_OVERVIEW/README.md": """# Case Overview

This directory contains high-level case information:
- case_summary.md: Brief description of the case
- timeline.md: Key dates and events
- parties.md: Information about parties and counsel
- jurisdiction_notes.md: Court and jurisdiction details
""",
    "07_DRAFTS_AND_WORK_PRODUCT/README.md": """# Drafts and Work Product

Working documents and drafts. Files here are NOT for filing.

Structure:
- drafts/: Document drafts in progress
- outlines/: Outlines and planning documents
- scripts/: Python scripts for document generation
""",
}

def create_directory_structure():
    """Create all standard directories."""
    base_path = Path.cwd()

    print("Initializing legal case directory structure...")
    print(f"Base path: {base_path}\n")

    created = 0
    existed = 0

    for dir_path in DIRECTORIES:
        full_path = base_path / dir_path
        if full_path.exists():
            print(f"  [EXISTS] {dir_path}")
            existed += 1
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  [CREATED] {dir_path}")
            created += 1

    print(f"\nDirectories: {created} created, {existed} already existed")
    return created, existed

def create_readme_files():
    """Create README files in key directories."""
    base_path = Path.cwd()

    print("\nCreating README files...")

    for readme_path, content in README_TEMPLATES.items():
        full_path = base_path / readme_path
        if not full_path.exists():
            full_path.write_text(content)
            print(f"  [CREATED] {readme_path}")
        else:
            print(f"  [EXISTS] {readme_path}")

def create_symlinks():
    """Create symlinks for Claude configuration."""
    base_path = Path.cwd()

    print("\nCreating configuration symlinks...")

    # Determine source path: try subdirectory first, then installed package
    source_base = base_path / "wepublic_defender"
    if not (source_base / ".claude").exists():
        # Try finding it from installed package (go up to repo root)
        try:
            import wepublic_defender
            source_base = Path(wepublic_defender.__file__).parent.parent
        except (ImportError, AttributeError):
            pass

    # Symlink/Copy CLAUDE.md from repo to root (always overwrite)
    claude_md_source = source_base / ".claude" / "CLAUDE.md"
    claude_md_target = base_path / "CLAUDE.md"

    if claude_md_source.exists():
        # On Windows, use copy instead of symlink (requires admin)
        if os.name == 'nt':
            import shutil
            shutil.copy2(claude_md_source, claude_md_target)
            print("  [UPDATED] CLAUDE.md")
        else:
            if claude_md_target.exists():
                claude_md_target.unlink()
            claude_md_target.symlink_to(claude_md_source)
            print("  [UPDATED] CLAUDE.md")
    else:
        print(f"  [WARNING] Source file not found: {claude_md_source}")

    # Copy LEGAL_WORK_PROTOCOL.md from new location (always overwrite)
    protocol_source = source_base / ".claude" / "protocols" / "LEGAL_WORK_PROTOCOL.md"
    protocol_target = base_path / "LEGAL_WORK_PROTOCOL.md"

    if protocol_source.exists():
        import shutil
        shutil.copy2(protocol_source, protocol_target)
        print("  [UPDATED] LEGAL_WORK_PROTOCOL.md")
    else:
        # Fallback to old location for backwards compatibility
        protocol_source_old = source_base / ".claude" / "LEGAL_WORK_PROTOCOL.md"
        if protocol_source_old.exists():
            import shutil
            shutil.copy2(protocol_source_old, protocol_target)
            print("  [UPDATED] LEGAL_WORK_PROTOCOL.md (from old location)")

    # Copy COMMANDS_REFERENCE.md (always overwrite)
    commands_source = source_base / ".claude" / "COMMANDS_REFERENCE.md"
    commands_target = base_path / "COMMANDS_REFERENCE.md"

    if commands_source.exists():
        import shutil
        shutil.copy2(commands_source, commands_target)
        print("  [UPDATED] COMMANDS_REFERENCE.md")

    # Copy SESSION_START_MANDATORY.md to .claude/ (always overwrite)
    session_start_source = source_base / ".claude" / "SESSION_START_MANDATORY.md"
    session_start_target = base_path / ".claude" / "SESSION_START_MANDATORY.md"

    if session_start_source.exists():
        import shutil
        # Ensure .claude directory exists
        session_start_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(session_start_source, session_start_target)
        print("  [UPDATED] .claude/SESSION_START_MANDATORY.md")
    else:
        print(f"  [WARNING] Source file not found: {session_start_source}")

    # Copy .env example to root if no .env exists
    env_example = base_path / "wepublic_defender" / ".env.example"
    env_target = base_path / ".env"
    if env_example.exists() and not env_target.exists():
        import shutil
        shutil.copy2(env_example, env_target)
        print("  [COPIED] .env example to .env (fill in your API keys)")

    # Ensure per-case settings directory exists and copy default settings
    case_settings = base_path / ".wepublic_defender"
    case_settings.mkdir(parents=True, exist_ok=True)

    # Locate source config directory robustly (works regardless of CWD)
    repo_root = Path(__file__).resolve().parents[1]  # repo root
    source_candidates = [
        repo_root / "wepublic_defender" / "config",  # package config path
        repo_root / "config",  # fallback if config is at repo root
    ]
    source_config_dir = None
    for cand in source_candidates:
        if cand.exists():
            source_config_dir = cand
            break

    if source_config_dir is None:
        print("  [WARN] Could not locate source config directory.")
        return

    default_review = source_config_dir / "legal_review_settings.json"
    target_review = case_settings / "legal_review_settings.json"
    if default_review.exists() and not target_review.exists():
        import shutil
        shutil.copy2(default_review, target_review)
        print("  [COPIED] per-case settings: .wepublic_defender/legal_review_settings.json")

    default_providers = source_config_dir / "llm_providers.json"
    target_providers = case_settings / "llm_providers.json"
    if default_providers.exists() and not target_providers.exists():
        import shutil
        shutil.copy2(default_providers, target_providers)
        print("  [COPIED] per-case settings: .wepublic_defender/llm_providers.json")
    if not default_review.exists() or not default_providers.exists():
        print("  [WARN] Source config files not found in:")
        print(f"        {source_config_dir}")
        print("        Ensure repo is intact (look for wepublic_defender/config/*.json).")

    # Copy/merge .claude/commands so Claude can discover commands at case root
    commands_src = repo_root / ".claude" / "commands"
    commands_dst = base_path / ".claude" / "commands"
    try:
        if commands_src.exists():
            commands_dst.mkdir(parents=True, exist_ok=True)
            for item in commands_src.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(commands_src)
                    dst_file = commands_dst / rel
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    if not dst_file.exists():
                        import shutil
                        shutil.copy2(item, dst_file)
                        print(f"  [COPIED] .claude/commands/{rel}")
    except Exception as e:
        print(f"  [WARN] Failed to copy .claude/commands: {e}")

    # Copy/merge .claude/workflows (workflow instruction files)
    workflows_src = repo_root / ".claude" / "workflows"
    workflows_dst = base_path / ".claude" / "workflows"
    try:
        if workflows_src.exists():
            workflows_dst.mkdir(parents=True, exist_ok=True)
            for item in workflows_src.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(workflows_src)
                    dst_file = workflows_dst / rel
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(item, dst_file)
                    print(f"  [COPIED] .claude/workflows/{rel}")
    except Exception as e:
        print(f"  [WARN] Failed to copy .claude/workflows: {e}")

    # Copy/merge .claude/protocols (legal standards and protocols)
    protocols_src = repo_root / ".claude" / "protocols"
    protocols_dst = base_path / ".claude" / "protocols"
    try:
        if protocols_src.exists():
            protocols_dst.mkdir(parents=True, exist_ok=True)
            for item in protocols_src.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(protocols_src)
                    dst_file = protocols_dst / rel
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(item, dst_file)
                    print(f"  [COPIED] .claude/protocols/{rel}")
    except Exception as e:
        print(f"  [WARN] Failed to copy .claude/protocols: {e}")

    # Copy/merge .claude/templates (session notes, timeline templates)
    templates_src = repo_root / ".claude" / "templates"
    templates_dst = base_path / ".claude" / "templates"
    try:
        if templates_src.exists():
            templates_dst.mkdir(parents=True, exist_ok=True)
            for item in templates_src.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(templates_src)
                    dst_file = templates_dst / rel
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy2(item, dst_file)
                    print(f"  [COPIED] .claude/templates/{rel}")
    except Exception as e:
        print(f"  [WARN] Failed to copy .claude/templates: {e}")

    # Copy/merge .claude/hooks (session automation - SessionStart, etc.)
    # OS-aware: Copy only the appropriate hook files for the current platform
    hooks_src = repo_root / ".claude" / "hooks"
    hooks_dst = base_path / ".claude" / "hooks"
    try:
        if hooks_src.exists():
            hooks_dst.mkdir(parents=True, exist_ok=True)

            # Determine OS and corresponding hook file extension
            current_os = platform.system()
            if current_os == 'Windows':
                hook_extension = '.bat'
            else:  # Linux, Darwin (Mac), or other Unix-like
                hook_extension = '.sh'

            # List of hook names to copy (canonical names without extension)
            # These hooks exist for all platforms
            hook_names = ['SessionStart', 'PreCompact']

            # Windows-only hooks (remind about backslashes for Edit/MultiEdit)
            if current_os == 'Windows':
                hook_names.append('UserPromptSubmit')

            import shutil
            for hook_name in hook_names:
                # Source: OS-specific hook file (e.g., SessionStart.bat or SessionStart.sh)
                src_file = hooks_src / f"{hook_name}{hook_extension}"
                # Destination: Canonical name without extension (e.g., SessionStart)
                dst_file = hooks_dst / hook_name

                if src_file.exists():
                    shutil.copy2(src_file, dst_file)
                    # Make executable on Unix/Mac (hooks need execute permission)
                    if current_os != 'Windows':
                        os.chmod(dst_file, 0o755)
                    print(f"  [COPIED] .claude/hooks/{hook_name} (from {hook_name}{hook_extension})")
                else:
                    print(f"  [WARN] Hook not found: {src_file}")
    except Exception as e:
        print(f"  [WARN] Failed to copy .claude/hooks: {e}")

    # Copy .claude/settings.local.json to enable hooks and permissions
    # Use template-based approach with platform-specific overrides
    settings_template_src = repo_root / ".claude" / "templates" / "settings.local.json"
    settings_local_dst = base_path / ".claude" / "settings.local.json"

    if settings_template_src.exists():
        import shutil
        import json

        # Create .claude directory if needed
        settings_local_dst.parent.mkdir(parents=True, exist_ok=True)

        # Copy base template
        shutil.copy2(settings_template_src, settings_local_dst)

        # If on Windows, merge Windows-specific overrides
        current_os = platform.system()
        if current_os == 'Windows':
            windows_overrides_src = repo_root / ".claude" / "templates" / "settings.local.windows_overrides.json"
            if windows_overrides_src.exists():
                # Load base settings
                with open(settings_local_dst, 'r', encoding='utf-8') as f:
                    base_settings = json.load(f)

                # Load Windows overrides
                with open(windows_overrides_src, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)

                # Merge hooks (add Windows-specific hooks to base)
                if 'hooks' in overrides:
                    base_settings['hooks'].update(overrides['hooks'])

                # Write merged settings back
                with open(settings_local_dst, 'w', encoding='utf-8') as f:
                    json.dump(base_settings, f, indent=2)

                print("  [UPDATED] .claude/settings.local.json (with Windows-specific overrides)")
            else:
                print("  [UPDATED] .claude/settings.local.json (base template, Windows overrides not found)")
        else:
            print("  [UPDATED] .claude/settings.local.json (base template for Unix/Mac)")
    else:
        print(f"  [WARNING] Source template not found: {settings_template_src}")

    # Create .database for state tracking (file management logs, etc.)
    db_dir = base_path / ".database"
    db_dir.mkdir(parents=True, exist_ok=True)

    # README explaining .database/
    db_readme = db_dir / "README.md"
    if not db_readme.exists():
        db_readme.write_text(
            "# .database Directory\n\n"
            "This directory tracks file management state to prevent duplicate work and provide audit trail.\n\n"
            "**IMPORTANT:** This directory is per-case and should NOT be committed to git (.gitignored).\n\n"
            "## Files\n\n"
            "### file_management_log.md\n"
            "Human-readable ledger of all file management actions.\n\n"
            "Format: `timestamp | action | src | dst | notes`\n\n"
            "Example:\n"
            "```\n"
            "2025-10-20 14:30:00 | moved | 00_NEW_DOCUMENTS_INBOX/doc.pdf | 02_PLEADINGS/03_Motions/MOTION.pdf | Categorized as motion\n"
            "```\n\n"
            "### file_management_index.json\n"
            "JSON index keyed by file path for quick lookup.\n\n"
            "Used to check: \"Have I already processed this file?\"\n\n"
            "Format:\n"
            "```json\n"
            "{\n"
            '  "path/to/file.pdf": {\n'
            '    "timestamp": "2025-10-20 14:30:00",\n'
            '    "action": "moved",\n'
            '    "src": "00_NEW_DOCUMENTS_INBOX/doc.pdf",\n'
            '    "dst": "02_PLEADINGS/03_Motions/MOTION.pdf",\n'
            '    "notes": "Categorized as motion"\n'
            "  }\n"
            "}\n"
            "```\n\n"
            "## Usage\n\n"
            "- `/organize` command reads index to skip already-processed files\n"
            "- SessionStart hook reports organization stats if available\n"
            "- Provides crash recovery - know what's been done even if session crashes\n\n"
            "## Relationship to Other Tracking\n\n"
            "- `.database/` = File movements and organization\n"
            "- `.wepublic_defender/session_notes.md` = Current work in progress\n"
            "- `.wepublic_defender/case_timeline.md` = Major case events (filings, orders, etc.)\n",
            encoding="utf-8",
        )
        print("  [CREATED] .database/README.md")

    fm_log = db_dir / "file_management_log.md"
    if not fm_log.exists():
        fm_log.write_text(
            "# File Management Log\n\n"
            "Records of file moves, folder consolidations, and related file management actions.\n\n"
            "Columns: timestamp | action | src | dst | notes\n\n",
            encoding="utf-8",
        )
        print("  [CREATED] .database/file_management_log.md")

    fm_index = db_dir / "file_management_index.json"
    if not fm_index.exists():
        fm_index.write_text("{}", encoding="utf-8")
        print("  [CREATED] .database/file_management_index.json")

def create_gameplan():
    """Create GAMEPLAN.md if it doesn't exist."""
    base_path = Path.cwd()
    gameplan_path = base_path / "GAMEPLAN.md"

    if not gameplan_path.exists():
        template = """# Case Strategy and Game Plan

## Current Status
[Brief description of where case stands]

## Immediate Next Steps
1. [Action item]
2. [Action item]
3. [Action item]

## Key Deadlines
- [Date]: [Event/Deadline]

## Strategic Goals
[High-level strategic objectives]

## Risks and Concerns
[Potential issues to monitor]

## Notes
[Additional strategic notes]
"""
        gameplan_path.write_text(template)
        print("\n[CREATED] GAMEPLAN.md")
    else:
        print("\n[EXISTS] GAMEPLAN.md")

def _get_logger():
    """Get logger, handling case where package may not be importable yet."""
    try:
        from wepublic_defender.logging_utils import get_logger
        return get_logger()
    except ImportError:
        # Package not installed yet, return None
        return None


def main():
    """Main initialization function."""
    logger = _get_logger()

    print("="*60)
    print("LEGAL CASE DIRECTORY INITIALIZATION")
    print("="*60)

    if logger:
        logger.info("Case init started | cwd=%s", Path.cwd())

    # Create directory structure
    created, existed = create_directory_structure()
    if logger:
        logger.info("Directory structure | created=%s | existed=%s", created, existed)

    # Create README files
    create_readme_files()
    if logger:
        logger.info("README files created")

    # Create symlinks/copies for Claude
    create_symlinks()
    if logger:
        logger.info("Configuration files copied/symlinked")

    # Create GAMEPLAN.md
    create_gameplan()
    if logger:
        logger.info("GAMEPLAN.md initialized")

    print("\n" + "="*60)
    print("INITIALIZATION COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Configure API keys in .env")
    print("2. Edit GAMEPLAN.md with case strategy")
    print("3. Add case details to 01_CASE_OVERVIEW/")
    print("4. Place new documents in 00_NEW_DOCUMENTS_INBOX/")
    print("5. Start Claude Code: claude")
    print("\nClaude will help organize files and maintain structure.")
    print("\n" + "="*60)
    print("AVAILABLE COMMANDS")
    print("="*60)
    print("\nJust type these in Claude Code (or ask in plain English):")
    print("\n  /check-env             Check setup and API keys")
    print("  /organize              Organize inbox files")
    print("  /deep-research-prep    Generate deep research prompt")
    print("  /research [topic]      Quick legal research")
    print("  /strategy              Get strategic recommendations")
    print("  /draft [type]          Draft a legal document")
    print("  /review [file]         Review document before filing")
    print("\nOr just tell Claude what you want in plain English!")
    print("\nFor more details, open COMMANDS_REFERENCE.md")
    print("="*60)

    # IMPORTANT: Warn about needing to restart Claude Code for slash commands
    print("\n" + "="*60)
    print("*** IMPORTANT: RESTART CLAUDE CODE NOW ***")
    print("="*60)
    print("\nSlash commands have been installed to .claude/commands/")
    print("but Claude Code must be restarted to load them.")
    print("\nSteps:")
    print("  1. Exit Claude Code (Ctrl+C or close the window)")
    print("  2. Run 'claude' again in this same folder")
    print("  3. Slash commands like /deep-research-prep will now work")
    print("\n" + "="*60 + "\n")

    if logger:
        logger.info("Case init completed successfully")

if __name__ == "__main__":
    main()

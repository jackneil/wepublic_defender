#!/usr/bin/env python3
"""
Organize files from 00_NEW_DOCUMENTS_INBOX/ into appropriate directories.
Can be called by Claude or run standalone.
"""

import shutil
from pathlib import Path
from typing import List, Tuple

# File categorization rules (keywords in filename)
CATEGORIZATION_RULES = {
    "02_PLEADINGS": [
        "complaint", "answer", "motion", "order", "brief",
        "memorandum", "response", "reply", "petition", "amended"
    ],
    "03_DISCOVERY": [
        "discovery", "interrogator", "request_for_production",
        "request_for_admission", "deposition", "rfa", "rfp", "rog"
    ],
    "04_EVIDENCE": [
        "evidence", "exhibit", "statement", "record", "receipt",
        "invoice", "contract", "agreement", "transcript"
    ],
    "05_CORRESPONDENCE": [
        "letter", "email", "correspondence", "notice", "communication"
    ],
    "06_RESEARCH": [
        "research", "case_law", "statute", "analysis", "notes"
    ],
    "07_DRAFTS_AND_WORK_PRODUCT": [
        "draft", "outline", "notes", "work_product", "memo"
    ],
    "08_REFERENCE": [
        "rule", "form", "template", "reference", "guide"
    ]
}

def categorize_file(filename: str) -> str:
    """
    Categorize a file based on its name.

    Returns directory path or None if uncertain.
    """
    filename_lower = filename.lower()

    for directory, keywords in CATEGORIZATION_RULES.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return directory

    return None

def organize_inbox(dry_run: bool = False) -> Tuple[List[str], List[str], List[str]]:
    """
    Organize files from inbox.

    Args:
        dry_run: If True, only show what would be done

    Returns:
        (moved_files, uncertain_files, errors)
    """
    base_path = Path.cwd()
    inbox_path = base_path / "00_NEW_DOCUMENTS_INBOX"

    if not inbox_path.exists():
        return [], [], ["Inbox directory not found"]

    moved = []
    uncertain = []
    errors = []

    # Get all files in inbox (skip README)
    files = [f for f in inbox_path.iterdir()
             if f.is_file() and f.name != "README.md"]

    for file_path in files:
        try:
            # Categorize file
            target_dir = categorize_file(file_path.name)

            if target_dir is None:
                uncertain.append(file_path.name)
                continue

            # Build target path
            target_path = base_path / target_dir / file_path.name

            # Move file (or simulate)
            if dry_run:
                moved.append(f"{file_path.name} → {target_dir}/")
            else:
                shutil.move(str(file_path), str(target_path))
                moved.append(f"{file_path.name} → {target_dir}/")

        except Exception as e:
            errors.append(f"{file_path.name}: {str(e)}")

    return moved, uncertain, errors

def main():
    """Run organization with user confirmation."""
    print("="*60)
    print("INBOX ORGANIZATION")
    print("="*60)

    # Dry run first
    print("\nScanning inbox...")
    moved, uncertain, errors = organize_inbox(dry_run=True)

    if not moved and not uncertain:
        print("No files found in inbox.")
        return

    # Show what would be moved
    if moved:
        print(f"\nWould move {len(moved)} files:")
        for item in moved:
            print(f"  ✓ {item}")

    if uncertain:
        print(f"\nUncertain about {len(uncertain)} files:")
        for item in uncertain:
            print(f"  ? {item}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  ✗ {error}")

    # Confirm
    if moved:
        response = input("\nProceed with moving files? (y/n): ")
        if response.lower() == 'y':
            moved, uncertain, errors = organize_inbox(dry_run=False)
            print(f"\n✓ Moved {len(moved)} files successfully")
            if uncertain:
                print(f"? {len(uncertain)} files need manual categorization")
        else:
            print("\nCancelled.")

if __name__ == "__main__":
    main()

"""
Console script wrapper for wpd-init-case.
Imports and runs the full initialization from scripts/init_case_directory.py
"""
import sys
from pathlib import Path

# Add scripts directory to path so we can import init_case_directory
repo_root = Path(__file__).resolve().parents[2]
scripts_path = repo_root / "scripts"
sys.path.insert(0, str(scripts_path))

try:
    from init_case_directory import main as init_main
except ImportError as e:
    print("ERROR: Could not import init_case_directory module.")
    print(f"Expected location: {scripts_path / 'init_case_directory.py'}")
    print(f"Error: {e}")
    sys.exit(1)


def main() -> int:
    """Run the full case directory initialization."""
    result = init_main()
    return result if result is not None else 0


if __name__ == "__main__":
    sys.exit(main())

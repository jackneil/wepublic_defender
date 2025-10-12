import argparse
import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def _ensure_utf8():
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")  # type: ignore
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")  # type: ignore
    except Exception:
        pass


def _now() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    _ensure_utf8()

    ap = argparse.ArgumentParser(prog="wpd-file-log", description="Append a file management action to the .database/file_management_* files")
    ap.add_argument("--action", default="other", help="Action type (e.g., moved, merged, deleted_empty, categorized, renamed, other)")
    ap.add_argument("--src", help="Source path (if applicable)")
    ap.add_argument("--dst", help="Destination path (if applicable)")
    ap.add_argument("--notes", help="Free-form notes", default="")
    args = ap.parse_args()

    db_dir = Path.cwd() / ".database"
    db_dir.mkdir(parents=True, exist_ok=True)
    log_path = db_dir / "file_management_log.md"
    idx_path = db_dir / "file_management_index.json"

    # Append to markdown log
    line = f"{_now()} | {args.action} | {args.src or '-'} | {args.dst or '-'} | {args.notes or '-'}\n"
    if not log_path.exists():
        log_path.write_text("# File Management Log\n\n", encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)

    # Update JSON index
    idx: Dict[str, Any] = {}
    if idx_path.exists():
        try:
            idx = json.loads(idx_path.read_text(encoding="utf-8"))
        except Exception:
            idx = {}

    entry = {
        "timestamp": _now(),
        "action": args.action,
        "src": args.src,
        "dst": args.dst,
        "notes": args.notes,
    }
    if args.src:
        idx[args.src] = entry
    if args.dst:
        idx[args.dst] = entry

    idx_path.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[write] .database/file_management_log.md", flush=True)
    print(f"[write] .database/file_management_index.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""CSV usage logging for cost tracking."""
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


def log_agent_call(
    agent: str,
    model: str,
    file_or_text: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int,
    cost: float,
    duration: float,
    status: str = "success",
    error: Optional[str] = None,
) -> None:
    """Append agent call to usage log CSV."""
    # Find case root (where .wepublic_defender exists)
    cwd = Path.cwd()
    wpd_dir = cwd / ".wepublic_defender"

    # If not in case root, try to find it
    if not wpd_dir.exists():
        for parent in cwd.parents:
            if (parent / ".wepublic_defender").exists():
                wpd_dir = parent / ".wepublic_defender"
                break

    # Create .wepublic_defender if needed
    wpd_dir.mkdir(parents=True, exist_ok=True)

    csv_path = wpd_dir / "usage_log.csv"

    # Create with headers if new
    is_new = not csv_path.exists()

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if is_new:
            writer.writerow([
                "timestamp",
                "agent",
                "model",
                "file",
                "input_tokens",
                "output_tokens",
                "cached_tokens",
                "cost",
                "duration",
                "status",
                "error",
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            agent,
            model,
            file_or_text,
            input_tokens,
            output_tokens,
            cached_tokens,
            f"{cost:.6f}",
            f"{duration:.2f}",
            status,
            error or "",
        ])

"""Usage summary report from CSV log."""
import sys
import csv
from pathlib import Path
from collections import defaultdict


def main() -> int:
    """Print usage summary from CSV log."""
    # Find .wepublic_defender directory
    cwd = Path.cwd()
    wpd_dir = cwd / ".wepublic_defender"

    if not wpd_dir.exists():
        for parent in cwd.parents:
            if (parent / ".wepublic_defender").exists():
                wpd_dir = parent / ".wepublic_defender"
                break

    csv_path = wpd_dir / "usage_log.csv"

    if not csv_path.exists():
        print("No usage log found. Run some agents first.")
        return 1

    # Parse CSV
    total_cost = 0.0
    total_calls = 0
    by_agent = defaultdict(lambda: {"calls": 0, "cost": 0.0, "tokens_in": 0, "tokens_out": 0})
    by_model = defaultdict(lambda: {"calls": 0, "cost": 0.0, "tokens_in": 0, "tokens_out": 0})
    errors = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_calls += 1
            cost = float(row.get("cost", 0))
            total_cost += cost

            agent = row.get("agent", "unknown")
            model = row.get("model", "unknown")
            status = row.get("status", "success")

            if status == "error":
                errors += 1
                continue

            in_tok = int(row.get("input_tokens", 0))
            out_tok = int(row.get("output_tokens", 0))

            by_agent[agent]["calls"] += 1
            by_agent[agent]["cost"] += cost
            by_agent[agent]["tokens_in"] += in_tok
            by_agent[agent]["tokens_out"] += out_tok

            by_model[model]["calls"] += 1
            by_model[model]["cost"] += cost
            by_model[model]["tokens_in"] += in_tok
            by_model[model]["tokens_out"] += out_tok

    # Print report
    print("\n=== WePublicDefender Usage Summary ===\n")
    print(f"Total calls: {total_calls}")
    print(f"Successful: {total_calls - errors}")
    print(f"Errors: {errors}")
    print(f"Total cost: ${total_cost:.4f}\n")

    print("--- By Agent ---")
    for agent, stats in sorted(by_agent.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"{agent:20s} | {stats['calls']:3d} calls | ${stats['cost']:7.4f} | {stats['tokens_in']:6d} in | {stats['tokens_out']:6d} out")

    print("\n--- By Model ---")
    for model, stats in sorted(by_model.items(), key=lambda x: x[1]["cost"], reverse=True):
        print(f"{model:20s} | {stats['calls']:3d} calls | ${stats['cost']:7.4f} | {stats['tokens_in']:6d} in | {stats['tokens_out']:6d} out")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())

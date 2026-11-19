#!/usr/bin/env python3
"""Merge task_coverage JSONL files and the static task inventory into a coverage report.

The report is informational: it always exits 0 so that it can never gate a pull request. A runtime path that is
missing from the inventory is the one exception that is made loud, with a workflow error annotation, because
it means the two sides no longer agree on what a task is and every number below it is suspect.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from task_inventory import load_inventory


# Phases whose records never count: verify and prepare may run role task files but do not apply the roles.
EXCLUDED_PHASES = {"verify", "prepare"}


def read_records(jsonl_files: list[Path]) -> list[dict[str, Any]]:
    """Read every usable record, warning about and skipping blank, truncated or malformed lines."""
    records: list[dict[str, Any]] = []
    for jsonl in jsonl_files:
        with jsonl.open(encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    absent = {"path", "scenario", "host"} - record.keys()
                    if absent:
                        raise KeyError(sorted(absent))
                except (json.JSONDecodeError, KeyError, AttributeError) as error:
                    print(f"::warning::{jsonl}:{number}: skipping unreadable coverage record ({error!r})",
                          file=sys.stderr)
                    continue
                records.append(record)
    return records


def percent(part: int, whole: int) -> float:
    """Return part as a percentage of whole, rounded to one decimal."""
    return round(100 * part / whole, 1) if whole else 0.0


def build_report(inventory: dict[str, dict[str, Any]], records: list[dict[str, Any]],
                 missing: list[str]) -> dict[str, Any]:
    """Compute the coverage figures from the inventory and the runtime records."""
    known = [record for record in records
             if record["path"] in inventory and record.get("phase") not in EXCLUDED_PHASES]
    # A task is executed in a cell when it reported ok, which includes changed.
    executed_in: dict[str, set[str]] = defaultdict(set)
    statuses: dict[str, set[str]] = defaultdict(set)
    has_when: dict[str, bool] = defaultdict(bool)
    platform_executed: dict[str, set[str]] = defaultdict(set)
    for record in known:
        platform = f"{record['scenario']}/{record['host']}"
        statuses[record["path"]].add(record["status"])
        has_when[record["path"]] = has_when[record["path"]] or bool(record["has_when"])
        if record["status"] == "ok":
            executed_in[record["path"]].add(platform)
            platform_executed[platform].add(record["path"])

    roles: dict[str, dict[str, Any]] = {}
    for path, task in inventory.items():
        entry = roles.setdefault(task["role"], {"total": 0, "executed": 0, "never_executed": []})
        entry["total"] += 1
        if path in executed_in:
            entry["executed"] += 1
        else:
            seen = sorted(statuses.get(path, set()))
            entry["never_executed"].append({
                "path": path,
                "name": task["name"],
                "seen": ", ".join(seen) if seen else "never reached",
            })
    for entry in roles.values():
        entry["percent"] = percent(entry["executed"], entry["total"])

    executed_only = sorted(p for p in inventory if has_when[p] and statuses[p] == {"ok"})
    skipped_only = sorted(p for p in inventory if has_when[p] and statuses[p] == {"skipped"})

    # A platform that only skipped or failed still gets a column, with zero counts.
    platforms = sorted({f"{record['scenario']}/{record['host']}" for record in known})
    matrix = {
        platform: {
            role: sum(1 for path in platform_executed.get(platform, set()) if inventory[path]["role"] == role)
            for role in roles
        }
        for platform in platforms
    }
    total = len(inventory)
    executed = sum(entry["executed"] for entry in roles.values())
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "totals": {"tasks": total, "executed": executed, "percent": percent(executed, total),
                   "records": len(known), "platforms": platforms},
        "roles": dict(sorted(roles.items())),
        "one_sided": {
            "executed_only": [{"path": p, "name": inventory[p]["name"]} for p in executed_only],
            "skipped_only": [{"path": p, "name": inventory[p]["name"]} for p in skipped_only],
        },
        "matrix": matrix,
        "inventory_mismatch": missing,
    }


def cell(text: object) -> str:
    """Escape a value for a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: dict[str, Any]) -> str:
    """Render the report as GitHub flavoured Markdown."""
    totals = report["totals"]
    out = ["## Molecule task coverage", ""]
    if report["inventory_mismatch"]:
        out += [f"> **ERROR: {len(report['inventory_mismatch'])} runtime task paths are missing from the static "
                "inventory.** Line numbers or the task model disagree; the figures below are unreliable.", ""]
        out += [f"- `{path}`" for path in report["inventory_mismatch"]] + [""]
    out += [f"**{totals['executed']} of {totals['tasks']} tasks executed ({totals['percent']}%)** "
            f"on {len(totals['platforms'])} platforms, from {totals['records']} records. "
            "A task counts as executed when it reported ok or changed on at least one platform.", ""]

    out += ["### Coverage per role", "", "| Role | Executed | Total | % |", "| --- | ---: | ---: | ---: |"]
    for role, entry in report["roles"].items():
        out.append(f"| {role} | {entry['executed']} | {entry['total']} | {entry['percent']} |")

    out += ["", "### Never executed", ""]
    for role, entry in report["roles"].items():
        if not entry["never_executed"]:
            continue
        out += [f"<details><summary>{role}: {len(entry['never_executed'])}</summary>", "",
                "| Task | Name | Seen as |", "| --- | --- | --- |"]
        out += [f"| `{t['path']}` | {cell(t['name'])} | {t['seen']} |" for t in entry["never_executed"]]
        out += ["", "</details>", ""]

    one_sided = report["one_sided"]
    out += ["### One-sided conditions", "",
            "Tasks with a `when` that only ever ran, so the skip branch is untested, or only ever skipped.", ""]
    for title, key in (("Only executed", "executed_only"), ("Only skipped", "skipped_only")):
        out += [f"<details><summary>{title}: {len(one_sided[key])}</summary>", "",
                "| Task | Name |", "| --- | --- |"]
        out += [f"| `{t['path']}` | {cell(t['name'])} |" for t in one_sided[key]]
        out += ["", "</details>", ""]

    platforms = totals["platforms"]
    out += ["### Executed tasks per platform and role", "",
            "Tasks executed on each platform out of the role total, a zero or low column marks a container-only gap.",
            "", "| Role | " + " | ".join(platforms) + " |", "| --- | " + " | ".join("---:" for _ in platforms) + " |"]
    for role, entry in report["roles"].items():
        counts = " | ".join(f"{report['matrix'][p][role]}/{entry['total']}" for p in platforms)
        out.append(f"| {role} | {counts} |")
    return "\n".join(out) + "\n"


def find_jsonl(paths: list[Path]) -> list[Path]:
    """Expand directories into the task_coverage.jsonl files below them."""
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found += sorted(path.rglob("task_coverage.jsonl"))
        elif path.is_file():
            found.append(path)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("logs", type=Path, nargs="*", default=[Path("molecule-logs")],
                        help="directories searched for task_coverage.jsonl, or the files themselves")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", type=Path, default=Path("molecule-logs/coverage.json"), dest="json_path")
    args = parser.parse_args()

    jsonl_files = find_jsonl(args.logs)
    if not jsonl_files:
        print("coverage_report: no task_coverage.jsonl found, nothing to report", file=sys.stderr)
        return 0
    inventory = load_inventory(args.root)
    records = read_records(jsonl_files)
    missing = sorted({record["path"] for record in records} - inventory.keys())
    if missing:
        print(f"::error title=Task coverage inventory mismatch::{len(missing)} runtime task paths are not in "
              "the static inventory", file=sys.stderr)
    report = build_report(inventory, records, missing)

    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = render_markdown(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(markdown)
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())

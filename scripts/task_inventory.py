#!/usr/bin/env python3
"""Enumerate every task and handler in roles/ with the file:line keys that Ansible reports at runtime.

The keys match what ``task.get_path()`` returns for a task, made relative to the collection root, so the
inventory can be joined with the records written by the ``task_coverage`` callback plugin.

Counting rules:
- A ``block`` is not a task, its ``block``, ``rescue`` and ``always`` children are.
- A looped task is one task, however many items it loops over.
- ``import_tasks`` and ``import_role`` lines are not tasks, they emit no event, the imported tasks are counted
  from their own files.
- ``include_tasks`` and ``include_role`` lines are tasks, they run and report like any other task.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

BLOCK_KEYS = ("block", "rescue", "always")
IMPORT_ACTIONS = {"import_tasks", "import_role"}
# Task keywords that are never the action, anything left over, other than with_*, is the module name.
KEYWORDS = {
    "any_errors_fatal", "args", "async", "become", "become_exe", "become_flags", "become_method", "become_user",
    "changed_when", "check_mode", "collections", "connection", "debugger", "delay", "delegate_facts",
    "delegate_to", "diff", "environment", "failed_when", "ignore_errors", "ignore_unreachable", "listen",
    "loop", "loop_control", "module_defaults", "name", "no_log", "notify", "poll", "port", "register",
    "remote_user", "retries", "run_once", "tags", "throttle", "timeout", "until", "vars", "when",
}


def action_of(task: yaml.MappingNode) -> str:
    """Return the module name of a task mapping, with any collection prefix removed."""
    for key_node, _ in task.value:
        key = str(key_node.value)
        if key in KEYWORDS or key.startswith("with_") or key in BLOCK_KEYS:
            continue
        return key.rsplit(".", 1)[-1]
    return ""


def scalar_value(task: yaml.MappingNode, wanted: str) -> str | None:
    """Return the scalar value of a key in a task mapping, or None."""
    for key_node, value_node in task.value:
        if key_node.value == wanted and isinstance(value_node, yaml.ScalarNode):
            return str(value_node.value)
    return None


def walk(node: yaml.Node, found: list[yaml.MappingNode]) -> None:
    """Collect task mappings from a sequence node, descending into blocks."""
    if not isinstance(node, yaml.SequenceNode):
        return
    for task in node.value:
        if not isinstance(task, yaml.MappingNode):
            continue
        children = [value for key, value in task.value if key.value in BLOCK_KEYS]
        if children:
            for child in children:
                walk(child, found)
            continue
        if action_of(task) in IMPORT_ACTIONS:
            continue
        found.append(task)


def load_inventory(root: Path) -> dict[str, dict[str, Any]]:
    """Return every task and handler under root/roles keyed by ``roles/<role>/<kind>/<file>:<line>``."""
    inventory: dict[str, dict[str, Any]] = {}
    for path in sorted((root / "roles").glob("*/*/*.y*ml")):
        role, kind = path.parts[-3], path.parts[-2]
        if kind not in ("tasks", "handlers"):
            continue
        document = yaml.compose(path.read_text(encoding="utf-8"))
        tasks: list[yaml.MappingNode] = []
        if document is not None:
            walk(document, tasks)
        for task in tasks:
            relative = path.relative_to(root).as_posix()
            # PyYAML marks a block mapping at its first key, which is the line Ansible reports.
            line = task.start_mark.line + 1
            action = action_of(task)
            inventory[f"{relative}:{line}"] = {
                "role": role,
                "kind": kind,
                "file": relative,
                "line": line,
                "name": scalar_value(task, "name") or action,
                "action": action,
            }
    return inventory


def recorded_paths(jsonl_files: list[Path]) -> set[str]:
    """Return the distinct task paths found in task_coverage JSONL files."""
    paths: set[str] = set()
    for jsonl in jsonl_files:
        with jsonl.open(encoding="utf-8") as handle:
            for number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    paths.add(json.loads(line)["path"])
                except (json.JSONDecodeError, KeyError) as error:
                    raise SystemExit(f"{jsonl}:{number}: unreadable coverage record: {error!r}") from error
    return paths


def missing_from_inventory(inventory: dict[str, dict[str, Any]], jsonl_files: list[Path]) -> list[str]:
    """Return the runtime paths that the static inventory does not know about."""
    return sorted(recorded_paths(jsonl_files) - inventory.keys())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--check", type=Path, nargs="*", default=[], metavar="JSONL",
                        help="fail if any recorded runtime path is missing from the inventory")
    parser.add_argument("--output", type=Path, help="write the inventory as JSON, default is stdout")
    args = parser.parse_args()

    inventory = load_inventory(args.root)
    text = json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    elif not args.check:
        sys.stdout.write(text)

    if args.check:
        missing = missing_from_inventory(inventory, args.check)
        if missing:
            print(f"FAIL: {len(missing)} runtime task paths are not in the inventory:", file=sys.stderr)
            for path in missing:
                print(f"  {path}", file=sys.stderr)
            return 1
        print(f"OK: {len(recorded_paths(args.check))} runtime task paths, all in the {len(inventory)} task inventory")
    return 0


if __name__ == "__main__":
    sys.exit(main())

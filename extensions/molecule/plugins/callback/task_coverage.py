"""Callback plugin recording which role tasks ran, as JSON lines, for coverage reporting."""

from __future__ import annotations

DOCUMENTATION = """
    name: task_coverage
    type: aggregate
    short_description: Append one JSON line per role task result for coverage reporting
    description:
      - Writes one JSON object per task result and host to
        C(molecule-logs/<scenario>/task_coverage.jsonl) below the Molecule project directory.
      - Only tasks and handlers defined under C(roles/<role>/tasks) or C(roles/<role>/handlers) are recorded.
      - Verify and prepare playbooks can still run role task files, so every record carries a C(phase) and the
        report drops the verify and prepare phases.
      - Every record is a single O_APPEND write from the controller process, so it is safe with C(strategy free)
        and when several playbook runs append to the same file one after another.
      - A playbook named C(create*) truncates the file, which keeps a local rerun from mixing with stale data.
    requirements:
      - Enable with C(callbacks_enabled) and make the plugin directory known through C(callback_plugins).
      - Reads MOLECULE_PROJECT_DIRECTORY and MOLECULE_SCENARIO_NAME, or TASK_COVERAGE_FILE as an override.
"""

import json
import os
import re
import time
from pathlib import Path

from ansible.plugins.callback import CallbackBase

# Matches the absolute path of a task or handler inside any copy of the collection.
ROLE_PATH = re.compile(r".*/roles/(?P<role>[^/]+)/(?P<kind>tasks|handlers)/(?P<file>.+):(?P<line>\d+)$")


class CallbackModule(CallbackBase):
    """Record every role task result as one JSON line."""

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "task_coverage"
    CALLBACK_NEEDS_ENABLED = True

    def __init__(self) -> None:
        super().__init__()
        self._fd: int | None = None
        self._scenario = os.environ.get("MOLECULE_SCENARIO_NAME", "unknown")
        self._playbook = ""
        self._run = 1
        self._distribution: dict[str, str] = {}
        self._path = self._output_path()

    @staticmethod
    def _output_path() -> Path | None:
        override = os.environ.get("TASK_COVERAGE_FILE")
        if override:
            return Path(override)
        project = os.environ.get("MOLECULE_PROJECT_DIRECTORY")
        scenario = os.environ.get("MOLECULE_SCENARIO_NAME")
        if not project or not scenario:
            return None
        return Path(project) / "molecule-logs" / scenario / "task_coverage.jsonl"

    def _previous_runs(self) -> int:
        """Count the earlier runs of this playbook already in the file."""
        seen: set[str] = set()
        try:
            with self._path.open(encoding="utf-8") as handle:
                for line in handle:
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if record.get("playbook") == self._playbook:
                        seen.add(str(record.get("run_id")))
        except FileNotFoundError:
            pass
        return len(seen)

    def v2_playbook_on_start(self, playbook) -> None:
        if self._path is None:
            self._display.warning("task_coverage: MOLECULE_PROJECT_DIRECTORY or MOLECULE_SCENARIO_NAME is unset")
            return
        self._playbook = Path(playbook._file_name).stem
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if self._playbook.startswith("create"):
            self._path.write_text("", encoding="utf-8")
        self._run = self._previous_runs() + 1
        self._fd = os.open(self._path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)

    def _phase(self) -> str:
        if self._playbook == "converge":
            return {1: "converge", 2: "idempotence"}.get(self._run, f"converge-{self._run}")
        return self._playbook

    def _remember_distribution(self, host: str, result) -> None:
        facts = result._result.get("ansible_facts")
        if isinstance(facts, dict) and facts.get("ansible_distribution"):
            self._distribution[host] = str(facts["ansible_distribution"])

    def _record(self, result, status: str, ignored: bool = False) -> None:
        if self._fd is None:
            return
        task = result._task
        match = ROLE_PATH.match(task.get_path() or "")
        if match is None:
            return
        host = result._host.get_name()
        record = {
            "scenario": self._scenario,
            "host": host,
            "distribution": self._distribution.get(host, "unknown"),
            "path": f"roles/{match['role']}/{match['kind']}/{match['file']}:{match['line']}",
            "role": match["role"],
            "task": task.name or task.action,
            "status": status,
            "changed": bool(result._result.get("changed", False)),
            "ignored": ignored,
            "has_when": bool(task.when),
            "playbook": self._playbook,
            "run_id": f"{self._playbook}#{self._run}",
            "phase": self._phase(),
            "time": time.time(),
        }
        # One write per line keeps records whole when hosts report interleaved under strategy free.
        os.write(self._fd, (json.dumps(record, sort_keys=True) + "\n").encode("utf-8"))

    def v2_runner_on_ok(self, result) -> None:
        self._remember_distribution(result._host.get_name(), result)
        self._record(result, "ok")

    def v2_runner_on_failed(self, result, ignore_errors: bool = False) -> None:
        self._record(result, "failed", ignored=ignore_errors)

    def v2_runner_on_skipped(self, result) -> None:
        self._record(result, "skipped")

    def v2_runner_on_unreachable(self, result) -> None:
        self._record(result, "unreachable")

    def v2_playbook_on_stats(self, stats) -> None:
        if self._fd is not None:
            os.close(self._fd)
            self._fd = None

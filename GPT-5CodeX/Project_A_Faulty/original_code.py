"""Faulty directory analysis implementation that shells out to POSIX-only commands.

This module deliberately demonstrates a compatibility failure on Windows hosts by
invoking utilities such as ``ls`` and ``du`` via ``shell=True``. The lack of
portable fallbacks combined with unsafe string interpolation exposes both
platform-specific failures and injection risks.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


class CompatibilityIssue(RuntimeError):
    """Raised when the analysis cannot execute due to an environment mismatch."""


@dataclass
class AnalysisRequest:
    path: str
    include_hidden: bool
    max_depth: int
    operations: List[str]


def _ensure_supported_host() -> None:
    """Guard against executing on unsupported hosts."""

    if platform.system().lower().startswith("win"):
        raise CompatibilityIssue(
            "POSIX-only tooling not available on Windows hosts; no fallback path provided."
        )


def _read_operations(config: Dict[str, Any]) -> List[str]:
    operations = config.get("operations")
    if not operations:
        raise ValueError("At least one operation must be requested.")
    if not isinstance(operations, list) or not all(isinstance(op, str) for op in operations):
        raise TypeError("operations must be a list of strings")
    return operations


def _normalize_path(raw_path: Any) -> Path:
    if not isinstance(raw_path, str):
        raise TypeError("path must be provided as a string")
    path = Path(raw_path)
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path


def _run_command(command: str) -> str:
    """Execute a shell command that is only present on POSIX systems."""

    try:
        completed = subprocess.run(  # noqa: S603,S607 - intentional to show flaw
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:  # Command missing on the host
        raise CompatibilityIssue(
            "External command missing; host shell does not expose required POSIX tooling."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise CompatibilityIssue(
            f"Shell command failed with exit code {exc.returncode}: {exc.stderr.strip()}"
        ) from exc
    return completed.stdout


def _list_entries(path: Path, include_hidden: bool, max_depth: int) -> List[str]:
    flags = " -a" if include_hidden else ""
    depth_segment = ""
    if max_depth > 1:
        depth_segment = f"; find '{path}' -maxdepth {max_depth - 1} -type f"
    command = f"ls{flags} '{path}'{depth_segment}"
    output = _run_command(command)
    entries = [line.strip() for line in output.splitlines() if line.strip()]
    return entries


def _calculate_total_size(path: Path) -> int:
    command = f"du -sb '{path}'"
    output = _run_command(command)
    first_line = output.splitlines()[0]
    size_token = first_line.split()[0]
    return int(size_token)


def run_analysis(config: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(config, dict):
        raise TypeError("Configuration must be supplied as a dictionary")

    request = AnalysisRequest(
        path=config.get("path"),
        include_hidden=bool(config.get("include_hidden", False)),
        max_depth=int(config.get("max_depth", 1)),
        operations=_read_operations(config),
    )

    target = _normalize_path(request.path)

    _ensure_supported_host()

    result: Dict[str, Any] = {"path": str(target)}

    if "list_entries" in request.operations:
        result["entries"] = _list_entries(target, request.include_hidden, request.max_depth)
    if "total_size" in request.operations:
        result["total_size_bytes"] = _calculate_total_size(target)

    return result


def run_from_file(path: str) -> Dict[str, Any]:
    """Convenience helper used by the run script for reproducibility."""

    with open(path, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    return run_analysis(config)


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Execute the faulty analysis workflow")
    parser.add_argument("config", help="Path to an input JSON configuration file")
    args = parser.parse_args()

    try:
        payload = run_from_file(args.config)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"ERROR: {exc}")
        raise SystemExit(1) from exc
    else:
        print(json.dumps(payload, indent=2))

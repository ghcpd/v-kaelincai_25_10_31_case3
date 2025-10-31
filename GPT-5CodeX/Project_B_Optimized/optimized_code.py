"""Portable directory analysis implementation with compatibility hardening.

The updated workflow replaces shell-dependent subprocess calls with standard
library primitives so it works consistently on Windows, macOS, and Linux. It
also mitigates shell injection risk and supports depth-limited traversal while
respecting hidden file policies.
"""

from __future__ import annotations

import ctypes
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

FILE_ATTRIBUTE_HIDDEN = 0x02


class AnalysisError(RuntimeError):
    """Base class for analysis-related failures."""


class CompatibilityIssue(AnalysisError):
    """Raised when the workflow detects an unavoidable compatibility regression."""


@dataclass
class AnalysisRequest:
    path: Path
    include_hidden: bool
    max_depth: int
    operations: List[str]


def _validate_operations(config: Dict[str, Any]) -> List[str]:
    operations = config.get("operations")
    if not operations:
        raise ValueError("At least one operation must be requested.")
    if not isinstance(operations, list) or not all(isinstance(op, str) for op in operations):
        raise TypeError("operations must be a list of strings")
    return operations


def _resolve_path(raw_path: Any) -> Path:
    if isinstance(raw_path, (str, os.PathLike)):
        path = Path(raw_path)
    else:
        raise TypeError("path must be provided as a string or Path")
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path.resolve()


def _is_hidden(path: Path) -> bool:
    name = path.name
    if name.startswith(".") and name not in {".", ".."}:
        return True
    if sys.platform.startswith("win"):
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        except AttributeError as exc:  # pragma: no cover - only during interpreter edge cases
            raise CompatibilityIssue("Win32 API not available for hidden attribute detection") from exc
        if attrs == -1:
            return False
        return bool(attrs & FILE_ATTRIBUTE_HIDDEN)
    return False


def _should_include(path: Path, include_hidden: bool) -> bool:
    return include_hidden or not _is_hidden(path)


def _list_entries(request: AnalysisRequest) -> List[str]:
    base = request.path
    max_depth = max(1, request.max_depth)
    collected: List[str] = []
    base_depth = len(base.parts)

    for root, dirs, files in os.walk(base):
        root_path = Path(root)
        relative_depth = len(root_path.parts) - base_depth
        if relative_depth >= max_depth:
            dirs[:] = []
            continue

        # Filter directories in-place to respect hidden flag.
        pruned_dirs = []
        for directory in list(dirs):
            directory_path = root_path / directory
            if _should_include(directory_path, request.include_hidden):
                pruned_dirs.append(directory)
                collected.append(str(directory_path.relative_to(base)))
        dirs[:] = pruned_dirs

        for filename in files:
            file_path = root_path / filename
            if not _should_include(file_path, request.include_hidden):
                continue
            if len(file_path.relative_to(base).parts) > max_depth:
                continue
            collected.append(str(file_path.relative_to(base)))

    collected.sort()
    return collected


def _calculate_total_size(request: AnalysisRequest) -> int:
    max_depth = max(1, request.max_depth)
    total = 0
    for handle in request.path.rglob("*"):
        if handle.is_dir():
            continue
        relative = handle.relative_to(request.path)
        if len(relative.parts) > max_depth:
            continue
        if not _should_include(handle, request.include_hidden):
            continue
        total += handle.stat().st_size
    return total


def run_analysis(config: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(config, dict):
        raise TypeError("Configuration must be supplied as a dictionary")

    path = _resolve_path(config.get("path"))
    include_hidden = bool(config.get("include_hidden", False))
    max_depth = int(config.get("max_depth", 1))
    operations = _validate_operations(config)

    request = AnalysisRequest(
        path=path,
        include_hidden=include_hidden,
        max_depth=max_depth,
        operations=operations,
    )

    result: Dict[str, Any] = {"path": str(path)}

    if "list_entries" in operations:
        result["entries"] = _list_entries(request)
    if "total_size" in operations:
        result["total_size_bytes"] = _calculate_total_size(request)

    return result


def run_from_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    return run_analysis(config)


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Execute the hardened analysis workflow")
    parser.add_argument("config", help="Path to an input JSON configuration file")
    args = parser.parse_args()

    payload = run_from_file(args.config)
    print(json.dumps(payload, indent=2))

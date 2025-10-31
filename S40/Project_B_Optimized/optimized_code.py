"""Optimized manifest processor resilient to schema evolution and OS variance."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import PurePath
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


class CompatibilityError(RuntimeError):
    """Raised when critical compatibility violations are detected."""


@dataclass
class DeploymentPlan:
    name: str
    artifact_path: str
    hash: str
    hooks: Dict[str, str]
    schema_version: str
    diagnostics: Dict[str, Any]


SUPPORTED_MAJOR_VERSIONS = {"1", "2"}
DEFAULT_OS_ALIAS = {"windows": "nt", "linux": "posix", "darwin": "posix"}


def _coerce_payload(payload: Any) -> Mapping[str, Any]:
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")

    if isinstance(payload, str):
        return json.loads(payload)

    if isinstance(payload, Mapping):
        return payload

    raise TypeError(
        "Deployment manifest payload must be a JSON string, mapping, or bytes."
    )


def _normalise_os(os_hint: Optional[str]) -> str:
    if not os_hint:
        return os.name

    if os_hint.lower() in {"nt", "posix"}:
        return os_hint.lower()

    return DEFAULT_OS_ALIAS.get(os_hint.lower(), os_hint.lower())


def _select_artifact(data: Mapping[str, Any], target_os: str) -> tuple[str, str]:
    # schema 1.x uses flat artifact_path/hash
    if "artifact_path" in data and "hash" in data:
        return data["artifact_path"], data["hash"]

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, Mapping):
        raise CompatibilityError("Manifest missing 'artifacts' mapping for schema >=2.0")

    # Accept synonyms and fallbacks for OS key resolution
    candidates: Iterable[str] = (target_os, "default", "fallback")
    for key in candidates:
        if key in artifacts:
            selected = artifacts[key]
            if not isinstance(selected, Mapping):
                raise CompatibilityError(f"Artifact entry for '{key}' must be a mapping")
            path = selected.get("path")
            digest = selected.get("hash") or selected.get("digest")
            if not path or not digest:
                raise CompatibilityError(f"Artifact entry for '{key}' missing path/hash")
            return path, digest

    raise CompatibilityError(
        f"Could not find artifact for target '{target_os}'. Available keys: {list(artifacts)}"
    )


def _normalise_path(path: str, target_os: str) -> str:
    # Use PurePath for deterministic formatting while respecting target OS semantics.
    if target_os == "nt":
        converted = str(PurePath(path).as_posix()).replace("/", "\\")
    else:
        converted = str(PurePath(path).as_posix())
    return converted


def _parse_hooks(raw_hooks: Any) -> Dict[str, str]:
    hooks: Dict[str, str] = {}
    if raw_hooks is None:
        return hooks

    if isinstance(raw_hooks, Iterable) and not isinstance(raw_hooks, (str, bytes)):
        for entry in raw_hooks:
            if isinstance(entry, Mapping):
                name = entry.get("name")
                path = entry.get("path") or entry.get("command")
                if not name or not path:
                    raise CompatibilityError("Hook object missing 'name' or 'path'")
            elif isinstance(entry, str):
                if ":" not in entry:
                    raise CompatibilityError(
                        "String hook entry must be formatted as 'name:path'."
                    )
                name, path = entry.split(":", 1)
            else:
                raise CompatibilityError(f"Unsupported hook entry type: {type(entry).__name__}")

            hooks[name] = str(path)
        return hooks

    raise CompatibilityError("Hooks must be a list of mappings or colon-delimited strings")


def prepare_deployment_plan(payload: Any, *, target_os: Optional[str] = None) -> DeploymentPlan:
    manifest = _coerce_payload(payload)
    schema_version = str(manifest.get("schema_version", "1.0"))
    major = schema_version.split(".", 1)[0]
    if major not in SUPPORTED_MAJOR_VERSIONS:
        raise CompatibilityError(f"Unsupported schema major version '{major}'.")

    normalised_os = _normalise_os(target_os)
    artifact_raw, digest = _select_artifact(manifest, normalised_os)
    artifact_path = _normalise_path(artifact_raw, normalised_os)

    hooks = _parse_hooks(manifest.get("hooks"))

    diagnostics: Dict[str, Any] = {
        "schema_version": schema_version,
        "target_os": normalised_os,
        "timestamp": time.time(),
        "artifact_source": artifact_raw,
        "hooks_count": len(hooks),
    }

    # Optional compatibility metadata for clients needing introspection
    if "metadata" in manifest and isinstance(manifest["metadata"], MutableMapping):
        diagnostics["metadata_keys"] = list(manifest["metadata"].keys())

    return DeploymentPlan(
        name=str(manifest.get("name", "unknown")),
        artifact_path=artifact_path,
        hash=str(digest),
        hooks=hooks,
        schema_version=schema_version,
        diagnostics=diagnostics,
    )


__all__ = ["CompatibilityError", "DeploymentPlan", "prepare_deployment_plan"]

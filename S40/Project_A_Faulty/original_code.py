"""Faulty manifest processor demonstrating compatibility issues.

This module intentionally contains brittle assumptions about the structure of the
incoming deployment manifest. It only supports schema version "1.0" and expects
single-path artifacts, making it incompatible with providers that upgraded to
schema "2.x" where artifacts are path maps keyed by operating system.

The implementation also rejects non-string payload objects and lacks resilience
for additional metadata fields introduced in newer protocol revisions.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict


EXPECTED_SCHEMA_VERSION = "1.0"


class CompatibilityError(RuntimeError):
    """Domain-specific error highlighting compatibility breakages."""


@dataclass
class DeploymentPlan:
    name: str
    artifact_path: str
    hash: str
    hooks: Dict[str, str]


def _ensure_payload_is_string(payload: Any) -> str:
    if not isinstance(payload, str):
        raise TypeError(
            "The deployment manifest must be provided as a JSON string. "
            "Bytes, dicts, and other objects are not supported in this version."
        )
    return payload


def _parse_payload(payload: str) -> Dict[str, Any]:
    data = json.loads(payload)
    version = data.get("schema_version")
    if version != EXPECTED_SCHEMA_VERSION:
        raise CompatibilityError(
            f"Unsupported manifest schema '{version}'. Expected '{EXPECTED_SCHEMA_VERSION}'."
        )
    return data


def _normalise_artifact_path(raw_path: str) -> str:
    if os.name == "nt":
        return raw_path.replace("/", "\\")
    return raw_path.replace("\\", "/")


def prepare_deployment_plan(payload: Any, target_os: str | None = None) -> DeploymentPlan:
    """Produce a deployment plan for the caller's platform.

    Args:
        payload: JSON string describing the deployment manifest.
        target_os: Optional override for the current OS ("nt" or "posix").

    Returns:
        DeploymentPlan: Selected artifact and hook wiring.

    Raises:
        TypeError: If the payload is not a string.
        CompatibilityError: If the schema version is not exactly 1.0.
        KeyError: If required keys are missing (due to schema drift).
    """

    manifest_str = _ensure_payload_is_string(payload)
    data = _parse_payload(manifest_str)

    artifact_path = data["artifact_path"]  # Raises KeyError for schema >=2.0
    artifact_hash = data["hash"]

    selected_os = target_os or os.name
    if selected_os not in {"nt", "posix"}:
        raise CompatibilityError(f"Unsupported target OS '{selected_os}'")

    normalised_path = _normalise_artifact_path(artifact_path)

    hooks = {}
    for hook in data.get("hooks", []):
        # schema 1.0 delivered hooks as "name:path" strings; new schema changed
        # to objects. This parser still assumes the old layout.
        name, path = hook.split(":", 1)
        hooks[name] = path

    return DeploymentPlan(
        name=data["name"],
        artifact_path=normalised_path,
        hash=artifact_hash,
        hooks=hooks,
    )


__all__ = ["CompatibilityError", "DeploymentPlan", "prepare_deployment_plan"]

"""Tests exposing compatibility issues in the faulty implementation."""

from __future__ import annotations

import json
import os
import pathlib
import sys
import time
from typing import Any, Dict

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from original_code import CompatibilityError, prepare_deployment_plan


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def load_test_cases() -> Dict[str, Any]:
    data_path = FIXTURE_DIR / "test_data.json"
    with data_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.mark.parametrize("case_name", list(load_test_cases().keys()))
def test_prepare_deployment_plan(case_name: str) -> None:
    cases = load_test_cases()
    case = cases[case_name]

    payload = case["input"]
    expected_outcome = case["expected_outcome"]

    start = time.perf_counter()
    try:
        plan = prepare_deployment_plan(payload, case.get("target_os"))
    except Exception as exc:  # broad to capture TypeError + CompatibilityError
        duration = time.perf_counter() - start
        if expected_outcome == "pass":
            raise AssertionError(
                f"Case '{case_name}' expected success but failed with {exc!r}"
            ) from exc

        # Ensure the exception type matches the expectation note
        expected_error = case.get("expected_error_type")
        if expected_error and expected_error != exc.__class__.__name__:
            raise AssertionError(
                f"Case '{case_name}' expected {expected_error} but got {exc.__class__.__name__}"
            ) from exc

        case_result = {
            "status": "fail",
            "duration": duration,
            "error": str(exc),
        }
    else:
        duration = time.perf_counter() - start
        if expected_outcome != "pass":
            raise AssertionError(
                f"Case '{case_name}' expected failure but succeeded: {plan}"
            )

        # For faulty implementation, we intentionally capture the limited output
        case_result = {
            "status": "pass",
            "duration": duration,
            "plan": {
                "name": plan.name,
                "artifact_path": plan.artifact_path,
                "hash": plan.hash,
                "hooks": plan.hooks,
            },
        }

    (FIXTURE_DIR / "log_original.txt").write_text(
        json.dumps({case_name: case_result}, indent=2), encoding="utf-8"
    )

    with (FIXTURE_DIR / "time_original.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"{case_name}: {duration:.6f}\n")


def test_environment_expectations() -> None:
    # This highlights platform-specific assumptions.
    if os.name != "nt":
        # On non-Windows systems, backslash conversions break expectations.
        with pytest.raises(KeyError):
            prepare_deployment_plan(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "name": "demo",
                        "artifact_path": "C:/app/bundle.zip",
                        "hash": "123",
                        "hooks": ["install:C:/hooks/install.bat"],
                    }
                ),
                target_os="posix",
            )

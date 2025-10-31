"""Comprehensive regression tests validating optimized manifest processor."""

from __future__ import annotations

import json
import pathlib
import time
from typing import Any, Dict

import pytest

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def load_cases() -> Dict[str, Any]:
    with (FIXTURE_DIR / "test_data.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.mark.parametrize("case_name", list(load_cases().keys()))
def test_prepare_deployment_plan(case_name: str) -> None:
    from optimized_code import CompatibilityError, prepare_deployment_plan

    cases = load_cases()
    case = cases[case_name]
    payload = case["input"]
    target_os = case.get("target_os")
    expected_outcome = case["expected_outcome"]

    start = time.perf_counter()

    try:
        plan = prepare_deployment_plan(payload, target_os=target_os)
    except CompatibilityError as exc:
        duration = time.perf_counter() - start
        if expected_outcome == "pass":
            raise AssertionError(
                f"Case '{case_name}' should have succeeded but failed: {exc}"
            ) from exc

        expected_error = case.get("expected_error_type")
        if expected_error and expected_error != exc.__class__.__name__:
            raise AssertionError(
                f"Case '{case_name}' expected {expected_error} but got {exc.__class__.__name__}"
            ) from exc

        log_entry = {
            "status": "fail",
            "error": str(exc),
            "duration": duration,
        }
    else:
        duration = time.perf_counter() - start
        if expected_outcome != "pass":
            raise AssertionError(
                f"Case '{case_name}' expected failure but produced plan {plan}"
            )

        log_entry = {
            "status": "pass",
            "artifact_path": plan.artifact_path,
            "hooks": plan.hooks,
            "schema_version": plan.schema_version,
            "duration": duration,
        }

    with (FIXTURE_DIR / "log_optimized.txt").open("a", encoding="utf-8") as handle:
        json.dump({case_name: log_entry}, handle)
        handle.write("\n")

    with (FIXTURE_DIR / "time_optimized.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"{case_name}: {duration:.6f}\n")


def test_invalid_hook_entries() -> None:
    from optimized_code import CompatibilityError, prepare_deployment_plan

    with pytest.raises(CompatibilityError):
        prepare_deployment_plan(
            {
                "schema_version": "2.0",
                "name": "demo",
                "artifacts": {"default": {"path": "bundle.zip", "hash": "dead"}},
                "hooks": [123],
            }
        )

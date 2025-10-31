import json
import os
from pathlib import Path
from typing import Any, Dict
from unittest import mock

import pytest

import original_code

FIXTURE_PATH = Path(__file__).parent / "test_data.json"


def load_test_cases():
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    for case in data:
        yield case["name"], case


def fake_response(case: Dict[str, Any]):
    class DummyResponse:
        status_code = 200

        def __init__(self, payload, status=200):
            self._payload = payload
            self.status_code = status

        def raise_for_status(self):
            if self.status_code >= 400:
                raise original_code.requests.HTTPError(f"HTTP {self.status_code}")

        def json(self):
            return self._payload

    compatibility = case["compatibility_issue"]
    name = case["name"]
    if name == "normal_v2_response":
        payload = {
            "results": [
                {
                    "task_id": "task-normal-001",
                    "status": {"code": "OK", "detail": "processed"},
                    "status_code": None,
                    "completed_at": "2025-10-31T12:30:00Z",
                    "retry_after": None,
                }
            ]
        }
    elif name == "rate_limited_v2":
        payload = {
            "results": [
                {
                    "task_id": "task-rate-002",
                    "status": {"code": "RATE_LIMIT", "detail": "slow down"},
                    "status_code": None,
                    "completed_at": "2025-10-31T12:30:00Z",
                    "retry_after": "PT30S",
                }
            ]
        }
    elif name == "timestamp_edge_case":
        payload = {
            "results": [
                {
                    "task_id": "task-time-003",
                    "status": {"code": "OK", "detail": "processed"},
                    "status_code": 200,
                    "completed_at": "2025-10-31T00:00:00+00:00",
                }
            ]
        }
    elif name == "malformed_payload":
        return DummyResponse(
            {
                "errors": [
                    {
                        "code": "INVALID_PAYLOAD",
                        "detail": "Null payload not allowed",
                        "field": "payload",
                    }
                ]
            },
            status=400,
        )
    else:  # complex_nested_batch
        payload = {
            "results": [
                {
                    "task_id": "task-nested-005",
                    "status": {"code": "OK", "detail": "processed"},
                    "status_code": 200,
                    "completed_at": "2025-10-31T12:30:00+09:00",
                    "metrics": {"latency_ms": "12.5"},
                }
            ]
        }
    return DummyResponse(payload)


@pytest.mark.parametrize("name,case", list(load_test_cases()))
def test_faulty_client_incompatibility(name, case):
    batch = case["input"]["batch"]
    response = fake_response(case)
    with mock.patch("original_code.requests.post", return_value=response):
        outcome = original_code.measure_processing(batch)

    if case["expected_result"] == "failure":
        assert outcome["success"] is False, f"Expected failure for {name}"
        assert outcome["error"], "Error message should be present"
    else:
        assert outcome["success"] is True, f"Expected success for {name}"

import json
from pathlib import Path
from typing import Any, Dict
from unittest import mock

import pytest

import optimized_code

FIXTURE_PATH = Path(__file__).parent / "test_data.json"


def load_test_cases():
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    for case in data:
        yield case["name"], case


def build_response(case: Dict[str, Any]):
    class DummyResponse:
        def __init__(self, payload, status_code=200):
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code >= 400:
                raise optimized_code.requests.HTTPError(response=self)

        def json(self):
            return self._payload

    name = case["name"]
    if name == "normal_v2_response":
        payload = {
            "results": [
                {
                    "task_id": "task-normal-001",
                    "status": {"code": "OK", "detail": "processed"},
                    "completed_at": "2025-10-31T12:30:00Z",
                    "metrics": {"latency_ms": 15.2},
                }
            ]
        }
        return DummyResponse(payload)
    if name == "rate_limited_v2":
        payload = {
            "results": [
                {
                    "task_id": "task-rate-002",
                    "status": {"code": "RATE_LIMIT", "detail": "slow down"},
                    "retry_after": "PT30S",
                    "completed_at": "2025-10-31T12:30:00Z",
                }
            ]
        }
        return DummyResponse(payload)
    if name == "timestamp_edge_case":
        payload = {
            "results": [
                {
                    "task_id": "task-time-003",
                    "status": {"code": "OK", "detail": "processed"},
                    "completed_at": "2025-10-31T00:00:00+00:00",
                }
            ]
        }
        return DummyResponse(payload)
    if name == "malformed_payload":
        payload = {
            "results": [],
            "errors": [
                {
                    "code": "INVALID_PAYLOAD",
                    "detail": "Null payload not allowed",
                    "field": "payload",
                }
            ],
        }
        return DummyResponse(payload, status_code=200)
    payload = {
        "results": [
            {
                "task_id": "task-nested-005",
                "status": {"code": "OK", "detail": "processed"},
                "completed_at": "2025-10-31T12:30:00+09:00",
                "metrics": {"latency_ms": "12.5"},
                "timezone": "Asia/Tokyo",
            }
        ]
    }
    return DummyResponse(payload)


@pytest.mark.parametrize("name,case", list(load_test_cases()))
def test_optimized_client(name, case):
    batch = case["input"]["batch"]
    response = build_response(case)
    with mock.patch("optimized_code.requests.post", return_value=response):
        outcome = optimized_code.measure_processing(batch)

    assert outcome["success"] is True, outcome["error"]
    assert outcome["results"], "Results should not be empty"
    first = outcome["results"][0]
    assert first["task_id"].startswith("task-"), "Task ID should propagate"
    assert isinstance(first["completed_at"], optimized_code.datetime)
    if case["name"] == "rate_limited_v2":
        assert first["retry_after_seconds"] == 30
    if case["name"] == "complex_nested_batch":
        assert first["metrics"]["latency_ms"] == pytest.approx(12.5, rel=1e-3)


@pytest.mark.parametrize("invalid_timestamp", [None, [], {}])
def test_invalid_timestamp_rejected(invalid_timestamp):
    batch = [{"task_id": "bad", "payload": {}, "priority": 1}]
    payload = {
        "results": [
            {
                "task_id": "bad",
                "status": {"code": "OK", "detail": "processed"},
                "completed_at": invalid_timestamp,
            }
        ]
    }
    response = build_response({"name": "normal_v2_response", "input": {"batch": batch}})
    response._payload = payload
    with mock.patch("optimized_code.requests.post", return_value=response):
        outcome = optimized_code.measure_processing(batch)
    assert outcome["success"] is False
    assert "timestamp" in outcome["error"].lower()

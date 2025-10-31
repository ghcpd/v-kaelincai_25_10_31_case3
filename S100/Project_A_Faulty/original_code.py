import json
import time
from datetime import datetime
from typing import Any, Dict, List

import requests

API_ENDPOINT = "https://api.vendor.example.com/v2/process"


def _serialize_payload(batch: List[Dict[str, Any]]) -> str:
    # Faulty: assumes ASCII output and dumps manually instead of using requests json param
    return json.dumps({"tasks": batch}, ensure_ascii=True)


def _parse_v1_status(status_code: int) -> Dict[str, Any]:
    if status_code == 200:
        return {"status": "ok", "detail": "processed"}
    if status_code == 429:
        return {"status": "retry", "detail": "rate limited"}
    return {"status": "error", "detail": f"unexpected code {status_code}"}


def _send_request(serialized: str) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        # Faulty: missing capability negotiation header required by v2 endpoint
    }
    response = requests.post(API_ENDPOINT, data=serialized, headers=headers, timeout=2)
    response.raise_for_status()
    return response.json()


def process_batch(batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    serialized = _serialize_payload(batch)
    raw_response = _send_request(serialized)

    results: List[Dict[str, Any]] = []
    for item in raw_response["results"]:
        # Faulty: expects v1 structure with integer status_code and epoch timestamp
        status_info = _parse_v1_status(int(item["status_code"]))
        completed_at_epoch = int(item["completed_at"])  # raises ValueError for RFC3339 strings
        completed_at = datetime.fromtimestamp(completed_at_epoch)
        results.append({
            "task_id": item["task_id"],
            "status": status_info["status"],
            "detail": status_info["detail"],
            "completed_at": completed_at,
            "retry_after": item.get("retry_after", 0),
        })
    return results


def measure_processing(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    start = time.time()
    try:
        results = process_batch(batch)
        success = True
    except Exception as exc:  # broad except to illustrate failure
        results = []
        success = False
        error = str(exc)
    else:
        error = ""
    duration = time.time() - start
    return {
        "success": success,
        "results": results,
        "error": error,
        "duration": duration,
    }


if __name__ == "__main__":
    with open("input_data.json", "r", encoding="utf-8") as fh:
        payload = json.load(fh)["batch"]
    outcome = measure_processing(payload)
    print(json.dumps(outcome, default=str, indent=2))

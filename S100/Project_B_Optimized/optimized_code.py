import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from dateutil import parser as date_parser

API_ENDPOINT = "https://api.vendor.example.com/v2/process"
API_FALLBACK_ENDPOINT = "https://api.vendor.example.com/v1/process"


@dataclass
class CapabilityConfig:
    accept_v2: bool = True
    accept_v1_fallback: bool = True
    supported_features: Iterable[str] = ("structured-status", "rfc3339-timestamps", "retry-after")


def _serialize_payload(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"tasks": batch, "requested_at": datetime.now(timezone.utc).isoformat()}


def _normalize_timestamp(value: Any) -> datetime:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        try:
            dt = date_parser.isoparse(value)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Unable to parse timestamp: {value}") from exc
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    raise TypeError(f"Unsupported timestamp type: {type(value)!r}")


def _prepare_headers(capabilities: CapabilityConfig) -> Dict[str, str]:
    caps = {
        "accept_v2": capabilities.accept_v2,
        "accept_v1_fallback": capabilities.accept_v1_fallback,
        "features": list(capabilities.supported_features),
    }
    return {
        "Content-Type": "application/json",
        "X-Client-Capabilities": json.dumps(caps, separators=(",", ":")),
        "User-Agent": "compat-client/2.0",
    }


def _send_request(payload: Dict[str, Any], *, capabilities: CapabilityConfig) -> Dict[str, Any]:
    headers = _prepare_headers(capabilities)
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as err:
        status = err.response.status_code if err.response else None
        if status == 400 and capabilities.accept_v1_fallback:
            fallback_response = requests.post(
                API_FALLBACK_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=5,
            )
            fallback_response.raise_for_status()
            return fallback_response.json()
        raise


def _coerce_status(entry: Dict[str, Any]) -> Dict[str, Any]:
    status_obj = entry.get("status")
    status_code = entry.get("status_code")
    detail = entry.get("detail")
    if isinstance(status_obj, dict):
        code = status_obj.get("code") or status_code or "UNKNOWN"
        detail = status_obj.get("detail") or detail or ""
    else:
        # Legacy integer codes
        mapping = {200: ("OK", "processed"), 429: ("RETRY", "rate limited")}
        code, detail = mapping.get(status_code, ("ERROR", f"unexpected code {status_code}"))
    return {"code": code, "detail": detail}


def _coerce_retry_after(entry: Dict[str, Any]) -> Optional[int]:
    retry_after = entry.get("retry_after")
    if retry_after is None:
        return None
    if isinstance(retry_after, (int, float)):
        return int(retry_after)
    if isinstance(retry_after, str):
        # Parse ISO duration PTxxS
        if retry_after.startswith("PT") and retry_after.endswith("S"):
            return int(float(retry_after[2:-1]))
        raise ValueError(f"Unrecognized retry_after format: {retry_after}")
    raise TypeError("retry_after must be numeric or ISO duration string")


def process_batch(batch: List[Dict[str, Any]], *, capabilities: Optional[CapabilityConfig] = None) -> List[Dict[str, Any]]:
    capabilities = capabilities or CapabilityConfig()
    payload = _serialize_payload(batch)
    raw_response = _send_request(payload, capabilities=capabilities)

    results: List[Dict[str, Any]] = []
    for entry in raw_response.get("results", []):
        status = _coerce_status(entry)
        completed_at = _normalize_timestamp(entry.get("completed_at"))
        tz = entry.get("timezone")
        if tz and ZoneInfo is not None:
            try:
                completed_at = completed_at.astimezone(ZoneInfo(tz))
            except Exception:  # pragma: no cover - fallback to original timezone
                pass
        metrics = entry.get("metrics", {})
        if isinstance(metrics, dict):
            normalized_metrics = {k: float(v) if isinstance(v, str) and v.replace(".", "", 1).isdigit() else v for k, v in metrics.items()}
        else:
            normalized_metrics = {}
        results.append({
            "task_id": entry.get("task_id", ""),
            "status": status["code"],
            "detail": status["detail"],
            "completed_at": completed_at,
            "retry_after_seconds": _coerce_retry_after(entry),
            "metrics": normalized_metrics,
        })
    return results


def measure_processing(batch: List[Dict[str, Any]], *, capabilities: Optional[CapabilityConfig] = None) -> Dict[str, Any]:
    start = time.time()
    try:
        results = process_batch(batch, capabilities=capabilities)
        success = True
        error = ""
    except Exception as exc:
        results = []
        success = False
        error = str(exc)
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

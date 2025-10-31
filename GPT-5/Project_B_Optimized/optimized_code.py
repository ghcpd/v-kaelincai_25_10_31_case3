"""Optimized, compatibility-hardened implementation.
Fixes:
- Robust timestamp parsing (supports 'Z') via dateutil.
- Graceful fallback if orjson unavailable.
- Deterministic canonicalization: sorted IDs and sorted keys.
- Accepts bytes or dict input; validates structure and types.
- Handles non-string IDs by coercion.
"""
import json
import hashlib
from typing import Any, Dict

try:
    import orjson  # optional
    HAS_ORJSON = True
except ImportError:  # pragma: no cover
    HAS_ORJSON = False

from dateutil import parser as date_parser


def _parse_timestamp(ts: Any):
    if isinstance(ts, bytes):
        ts = ts.decode()
    if not isinstance(ts, str):
        raise ValueError("Timestamp must be a string")
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        return date_parser.isoparse(ts)
    except Exception as e:  # pragma: no cover
        raise ValueError(f"Invalid timestamp '{ts}': {e}")


def process(data: Any) -> Dict[str, Any]:
    if isinstance(data, bytes):
        data = json.loads(data.decode())
    if not isinstance(data, dict) or "records" not in data:
        raise ValueError("Input must be dict with 'records'")
    records = data["records"]
    if not isinstance(records, list):
        raise ValueError("'records' must be a list")
    ids = []
    payload_map = {}
    for rec in records:
        if not isinstance(rec, dict):
            raise ValueError("Each record must be dict")
        rid = rec.get("id")
        if rid is None:
            raise ValueError("Record missing 'id'")
        rid = str(rid)
        ts = rec.get("timestamp")
        if ts is None:
            raise ValueError("Record missing 'timestamp'")
        _parse_timestamp(ts)  # validation only
        ids.append(rid)
        payload_map[rid] = rec.get("payload")
    ids_sorted = sorted(ids)
    ordered_payloads = [payload_map[i] for i in ids_sorted]
    if HAS_ORJSON:
        canonical_bytes = orjson.dumps(ordered_payloads, option=orjson.OPT_SORT_KEYS)
        canonical_str = canonical_bytes.decode()
    else:
        canonical_str = json.dumps(ordered_payloads, sort_keys=True, separators=(',', ':'))
    digest = hashlib.sha256(canonical_str.encode()).hexdigest()
    return {"record_count": len(records), "ids": ids_sorted, "payload_digest": digest}


def main():  # pragma: no cover
    import pathlib, sys
    if len(sys.argv) < 2:
        print("Usage: python optimized_code.py <input_json_path>")
        return 1
    path = pathlib.Path(sys.argv[1])
    data = json.loads(path.read_text())
    try:
        out = process(data)
        print(json.dumps(out, indent=2))
    except Exception as e:
        print(f"ERROR: {e}")
        return 2
    return 0

if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())

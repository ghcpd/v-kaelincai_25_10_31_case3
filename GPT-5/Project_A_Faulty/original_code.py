"""Faulty implementation illustrating compatibility issues.
Issues:
- Uses datetime.fromisoformat which fails on 'Z' timezone suffix in some Python versions.
- Assumes record 'id' is a lowercase-able string.
- Relies on dict/list ordering for canonicalization (unstable across older Python versions).
- Hard dependency on orjson; fails if wheel unavailable (e.g., certain platforms/Python versions).
"""
import json
import hashlib
import datetime

try:
    import orjson  # hard dependency; failure if not installed
except ImportError as e:
    raise RuntimeError("orjson not available; faulty implementation requires it") from e


def process(data):
    """Process records: produce count, ids, and digest.
    Faults:
      - Lowercases IDs assuming str.
      - Fails on timestamps ending with 'Z'.
      - Unstable canonicalization (no sorting).
    """
    if not isinstance(data, dict) or "records" not in data:
        raise ValueError("Input must be dict with 'records'")
    records = data["records"]
    ids = []
    payloads = []
    for rec in records:
        ts = rec["timestamp"]  # may raise KeyError intentionally
        # Will raise ValueError on 'Z' suffix
        _ = datetime.datetime.fromisoformat(ts)  # compatibility issue
        rid = rec["id"].lower()  # fails if id not str
        ids.append(rid)
        payloads.append(rec.get("payload"))
    # Canonicalization without sorting keys or IDs
    canonical_bytes = orjson.dumps(payloads)
    canonical_str = canonical_bytes.decode()
    digest = hashlib.sha256(canonical_str.encode()).hexdigest()
    return {"record_count": len(records), "ids": ids, "payload_digest": digest}


def main():
    import pathlib
    import sys
    if len(sys.argv) < 2:
        print("Usage: python original_code.py <input_json_path>")
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

if __name__ == "__main__":
    raise SystemExit(main())

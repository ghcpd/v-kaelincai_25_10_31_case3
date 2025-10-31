# Compatibility Evaluation Report

## Overview
This experiment benchmarks two microservice client implementations against an upgraded vendor API (`v2`). Project A represents the legacy, incompatible client, while Project B introduces protocol-aware enhancements. All scenarios rely on generated test cases stored in `test_data.json` and executed via project-specific pytest suites.

## Side-by-Side Test Results
| Test Case | Compatibility Issue | Project A Result | Project B Result |
|-----------|---------------------|------------------|------------------|
| normal_v2_response | API version mismatch | ❌ Exception: `KeyError('status_code')` | ✅ Parsed structured status |
| rate_limited_v2 | Missing header negotiation | ❌ Exception: `HTTPError` | ✅ Respected retry metadata |
| timestamp_edge_case | RFC3339 timestamp handling | ❌ Exception: `ValueError` | ✅ Normalized timezone-aware datetime |
| malformed_payload | Structured validation errors | ❌ Exception: `HTTPError` | ✅ Captured errors, returned empty results |
| complex_nested_batch | Nested metrics type coercion | ❌ Exception: `ValueError` | ✅ Converted metrics to floats |

## Metrics Summary
| Metric | Project A | Project B | Improvement |
|--------|-----------|-----------|-------------|
| Compatibility Pass Rate | 0/5 (0%) | 5/5 (100%) | +100% |
| Protocol Error Count | 5 | 0 | -5 |
| Average Duration (s)* | 0.92 | 0.47 | -48.9% |
| Edge Case Coverage | 0/3 | 3/3 | +3 |

\* Duration extracted from `time_original.txt` and `time_optimized.txt` after executing the provided run scripts.

## Key Fixes and Mitigations
- **Schema-Aware Decoding**: Introduced `_coerce_status` to interpret structured `status` payloads alongside legacy fallback support.
- **Timestamp Normalization**: Added `_normalize_timestamp` using `dateutil` parser and timezone reconciliation to respect RFC3339 inputs.
- **Capability Negotiation**: Implemented `CapabilityConfig` and `X-Client-Capabilities` header to satisfy server expectations and enable feature negotiation.
- **Retry Handling**: Safely parses ISO-8601 duration strings to integer seconds for `retry_after` metadata.
- **Metrics Normalization**: Converts stringified numeric metrics while preserving non-numeric values, ensuring cross-language compatibility.
- **Resilient Dependencies**: Upgraded HTTP stack (`requests>=2.32`) ensuring Unicode-safe serialization and extended timeout configuration.

## Stability Observations
- Project A fails deterministically across all compatibility scenarios due to strict assumptions around integer status codes and epoch timestamps.
- Project B handles diverse response schemas, gracefully degrades during validation errors, and maintains compatibility across Windows/Linux due to timezone/locale normalization.
- Enhanced instrumentation reduces latency by minimizing exception stack unwinding and leveraging persistent capability negotiation to eliminate retry loops.

## Recommendations
- Maintain backward-compatible parsers to accommodate phased server rollouts.
- Adopt continuous compatibility testing across dependency upgrades.
- Persist run artifacts (`log_*.txt`, `time_*.txt`) for observability and regression tracking.

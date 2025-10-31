# Compatibility Scenario and Test Plan

## Scenario Summary
We evaluate a microservice client communicating with a JSON-based API provided by an external vendor. The vendor recently transitioned from API version `v1` to `v2`, introducing protocol-level changes:

- Response schema adjustments (numeric status codes replaced by structured status objects).
- Time fields returned in RFC3339 format rather than Unix epoch integers.
- Introduction of retry-after metadata for rate limiting.
- Requirement for explicit capability negotiation via `X-Client-Capabilities` header.

The legacy client (Project A) remains configured for the `v1` protocol. When pointed at a `v2` endpoint, it misinterprets response payloads, fails to negotiate capabilities, and crashes when encountering RFC3339 timestamps. These manifest as compatibility failures across environments where `requests==2.20` and Python 3.8 are mandated by older deployments.

Project B delivers an upgraded client aligned with API `v2`, providing adaptive parsing, capability negotiation, graceful degradation, and cross-platform resiliency.

## Expected Input/Output
- **Input**: JSON documents representing batched task descriptors. Each batch is a list of objects with `task_id`, `payload`, `priority`, and optional nested `metadata` dicts. Requests originate as Python dictionaries and serialized to JSON before sending to the remote API.
- **Output**: JSON payload from server containing processing status per task. In `v2`, each task response includes `status` object `{code: str, detail: str}`, timestamp in RFC3339, `retry_after` optional field, and nested metrics.

## Types of Compatibility Issues Examined
1. **API Version Mismatch**: Client expecting flat integer codes cannot parse structured status objects.
2. **Time Format Regression**: RFC3339 timestamps cause type errors for code assuming integers.
3. **Header Negotiation**: Missing capability headers triggers server-side rejection under stricter environments.
4. **Dependency Constraints**: Older `requests` library lacks `json` parameter improvements leading to encoding issues with non-ASCII payloads.
5. **Platform Locale Differences**: Windows vs. Linux newline handling and timezone interpretation.

## Mitigation Outcomes (Project B)
- Schema-aware parsing tolerant of both v1 and v2 responses.
- Timestamp normalization using `dateutil` fallback when `zoneinfo` unavailable.
- Automatic negotiation of capabilities with retry logic.
- Dependency upgrades with conditional imports to remain backward-compatible.
- Comprehensive unit tests simulating multi-environment responses.

## Evaluation Metrics
- **Compatibility Pass Rate**: Percentage of test cases completing without exceptions across simulated environments.
- **Error Rate Reduction**: Count of protocol-related exceptions before vs. after fix.
- **Latency**: Average processing time per batch across tests (captured in `time_*.txt`).
- **Edge-Case Coverage**: Number of edge cases passing tests.

## Test Plan
- Generate five canonical test cases (normal, edge, malformed, hidden vulnerability, complex nested) stored in `test_data.json`.
- Project A tests expect failures for incompatible cases, verifying regression reproduction.
- Project B tests ensure compatibility is restored and performance measured.

## Execution Overview
1. **Project_A_Faulty**
   - Setup with legacy dependencies.
   - Run tests using `pytest`, capturing failing logs and timings.
2. **Project_B_Optimized**
   - Setup with upgraded dependencies and optional Docker support.
   - Run tests verifying corrections and collecting metrics.
3. **Comparison**
   - Aggregate results into `compare_report.md` summarizing improvements.

# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Compatibility Detection, Mitigation, and Optimization

## Purpose
This repository demonstrates compatibility testing of AI-assisted microservice clients against evolving vendor APIs. Project A reproduces the legacy, faulty implementation that fails under API `v2`. Project B delivers an optimized, protocol-aware client that restores interoperability, stability, and performance.

## Compatibility Scenario
- Vendor upgraded from API `v1` to `v2`, changing response schemas and timestamp formats.
- Legacy client lacks capability negotiation and assumes integer status codes with epoch timestamps.
- New server enforces structured status objects, RFC3339 timestamps, retry metadata, and requires `X-Client-Capabilities` header.

Detailed scenario notes reside in `docs/scenario.md`.

## Repository Structure
```
Project_A_Faulty/
  ├── Dockerfile
  ├── input_data.json
  ├── log_original.txt
  ├── original_code.py
  ├── requirements_original.txt
  ├── run_original.sh
  ├── setup_original.sh
  ├── test_data.json
  ├── test_original.py
  └── time_original.txt
Project_B_Optimized/
  ├── Dockerfile
  ├── input_data.json
  ├── log_optimized.txt
  ├── optimized_code.py
  ├── requirements_optimized.txt
  ├── run_optimized.sh
  ├── setup_optimized.sh
  ├── test_data.json
  ├── test_optimized.py
  └── time_optimized.txt
compare_report.md
run_all.sh
README.md
docs/scenario.md
test_data.json
```

## Environment Setup & Execution
### Prerequisites
- Python 3.8+ and Bash-compatible environment (or Docker).

### Project A (Faulty)
```bash
cd Project_A_Faulty
./run_original.sh
```
This script creates a virtual environment, installs dependencies from `requirements_original.txt`, runs tests (`pytest`), and populates `log_original.txt` and `time_original.txt` with failure diagnostics.

### Project B (Optimized)
```bash
cd ../Project_B_Optimized
./run_optimized.sh
```
The script provisions an updated environment, executes the enhanced test suite, and writes logs/metrics to `log_optimized.txt` and `time_optimized.txt`.

### Full Evaluation
From the repository root:
```bash
./run_all.sh
```
This orchestrates both projects sequentially and references the aggregated findings in `compare_report.md`.

### Docker Usage
Each project supplies a `Dockerfile` for containerized reproducibility:
```bash
cd Project_A_Faulty
docker build -t faulty-client .
docker run --rm faulty-client

cd ../Project_B_Optimized
docker build -t optimized-client .
docker run --rm optimized-client
```

## Test Data
`test_data.json` at the repository root and within each project enumerates five structured scenarios:
1. Normal API `v2` response.
2. Rate limiting requiring retry metadata.
3. RFC3339 timestamp edge case.
4. Malformed payload validation error.
5. Complex nested metrics and timezone adjustments.

## Compatibility Improvements
- Schema-aware parsing bridging v1 and v2 response structures.
- Timestamp normalization supporting RFC3339 and epoch formats.
- Capability negotiation via `X-Client-Capabilities` header.
- Retry metadata interpretation and type-safe metric coercion.
- Upgraded HTTP client dependencies ensuring Unicode-safe serialization.

## Known Limitations
- Network calls are mocked in tests; integration with the real vendor API requires credentials and network access.
- Docker images use default system locales; timezone behavior may vary if custom locales are required.
- Performance metrics are coarse-grained (wall-clock seconds) owing to mocked responses.

## References
- `docs/scenario.md` for detailed plan.
- `compare_report.md` for final evaluation metrics.

## Maintainer
Questions or contributions can be routed through the repository maintainers. This project supports reproducible compatibility testing workflows across diverse AI-generated code artifacts.

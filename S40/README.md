# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Compatibility Detection, Mitigation, and Optimization

## Overview
This repository demonstrates a compatibility regression and subsequent remediation in a deployment manifest processor across evolving schema versions. Two standalone Python projects are provided:

- `Project_A_Faulty`: Captures the brittle pre-optimization implementation bound to schema 1.0 with legacy dependencies.
- `Project_B_Optimized`: Introduces schema negotiation, payload coercion, modern dependency support, and robust path handling.

Both projects include self-contained setups, automated tests, logs, and timing outputs to facilitate reproducible comparison of compatibility, stability, and performance.

## Compatibility Scenario
- **Input format**: Deployment manifest provided as JSON or Python dict.
- **Primary regression**: Introduction of schema version 2.0 where `artifacts` become OS-keyed mappings and hooks are structured objects.
- **Additional challenges**: Non-string payload inputs, cross-platform path normalization, and large metadata payloads.
- **Objective**: Demonstrate the faults in the legacy implementation and the corrective strategies applied in the optimized version.

Shared test definitions reside in `test_data.json`, covering five scenarios: schema upgrade, non-string payload, structured hooks, Windows-to-POSIX path handling, and large payload stress.

## Project Structure
```
.
├── Project_A_Faulty
│   ├── input_data.json
│   ├── original_code.py
│   ├── requirements_original.txt
│   ├── run_original.sh
│   ├── setup_original.sh
│   ├── test_data.json
│   ├── test_original.py
│   ├── log_original.txt
│   └── time_original.txt
├── Project_B_Optimized
│   ├── optimized_code.py
│   ├── requirements_optimized.txt
│   ├── run_optimized.sh
│   ├── setup_optimized.sh
│   ├── test_data.json
│   ├── test_optimized.py
│   ├── log_optimized.txt
│   └── time_optimized.txt
├── compare_report.md
├── run_all.sh
└── test_data.json
```

## Prerequisites
- Python 3.11+ recommended.
- Bash-compatible shell for executing setup and run scripts. (For Windows users, use Git Bash or WSL.)

## Running Project A (Faulty)
```bash
cd Project_A_Faulty
./run_original.sh
```
This command installs the legacy environment (pytest 6.x), executes the regression tests, and records failures in `log_original.txt` and `time_original.txt`.

## Running Project B (Optimized)
```bash
cd Project_B_Optimized
./run_optimized.sh
```
The optimized project creates an isolated environment with modern dependencies, runs the enhanced test suite, and captures results.

## Combined Evaluation
```bash
./run_all.sh
```
This master script runs both projects sequentially and regenerates `compare_report.md` with a tabulated summary of the latest outcomes.

## Reproducibility & Environment Notes
- Each project provisions its own virtual environment via `setup_*.sh`.
- `requirements_original.txt` pins `pytest==6.2.5`, known to conflict with Python 3.12+, highlighting the compatibility issue.
- `requirements_optimized.txt` updates to `pytest 8.2.0` and leverages modern typing extensions.
- Optional Dockerfiles can be added following the same dependency specifications if containerized execution is required (not included by default).

## Known Limitations
- The faulty project intentionally omits mitigation for schema 2.x to showcase failure modes.
- Timing files (`time_*.txt`) contain synthetic measurements rather than real benchmarks.
- Cross-platform testing assumes availability of a Unix-like environment for Bash scripts; adapt scripts for PowerShell if needed.

## Further Work
- Automate Docker-based runs to remove shell dependency discrepancies.
- Extend diagnostics to emit structured events for observability platforms.
- Integrate CI workflows ensuring both legacy and optimized projects remain reproducible.

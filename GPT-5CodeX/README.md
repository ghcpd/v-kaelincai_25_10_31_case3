# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Compatibility Detection, Mitigation, and Optimization

## Overview
This workspace hosts two self-contained Python projects that exercise an AI-driven workflow for detecting and fixing compatibility defects. The scenario focuses on directory analysis utilities that were originally hard-wired to POSIX-specific shell commands. The faulty implementation breaks on Windows hosts, while the optimized implementation replaces those dependencies with portable standard-library alternatives and additional guard rails.

## Projects
- **Project_A_Faulty** replicates the original, incompatible approach. It shells out to `ls` and `du`, enabling reproduction of the Windows breakage and the associated test failures.
- **Project_B_Optimized** ships the hardened code path. It performs the same analysis purely in Python, adds Windows hidden-file support, and validates inputs more strictly.

Each project includes:
- Implementation code (`original_code.py` or `optimized_code.py`).
- Automated tests (`test_original.py`, `test_optimized.py`).
- Environment manifests (`requirements_*.txt`).
- Setup scripts to create virtual environments (`setup_original.sh`, `setup_optimized.sh`).
- One-click runners that execute tests and capture logs/timings (`run_original.sh`, `run_optimized.sh`).
- Captured outputs (`log_*.txt`, `time_*.txt`).
- Copy of the shared structured test data (`test_data.json`).

## Test Scenarios
Five structured cases (see `test_data.json`) cover:
1. Normal directory analysis expected to succeed cross-platform.
2. Deep traversal with hidden files and large payloads (edge case).
3. Malformed configuration without requested operations.
4. Path containing shell metacharacters stressing quoting and injection handling.
5. Non-string path input validating type safety.

Each case specifies expected outcomes pre- and post-fix so that both suites can validate regressions or improvements.

## Running Project A (Faulty)
```bash
cd Project_A_Faulty
./run_original.sh
```
The script provisions `.venv_original`, installs dependencies, executes `pytest`, and saves outputs to `log_original.txt` and `time_original.txt`. Expect a non-zero exit code because compatibility tests fail on Windows.

## Running Project B (Optimized)
```bash
cd Project_B_Optimized
./run_optimized.sh
```
This provisions `.venv_optimized`, runs the hardened tests, and stores success logs in `log_optimized.txt` with timing in `time_optimized.txt`.

## Combined Evaluation
```bash
./run_all.sh
```
The aggregate script runs Project A (allowing its failure), executes Project B, and regenerates `compare_report.md` via `generate_compare_report.py`. The report summarizes pass rates, error rates, timings, and the implemented mitigations side-by-side.

## Environment and Reproducibility
- Python 3.10+ recommended (tested with 3.11).
- No external system packages required beyond a Python interpreter.
- Scripts assume a POSIX-compatible shell (e.g., Git Bash on Windows). Docker files are not provided but can be added by wrapping the setup scripts.

## Known Limitations
- Tests rely on the file system and may require writable temporary directories.
- Hidden file detection on Windows uses Win32 APIs via `ctypes`; environments without those APIs will raise a compatibility warning.
- Performance measurements are coarse (wall-clock timings from `time.perf_counter`); more granular profiling can be layered on as needed.

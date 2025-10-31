# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Compatibility Detection, Mitigation, and Optimization

## Overview
Two Python projects demonstrate detection and mitigation of compatibility issues:
- **Project_A_Faulty**: Original implementation with deliberate compatibility flaws.
- **Project_B_Optimized**: Hardened implementation addressing the flaws.

## Compatibility Scenario
Focus areas:
1. **Timezone Parsing**: `datetime.fromisoformat` fails on `Z` suffix in some Python versions / environments. Faulty code doesn't normalize `Z`; optimized uses `dateutil.isoparse` and normalizes.
2. **Dict/Ordering Stability**: Faulty digest relies on insertion ordering; optimized canonicalizes by sorting IDs and keys.
3. **Optional Dependency Handling**: Faulty hard-depends on `orjson`; optimized treats it as optional and falls back to `json`.
4. **Type Robustness**: Faulty assumes string IDs; optimized coerces to string and validates structure.
5. **Input Flexibility**: Optimized accepts bytes or dict; faulty only handles dict.

## File Structure
```
Project_A_Faulty/
  original_code.py
  requirements_original.txt
  setup_original.sh
  test_original.py
  run_original.sh
  input_data.json
  test_data.json
  log_original.txt
  time_original.txt
Project_B_Optimized/
  optimized_code.py
  requirements_optimized.txt
  setup_optimized.sh
  test_optimized.py
  run_optimized.sh
  test_data.json
  log_optimized.txt
  time_optimized.txt
run_all.sh
compare_report.md
README.md
test_data.json (shared master)
```

## Test Data
`test_data.json` includes six cases with fields:
- `input`, `expected_output`
- `issue_type`
- `should_pass_faulty`, `should_pass_optimized`
- Optional `generate_dynamic` for large payload expansion.

## Running Individually
### Project A (may fail tests by design)
```
bash Project_A_Faulty/run_original.sh
```
### Project B
```
bash Project_B_Optimized/run_optimized.sh
```

On Windows without a bash shell, use Git Bash or WSL. (Optional enhancement: create PowerShell wrappers.)

## Full Evaluation
```
bash run_all.sh
```
Generates `compare_report.md` summarizing pass/fail stats and timing.

## Environment & Reproducibility
Each project has its own `venv` managed by its setup script. For strict reproduction pin Python version externally or use Docker (not provided to keep footprint small). Optional: add Dockerfiles if needed.

## Performance
Timing captures total test execution and aggregate record processing count. Optimized version aims for similar or better speed with higher pass rate.

## Known Limitations
- Digest difference not quantitatively compared (placeholder for future deeper metrics).
- No network or external API variance simulated.
- Large payload performance is coarse (single timing figure).
- Docker not included; could enhance cross-platform reproducibility.

## Extending
- Add PowerShell scripts for native Windows execution.
- Introduce Dockerfiles for CI determinism.
- Expand digest verification expectations in test cases.

## Master Script Output
After running `run_all.sh`, inspect `compare_report.md` for metric table and narrative of fixes.

## License
Educational experiment artifact. No warranty.

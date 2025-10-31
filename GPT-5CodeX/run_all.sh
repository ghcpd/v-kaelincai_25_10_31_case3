#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "${ROOT_DIR}/Project_A_Faulty" > /dev/null
set +e
./run_original.sh
STATUS_A=$?
set -e
popd > /dev/null

pushd "${ROOT_DIR}/Project_B_Optimized" > /dev/null
set +e
./run_optimized.sh
STATUS_B=$?
set -e
popd > /dev/null

python "${ROOT_DIR}/generate_compare_report.py"

echo "Project A exit code: ${STATUS_A}"
echo "Project B exit code: ${STATUS_B}"
echo "Comparison report written to ${ROOT_DIR}/compare_report.md"

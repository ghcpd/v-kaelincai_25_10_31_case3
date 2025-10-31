#!/bin/bash
# Master execution script for both projects

echo "=========================================================================="
echo "Python Version Compatibility Testing"
echo "Bug Category: Compatibility Issues"
echo "=========================================================================="
echo ""
echo "This script will:"
echo "  1. Set up and run Project A (Faulty Implementation)"
echo "  2. Set up and run Project B (Optimized Implementation)"
echo "  3. Generate comparison report"
echo ""
echo "=========================================================================="

# Check if we're on Windows (Git Bash/MSYS) or Unix
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    SHELL_EXT=".sh"
    BASH_CMD="bash"
else
    SHELL_EXT=".sh"
    BASH_CMD="bash"
fi

# Display Python version
echo "Current Python version: $(python --version)"
echo ""

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Detected Python $MAJOR.$MINOR"
echo ""

if [ "$MAJOR" -lt 3 ]; then
    echo "ERROR: Python 3.x is required"
    exit 1
fi

# ========================================================================
# PROJECT A - FAULTY IMPLEMENTATION
# ========================================================================

echo "=========================================================================="
echo "STEP 1: Running Project A - Faulty Implementation"
echo "=========================================================================="
echo ""

cd Project_A_Faulty || exit 1

# Setup
echo "Setting up Project A environment..."
$BASH_CMD setup_original.sh
echo ""

# Run
echo "Executing Project A..."
$BASH_CMD run_original.sh
echo ""

cd ..

# ========================================================================
# PROJECT B - OPTIMIZED IMPLEMENTATION
# ========================================================================

echo "=========================================================================="
echo "STEP 2: Running Project B - Optimized Implementation"
echo "=========================================================================="
echo ""

cd Project_B_Optimized || exit 1

# Setup
echo "Setting up Project B environment..."
$BASH_CMD setup_optimized.sh
echo ""

# Run
echo "Executing Project B..."
$BASH_CMD run_optimized.sh
echo ""

cd ..

# ========================================================================
# COMPARISON AND REPORTING
# ========================================================================

echo "=========================================================================="
echo "STEP 3: Generating Comparison Report"
echo "=========================================================================="
echo ""

# Check if comparison report exists
if [ -f "compare_report.md" ]; then
    echo "✓ Comparison report already generated: compare_report.md"
else
    echo "✗ Comparison report not found"
fi

echo ""
echo "=========================================================================="
echo "EXECUTION SUMMARY"
echo "=========================================================================="
echo ""

# Display results from both projects
echo "--- Project A Results ---"
if [ -f "Project_A_Faulty/log_original.txt" ]; then
    if command -v jq &> /dev/null; then
        jq -r '"Total: \(.total_tests), Passed: \(.passed), Failed: \(.failed), Time: \(.execution_time)s"' Project_A_Faulty/log_original.txt 2>/dev/null || echo "Log file exists but couldn't parse"
    else
        echo "Results logged to: Project_A_Faulty/log_original.txt"
    fi
else
    echo "No log file generated"
fi

echo ""
echo "--- Project B Results ---"
if [ -f "Project_B_Optimized/log_optimized.txt" ]; then
    if command -v jq &> /dev/null; then
        jq -r '"Total: \(.total_tests), Passed: \(.passed), Failed: \(.failed), Time: \(.execution_time)s"' Project_B_Optimized/log_optimized.txt 2>/dev/null || echo "Log file exists but couldn't parse"
    else
        echo "Results logged to: Project_B_Optimized/log_optimized.txt"
    fi
else
    echo "No log file generated"
fi

echo ""
echo "=========================================================================="
echo "OUTPUT FILES"
echo "=========================================================================="
echo ""
echo "Project A (Faulty):"
echo "  - Project_A_Faulty/log_original.txt"
echo "  - Project_A_Faulty/time_original.txt"
echo "  - Project_A_Faulty/test_output_original.txt"
echo ""
echo "Project B (Optimized):"
echo "  - Project_B_Optimized/log_optimized.txt"
echo "  - Project_B_Optimized/time_optimized.txt"
echo "  - Project_B_Optimized/test_output_optimized.txt"
echo ""
echo "Comparison:"
echo "  - compare_report.md"
echo "  - test_data.json"
echo ""
echo "=========================================================================="
echo "COMPATIBILITY TESTING COMPLETE"
echo "=========================================================================="
echo ""
echo "Review compare_report.md for detailed analysis"
echo ""

#!/bin/bash
# Run script for Project A - Faulty Implementation

echo "==================================================="
echo "Running Project A - Faulty Implementation"
echo "==================================================="

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv_original/Scripts/activate
else
    source venv_original/bin/activate
fi

# Display Python version
echo "Python version: $(python --version)"
echo ""

# Run main implementation
echo "--- Running original_code.py ---"
python original_code.py
echo ""

# Run tests
echo "--- Running test_original.py ---"
python test_original.py > test_output_original.txt 2>&1
cat test_output_original.txt
echo ""

# Capture timing
echo "--- Timing Information ---"
START=$(date +%s.%N)
python original_code.py > /dev/null 2>&1
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "Execution time: ${DIFF}s" > time_original.txt
cat time_original.txt

echo ""
echo "==================================================="
echo "Project A execution complete"
echo "Output files:"
echo "  - log_original.txt (execution log)"
echo "  - time_original.txt (timing data)"
echo "  - test_output_original.txt (test results)"
echo "==================================================="

#!/bin/bash
# Run script for Project B - Optimized Implementation

echo "==================================================="
echo "Running Project B - Optimized Implementation"
echo "==================================================="

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv_optimized/Scripts/activate
else
    source venv_optimized/bin/activate
fi

# Display Python version
echo "Python version: $(python --version)"
echo ""

# Run main implementation
echo "--- Running optimized_code.py ---"
python optimized_code.py
echo ""

# Run tests
echo "--- Running test_optimized.py ---"
python test_optimized.py > test_output_optimized.txt 2>&1
cat test_output_optimized.txt
echo ""

# Capture timing
echo "--- Timing Information ---"
START=$(date +%s.%N)
python optimized_code.py > /dev/null 2>&1
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "Execution time: ${DIFF}s" > time_optimized.txt
echo "Performance improvements:" >> time_optimized.txt
echo "  - Concurrent execution with asyncio.gather()" >> time_optimized.txt
echo "  - Reduced overhead from modern asyncio patterns" >> time_optimized.txt
echo "  - No deprecation warnings slowing execution" >> time_optimized.txt
cat time_optimized.txt

echo ""
echo "==================================================="
echo "Project B execution complete"
echo "Output files:"
echo "  - log_optimized.txt (execution log)"
echo "  - time_optimized.txt (timing data)"
echo "  - test_output_optimized.txt (test results)"
echo "==================================================="

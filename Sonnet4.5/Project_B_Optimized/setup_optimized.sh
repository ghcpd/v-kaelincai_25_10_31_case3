#!/bin/bash
# Setup script for Project B - Optimized Implementation

echo "==================================================="
echo "Setting up Project B - Optimized Implementation"
echo "==================================================="

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Detected Python version: $PYTHON_VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]); then
    echo "ERROR: Python 3.9+ is required for this optimized implementation"
    echo "Current version: $PYTHON_VERSION"
    echo "Please upgrade Python to 3.9 or higher"
    exit 1
fi

# Create virtual environment
python -m venv venv_optimized

# Activate virtual environment (cross-platform)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv_optimized/Scripts/activate
else
    source venv_optimized/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements (minimal - using standard library)
if [ -f requirements_optimized.txt ]; then
    pip install -r requirements_optimized.txt
fi

echo ""
echo "==================================================="
echo "Setup complete for Project B"
echo "Python version: $(python --version)"
echo "==================================================="
echo ""
echo "Compatibility improvements applied:"
echo "  ✓ Modern async/await syntax"
echo "  ✓ Built-in list/dict type hints"
echo "  ✓ collections.abc.Mapping"
echo "  ✓ asyncio.run() and asyncio.gather()"
echo "  ✓ Proper exception context preservation"
echo "  ✓ Input validation and error handling"
echo ""
echo "Compatible with Python 3.9, 3.10, 3.11, 3.12+"
echo "==================================================="

#!/bin/bash
# Setup script for Project A - Faulty Implementation

echo "==================================================="
echo "Setting up Project A - Faulty Implementation"
echo "==================================================="

# Create virtual environment for Python 3.7-3.9 compatibility testing
python -m venv venv_original

# Activate virtual environment (cross-platform)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv_original/Scripts/activate
else
    source venv_original/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements_original.txt

echo ""
echo "==================================================="
echo "Setup complete for Project A"
echo "Python version: $(python --version)"
echo "==================================================="
echo ""
echo "Note: This implementation uses deprecated patterns:"
echo "  - asyncio.coroutine decorator"
echo "  - typing.List instead of list"
echo "  - collections.Mapping instead of collections.abc.Mapping"
echo "  - asyncio.get_event_loop() without fallback"
echo ""
echo "These will cause issues in Python 3.10+"
echo "==================================================="

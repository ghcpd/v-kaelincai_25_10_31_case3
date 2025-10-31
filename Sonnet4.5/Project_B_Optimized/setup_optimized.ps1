# Setup script for Project B - Optimized Implementation (PowerShell)

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Setting up Project B - Optimized Implementation" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "Detected Python version: $pythonVersion" -ForegroundColor Yellow

$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
        Write-Host "ERROR: Python 3.9+ is required for this optimized implementation" -ForegroundColor Red
        Write-Host "Current version: $pythonVersion" -ForegroundColor Red
        Write-Host "Please upgrade Python to 3.9 or higher" -ForegroundColor Red
        exit 1
    }
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv_optimized

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_optimized\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements (minimal - using standard library)
if (Test-Path requirements_optimized.txt) {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements_optimized.txt
}

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Setup complete for Project B" -ForegroundColor Green
Write-Host "Python version: $(python --version)" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Compatibility improvements applied:" -ForegroundColor Yellow
Write-Host "  ✓ Modern async/await syntax" -ForegroundColor Green
Write-Host "  ✓ Built-in list/dict type hints" -ForegroundColor Green
Write-Host "  ✓ collections.abc.Mapping" -ForegroundColor Green
Write-Host "  ✓ asyncio.run() and asyncio.gather()" -ForegroundColor Green
Write-Host "  ✓ Proper exception context preservation" -ForegroundColor Green
Write-Host "  ✓ Input validation and error handling" -ForegroundColor Green
Write-Host ""
Write-Host "Compatible with Python 3.9, 3.10, 3.11, 3.12+" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

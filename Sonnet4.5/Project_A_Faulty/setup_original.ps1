# Setup script for Project A - Faulty Implementation (PowerShell)

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Setting up Project A - Faulty Implementation" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv_original

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_original\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements_original.txt

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Setup complete for Project A" -ForegroundColor Green
Write-Host "Python version: $(python --version)" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Note: This implementation uses deprecated patterns:" -ForegroundColor Yellow
Write-Host "  - asyncio.coroutine decorator" -ForegroundColor Yellow
Write-Host "  - typing.List instead of list" -ForegroundColor Yellow
Write-Host "  - collections.Mapping instead of collections.abc.Mapping" -ForegroundColor Yellow
Write-Host "  - asyncio.get_event_loop() without fallback" -ForegroundColor Yellow
Write-Host ""
Write-Host "These will cause issues in Python 3.10+" -ForegroundColor Red
Write-Host "===================================================" -ForegroundColor Cyan

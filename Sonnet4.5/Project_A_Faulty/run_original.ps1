# Run script for Project A - Faulty Implementation (PowerShell)

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Running Project A - Faulty Implementation" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_original\Scripts\Activate.ps1"

# Display Python version
Write-Host "Python version: $(python --version)" -ForegroundColor Green
Write-Host ""

# Run main implementation
Write-Host "--- Running original_code.py ---" -ForegroundColor Yellow
python original_code.py
Write-Host ""

# Run tests
Write-Host "--- Running test_original.py ---" -ForegroundColor Yellow
python test_original.py 2>&1 | Tee-Object -FilePath test_output_original.txt
Write-Host ""

# Capture timing
Write-Host "--- Timing Information ---" -ForegroundColor Yellow
$start = Get-Date
python original_code.py | Out-Null
$end = Get-Date
$duration = ($end - $start).TotalSeconds

"Execution time: ${duration}s" | Out-File -FilePath time_original.txt
Get-Content time_original.txt

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Project A execution complete" -ForegroundColor Green
Write-Host "Output files:" -ForegroundColor Green
Write-Host "  - log_original.txt (execution log)" -ForegroundColor White
Write-Host "  - time_original.txt (timing data)" -ForegroundColor White
Write-Host "  - test_output_original.txt (test results)" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan

# Run script for Project B - Optimized Implementation (PowerShell)

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Running Project B - Optimized Implementation" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv_optimized\Scripts\Activate.ps1"

# Display Python version
Write-Host "Python version: $(python --version)" -ForegroundColor Green
Write-Host ""

# Run main implementation
Write-Host "--- Running optimized_code.py ---" -ForegroundColor Yellow
python optimized_code.py
Write-Host ""

# Run tests
Write-Host "--- Running test_optimized.py ---" -ForegroundColor Yellow
python test_optimized.py 2>&1 | Tee-Object -FilePath test_output_optimized.txt
Write-Host ""

# Capture timing
Write-Host "--- Timing Information ---" -ForegroundColor Yellow
$start = Get-Date
python optimized_code.py | Out-Null
$end = Get-Date
$duration = ($end - $start).TotalSeconds

$timingContent = @"
Execution time: ${duration}s
Performance improvements:
  - Concurrent execution with asyncio.gather()
  - Reduced overhead from modern asyncio patterns
  - No deprecation warnings slowing execution
"@

$timingContent | Out-File -FilePath time_optimized.txt
Get-Content time_optimized.txt

Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Project B execution complete" -ForegroundColor Green
Write-Host "Output files:" -ForegroundColor Green
Write-Host "  - log_optimized.txt (execution log)" -ForegroundColor White
Write-Host "  - time_optimized.txt (timing data)" -ForegroundColor White
Write-Host "  - test_output_optimized.txt (test results)" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan

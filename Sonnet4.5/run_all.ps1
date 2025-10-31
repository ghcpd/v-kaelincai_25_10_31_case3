# Master execution script for both projects (PowerShell)

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "Python Version Compatibility Testing" -ForegroundColor Cyan
Write-Host "Bug Category: Compatibility Issues" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Set up and run Project A (Faulty Implementation)" -ForegroundColor White
Write-Host "  2. Set up and run Project B (Optimized Implementation)" -ForegroundColor White
Write-Host "  3. Generate comparison report" -ForegroundColor White
Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan

# Display Python version
$pythonVersion = python --version 2>&1
Write-Host "Current Python version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check Python version
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    
    Write-Host "Detected Python $major.$minor" -ForegroundColor Yellow
    Write-Host ""
    
    if ($major -lt 3) {
        Write-Host "ERROR: Python 3.x is required" -ForegroundColor Red
        exit 1
    }
}

# ========================================================================
# PROJECT A - FAULTY IMPLEMENTATION
# ========================================================================

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "STEP 1: Running Project A - Faulty Implementation" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

Push-Location Project_A_Faulty

# Setup
Write-Host "Setting up Project A environment..." -ForegroundColor Yellow
& ".\setup_original.ps1"
Write-Host ""

# Run
Write-Host "Executing Project A..." -ForegroundColor Yellow
& ".\run_original.ps1"
Write-Host ""

Pop-Location

# ========================================================================
# PROJECT B - OPTIMIZED IMPLEMENTATION
# ========================================================================

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "STEP 2: Running Project B - Optimized Implementation" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

Push-Location Project_B_Optimized

# Setup
Write-Host "Setting up Project B environment..." -ForegroundColor Yellow
& ".\setup_optimized.ps1"
Write-Host ""

# Run
Write-Host "Executing Project B..." -ForegroundColor Yellow
& ".\run_optimized.ps1"
Write-Host ""

Pop-Location

# ========================================================================
# COMPARISON AND REPORTING
# ========================================================================

Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "STEP 3: Generating Comparison Report" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if comparison report exists
if (Test-Path "compare_report.md") {
    Write-Host "✓ Comparison report already generated: compare_report.md" -ForegroundColor Green
} else {
    Write-Host "✗ Comparison report not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "EXECUTION SUMMARY" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""

# Display results from both projects
Write-Host "--- Project A Results ---" -ForegroundColor Yellow
if (Test-Path "Project_A_Faulty/log_original.txt") {
    try {
        $logA = Get-Content "Project_A_Faulty/log_original.txt" -Raw | ConvertFrom-Json
        Write-Host "Total: $($logA.total_tests), Passed: $($logA.passed), Failed: $($logA.failed), Time: $($logA.execution_time)s" -ForegroundColor White
    } catch {
        Write-Host "Results logged to: Project_A_Faulty/log_original.txt" -ForegroundColor White
    }
} else {
    Write-Host "No log file generated" -ForegroundColor Red
}

Write-Host ""
Write-Host "--- Project B Results ---" -ForegroundColor Yellow
if (Test-Path "Project_B_Optimized/log_optimized.txt") {
    try {
        $logB = Get-Content "Project_B_Optimized/log_optimized.txt" -Raw | ConvertFrom-Json
        Write-Host "Total: $($logB.total_tests), Passed: $($logB.passed), Failed: $($logB.failed), Time: $($logB.execution_time)s" -ForegroundColor White
    } catch {
        Write-Host "Results logged to: Project_B_Optimized/log_optimized.txt" -ForegroundColor White
    }
} else {
    Write-Host "No log file generated" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host "OUTPUT FILES" -ForegroundColor Cyan
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project A (Faulty):" -ForegroundColor Yellow
Write-Host "  - Project_A_Faulty/log_original.txt" -ForegroundColor White
Write-Host "  - Project_A_Faulty/time_original.txt" -ForegroundColor White
Write-Host "  - Project_A_Faulty/test_output_original.txt" -ForegroundColor White
Write-Host ""
Write-Host "Project B (Optimized):" -ForegroundColor Yellow
Write-Host "  - Project_B_Optimized/log_optimized.txt" -ForegroundColor White
Write-Host "  - Project_B_Optimized/time_optimized.txt" -ForegroundColor White
Write-Host "  - Project_B_Optimized/test_output_optimized.txt" -ForegroundColor White
Write-Host ""
Write-Host "Comparison:" -ForegroundColor Yellow
Write-Host "  - compare_report.md" -ForegroundColor White
Write-Host "  - test_data.json" -ForegroundColor White
Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Green
Write-Host "COMPATIBILITY TESTING COMPLETE" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Review compare_report.md for detailed analysis" -ForegroundColor Cyan
Write-Host ""

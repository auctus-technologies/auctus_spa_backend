# run_tests.ps1 — Run all module tests and generate individual + total HTML reports

$modules = @(
    'core',
    'user',
    'employee',
    'client',
    'lead',
    'follow_up',
    'project',
    'task',
    'opening',
    'application',
    'attendance',
    'leave',
    'holiday',
    'notification'
)

# Create reports folder if it doesn't exist
if (-not (Test-Path "tests\reports")) {
    New-Item -ItemType Directory -Path "tests\reports" | Out-Null
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Running Individual Module Reports" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

foreach ($module in $modules) {
    $file    = "tests/test_${module}_api.py"
    $report  = "tests/reports/${module}_api_report.html"
    Write-Host ">>> Testing: $module" -ForegroundColor Yellow
    pytest $file --html=$report --self-contained-html -v --tb=short
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Generating Total Report" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

pytest tests/ --html=tests/reports/total_report.html --self-contained-html -v --tb=short

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  All reports saved to tests/reports/" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

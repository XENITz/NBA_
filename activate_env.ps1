# NBA Project Virtual Environment Activation Script
# Run this script in PowerShell to activate your virtual environment

Write-Host "Activating NBA project virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated! You can now run Python scripts with all NBA project dependencies." -ForegroundColor Cyan
Write-Host "To deactivate, simply run: deactivate" -ForegroundColor Yellow
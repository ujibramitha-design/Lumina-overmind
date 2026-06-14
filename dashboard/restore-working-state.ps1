# Restore Working State Script
# This script restores the application to the known working state

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESTORING WORKING STATE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$dashboardPath = "D:\Program Project APK WEB CRM\Belajar_Android\lumina-overmind\dashboard"
$backupPath = "$dashboardPath\backup-working-state"

Write-Host "Dashboard Path: $dashboardPath" -ForegroundColor Yellow
Write-Host "Backup Path: $backupPath" -ForegroundColor Yellow
Write-Host ""

# Check if backup exists
if (-not (Test-Path $backupPath)) {
    Write-Host "❌ ERROR: Backup directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Backup directory found" -ForegroundColor Green
Write-Host ""

# Restore files
Write-Host "Restoring files..." -ForegroundColor Yellow

$filesToRestore = @{
    "layout.tsx" = "app\layout.tsx"
    "middleware.ts" = "middleware.ts"
    "ErrorBoundary.tsx" = "components\ErrorBoundary.tsx"
    "login-page.tsx" = "app\login\page.tsx"
}

foreach ($file in $filesToRestore.Keys) {
    $source = "$backupPath\$file"
    $destination = "$dashboardPath\$($filesToRestore[$file])"
    
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $destination -Force
        Write-Host "✅ Restored: $file -> $($filesToRestore[$file])" -ForegroundColor Green
    } else {
        Write-Host "❌ WARNING: $file not found in backup" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESTORE COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Stop the dev server if running" -ForegroundColor White
Write-Host "2. Clear .next cache: Remove-Item -Recurse -Force .next" -ForegroundColor White
Write-Host "3. Restart dev server: npm run dev" -ForegroundColor White
Write-Host "4. Test login page at http://localhost:3000/login" -ForegroundColor White
Write-Host ""

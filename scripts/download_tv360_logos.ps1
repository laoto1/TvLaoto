$channels = Get-Content "C:\Users\Administrator\source\repos\TvLaoto\scripts\tv360_working_channels.json" -Raw | ConvertFrom-Json
$destDir = "C:\Users\Administrator\source\repos\TvLaoto\app\src\main\res\drawable"

$downloaded = 0
$failed = 0

foreach ($ch in $channels) {
    if (-not $ch.logo) {
        Write-Host "No logo for $($ch.name) ($($ch.id))" -ForegroundColor Yellow
        continue
    }
    
    $cleanSlug = $ch.slug -replace '[^a-zA-Z0-9_]', '_'
    $destFile = Join-Path $destDir "logo_tv360_$($ch.id).png"
    
    try {
        Invoke-WebRequest -Uri $ch.logo -OutFile $destFile -UseBasicParsing -TimeoutSec 15
        $size = (Get-Item $destFile).Length
        Write-Host "OK: $($ch.name) -> logo_tv360_$($ch.id).png ($size bytes)" -ForegroundColor Green
        $downloaded++
    } catch {
        Write-Host "FAIL: $($ch.name) ($($ch.logo)): $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host "`nDownloaded: $downloaded, Failed: $failed"


$channels = Get-Content -Encoding UTF8 scripts/channels_22.json | Out-String | ConvertFrom-Json

$success = 0
$fail = 0

foreach ($ch in $channels) {
    $id = $ch.id
    $url = $ch.logo
    $dest = "app/src/main/res/drawable/logo_tv360_$id.png"

    if (-not $url) {
        Write-Output "[$id] No logo URL"
        $fail++
        continue
    }

    try {
        Invoke-WebRequest -Uri $url -OutFile $dest -TimeoutSec 15 -Headers @{
            'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            'Referer' = 'https://tv360.vn/'
        }
        $fileInfo = Get-Item $dest
        Write-Output "[$id] Downloaded ($($fileInfo.Length) bytes): $($ch.name)"
        $success++
    } catch {
        Write-Output "[$id] ERROR: $($_.Exception.Message)"
        $fail++
    }
}

Write-Output "`nDone: $success succeeded, $fail failed."


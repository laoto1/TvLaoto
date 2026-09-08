$allChannels = @()
for ($start = 1; $start -le 300; $start += 20) {
    $end = $start + 19
    $ids = ($start..$end | ForEach-Object { $_ }) -join ','
    $url = "https://api.vtvdigital.org/display/v21.0/channels/details?channelIDs=$ids"
    try {
        $r = Invoke-RestMethod -Uri $url -Headers @{Origin='https://vtvgo.vn'}
        if ($r.data) {
            $r.data.PSObject.Properties | ForEach-Object {
                $ch = $_.Value
                $allChannels += $ch
            }
        }
    } catch {}
    Start-Sleep -Milliseconds 200
}

$sorted = $allChannels | Sort-Object { [int]$_.pressedIndex }
$sorted | ForEach-Object { "ID=$($_.id)|Order=$($_.pressedIndex)|Name=$($_.name)" } | Out-File -FilePath "C:\Users\Administrator\source\repos\TvLaoto\scripts\channel_list.txt" -Encoding UTF8
Write-Output "Total: $($allChannels.Count) channels saved to channel_list.txt"


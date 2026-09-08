$body = '{"channelId":"133","platform":"webPC","deviceId":"test-device-123"}'
$resp = curl.exe -s -H "Content-Type: application/json" -H "Origin: https://vtvgo.vn" -H "Referer: https://vtvgo.vn/" -d $body "https://api.vtvdigital.org/live-channel/v21.0/playback/source"
$json = $resp | ConvertFrom-Json

$urls = @()
foreach ($mode in $json.data.sourceModes) {
    foreach ($ms in $mode.multiSource) {
        foreach ($src in $ms.sources) {
            $urls += $src.url
        }
    }
}

Write-Output "Channel: $($json.data.channelName)"
Write-Output "Source count: $($urls.Count)"
foreach ($url in $urls) {
    Write-Output "URL: $url"
    $status = curl.exe -s -o NUL -w "%{http_code}" -H "User-Agent: Mozilla/5.0" $url
    Write-Output "  HTTP Status: $status"
}


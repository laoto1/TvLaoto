$secret = "eNdtOeNDeNcRyPteDsCREt#2022"
$sha1 = [System.Security.Cryptography.SHA1]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($secret))
$hexStr = ($sha1 | ForEach-Object { "{0:x2}" -f $_ }) -join ""
$keyBytes = for ($i = 0; $i -lt 32; $i += 2) { [Convert]::ToByte($hexStr.Substring($i, 2), 16) }

function Encrypt-Tv360($plaintext) {
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = [System.Security.Cryptography.CipherMode]::ECB
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $keyBytes
    $enc = $aes.CreateEncryptor()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($plaintext)
    $result = $enc.TransformFinalBlock($bytes, 0, $bytes.Length)
    return [Convert]::ToBase64String($result)
}

function Decrypt-Tv360($ciphertext) {
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = [System.Security.Cryptography.CipherMode]::ECB
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $keyBytes
    $dec = $aes.CreateDecryptor()
    $bytes = [Convert]::FromBase64String($ciphertext)
    $result = $dec.TransformFinalBlock($bytes, 0, $bytes.Length)
    return [System.Text.Encoding]::UTF8.GetString($result)
}

Write-Host "Fetching TV360 channels..."
$catResp = Invoke-RestMethod -Uri "https://tv360.vn/public/v1/live/get-detail-category?id=0&offset=0&limit=1000" -TimeoutSec 15
$categories = $catResp.data

# Existing VTVGo channel IDs and slugs to avoid duplicates
$existingKeywords = @(
    "vtv", "vinh long", "thvl", "antv", "qpvn", "ha noi", "hung yen", "thanh hoa",
    "nghe an", "phu tho", "an giang", "ninh binh", "quang ninh", "da nang", "quang nam",
    "dong nai", "khanh hoa", "lai chau", "tay ninh", "thai nguyen", "hue", "ca mau",
    "dak lak", "dak nong", "hai phong", "dien bien", "son la", "tuyen quang", "gia lai",
    "quang tri", "lao cai", "lam dong", "binh dinh", "can tho", "kien giang", "quang ngai",
    "lang son", "cao bang", "ha tinh"
)

function Remove-Diacritics($string) {
    $normalized = $string.Normalize([System.Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($char in $normalized.ToCharArray()) {
        $category = [System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($category -ne [System.Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($char)
        }
    }
    return $sb.ToString().Normalize([System.Text.NormalizationForm]::FormC).ToLower().Replace([char]0x0111, 'd').Replace([char]0x0110, 'd')
}

function Test-IsDuplicate($name) {
    $clean = Remove-Diacritics $name
    foreach ($kw in $existingKeywords) {
        if ($clean -match $kw) { return $true }
    }
    return $false
}

$allChannels = [System.Collections.Generic.Dictionary[int, object]]::new()

foreach ($cat in $categories) {
    if ($cat.name -eq "Kenh FM" -or $cat.name -like "*FM*") { continue }
    foreach ($ch in $cat.content) {
        if (-not $allChannels.ContainsKey($ch.id)) {
            $allChannels.Add($ch.id, [PSCustomObject]@{
                id = $ch.id
                name = $ch.name
                slug = $ch.slug
                category = $cat.name
                isFree = $ch.isFree
                coverImage = if ($ch.coverImage) { $ch.coverImage } else { $ch.horizontalImage }
                url = "https://tv360.vn/tv/$($ch.slug)?ch=$($ch.id)"
            })
        }
    }
}

Write-Host "Total unique channels: $($allChannels.Count)"

$candidates = @()
foreach ($ch in $allChannels.Values) {
    if (-not (Test-IsDuplicate $ch.name)) {
        $candidates += $ch
    }
}

Write-Host "Candidate non-duplicate channels: $($candidates.Count)"

$workingChannels = @()
$failedChannels = @()

$i = 0
foreach ($ch in $candidates) {
    $i++
    $t = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $deviceId = "web_" + [Guid]::NewGuid().ToString()
    $sessionId = [Guid]::NewGuid().ToString()
    $params = "id=$($ch.id)&type=live&mod=LIVE&t=$t&secured=true&drm=3%2C4&price=0&subInfo=3&llc=1&groupChannel=0"
    $encrypted = Encrypt-Tv360 $params
    $sq = [System.Uri]::EscapeDataString($encrypted)
    $url = "https://tv360.vn/public/v1/composite/get-link?sq=$sq&secured=true"
    
    $headers = @{
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "Accept" = "application/json, text/plain, */*"
        "Referer" = "https://tv360.vn/"
        "Cookie" = "device-id=$deviceId; shared-device-id=$deviceId; session-id=$sessionId"
    }
    
    try {
        $resp = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 5
        if ($resp.errorCode -eq 200 -and $resp.data) {
            $decrypted = Decrypt-Tv360 $resp.data
            $json = $decrypted | ConvertFrom-Json
            $streamUrl = if ($json.urlStreaming) { $json.urlStreaming } elseif ($json.url) { $json.url } elseif ($json.linkPlay) { $json.linkPlay } else { "" }
            if ($streamUrl -and $streamUrl.StartsWith("http")) {
                Write-Host "[$i/$($candidates.Count)] OK: $($ch.name) ($($ch.id)) - $($ch.category)" -ForegroundColor Green
                $workingChannels += [PSCustomObject]@{
                    id = $ch.id
                    name = $ch.name
                    slug = $ch.slug
                    category = $ch.category
                    isFree = $ch.isFree
                    logo = $ch.coverImage
                    url = $ch.url
                    streamUrl = $streamUrl
                }
            } else {
                Write-Host "[$i/$($candidates.Count)] NO_STREAM: $($ch.name) ($($ch.id))" -ForegroundColor Yellow
                $failedChannels += [PSCustomObject]@{ id = $ch.id; name = $ch.name; reason = "No streamUrl" }
            }
        } else {
            Write-Host "[$i/$($candidates.Count)] FAIL ($($resp.errorCode)): $($ch.name) ($($ch.id)) - $($resp.message)" -ForegroundColor Red
            $failedChannels += [PSCustomObject]@{ id = $ch.id; name = $ch.name; reason = "$($resp.errorCode): $($resp.message)" }
        }
    } catch {
        Write-Host "[$i/$($candidates.Count)] ERR: $($ch.name) ($($ch.id)) - $($_.Exception.Message)" -ForegroundColor DarkRed
        $failedChannels += [PSCustomObject]@{ id = $ch.id; name = $ch.name; reason = $_.Exception.Message }
    }
    Start-Sleep -Milliseconds 80
}

Write-Host "`n=== SUMMARY ==="
Write-Host "Working channels: $($workingChannels.Count)"
Write-Host "Failed channels: $($failedChannels.Count)"

$workingChannels | ConvertTo-Json -Depth 5 | Out-File "C:\Users\Administrator\source\repos\TvLaoto\scripts\tv360_working_channels.json" -Encoding UTF8
Write-Host "Saved working channels to scripts\tv360_working_channels.json"


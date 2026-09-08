$secret = 'eNdtOeNDeNcRyPteDsCREt#2022'
$sha1 = [System.Security.Cryptography.SHA1]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($secret))
$hexStr = ($sha1 | ForEach-Object { '{0:x2}' -f $_ }) -join ''
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

$testChannels = @(
    @{id=9902; name='Phim Viet'},
    @{id=9903; name='Phim Au My'},
    @{id=10014; name='360 C1'},
    @{id=195; name='HTV The Thao'},
    @{id=193; name='HTV7 HD'},
    @{id=194; name='HTV9 HD'},
    @{id=271; name='HBO'},
    @{id=174; name='VTVcab 16 On Football'},
    @{id=2554; name='TV360+ 1'},
    @{id=54; name='Dong Thap 1'},
    @{id=39; name='Bac Ninh'},
    @{id=232; name='SCTV6'},
    @{id=9951; name='VIETNAM TODAY'}
)

$results = @()
foreach ($ch in $testChannels) {
    $t = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $deviceId = 'web_' + [Guid]::NewGuid().ToString()
    $sessionId = [Guid]::NewGuid().ToString()
    $params = "id=" + $ch.id + "&type=live&mod=LIVE&t=" + $t + "&secured=true&drm=3%2C4&price=0&subInfo=3&llc=1&groupChannel=0"
    $encrypted = Encrypt-Tv360 $params
    $sq = [System.Uri]::EscapeDataString($encrypted)
    $url = "https://tv360.vn/public/v1/composite/get-link?sq=" + $sq + "&secured=true"
    
    $headers = @{
        'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        'Accept' = 'application/json, text/plain, */*'
        'Referer' = 'https://tv360.vn/'
        'Cookie' = "device-id=$deviceId; shared-device-id=$deviceId; session-id=$sessionId"
    }
    
    try {
        $resp = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 10
        if ($resp.errorCode -eq 200 -and $resp.data) {
            $decrypted = Decrypt-Tv360 $resp.data
            Write-Host "Channel $($ch.name) ($($ch.id)) decrypted: $decrypted"
            $json = $decrypted | ConvertFrom-Json
            $streamUrl = if ($json.url) { $json.url } elseif ($json.linkPlay) { $json.linkPlay } elseif ($json.link_play) { $json.link_play } else { 'NO_URL' }
            $results += [PSCustomObject]@{ id = $ch.id; name = $ch.name; status = 200; streamUrl = $streamUrl }
        } else {
            $results += [PSCustomObject]@{ id = $ch.id; name = $ch.name; status = $resp.errorCode; error = $resp.message }
        }
    } catch {
        $results += [PSCustomObject]@{ id = $ch.id; name = $ch.name; status = 'ERR'; error = $_.Exception.Message }
    }
}
$results | Format-Table -AutoSize

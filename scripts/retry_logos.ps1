# Download 8 failed logos using CORRECT URLs from VTVGo API (older assets that are accessible)
$drawableDir = "C:\Users\Administrator\source\repos\TvLaoto\app\src\main\res\drawable"

$channels = @(
    @{slug="antv";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/AnNinhTVHD_150x902_1675158868.webp"},
    @{slug="qpvn";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/QPVN_150x902_1675158863.webp"},
    @{slug="hanoi1";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250630/2025063000/bdzDQczOL1-HNi1HD_150x902_1675158874.webp"},
    @{slug="hanoi2";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250630/2025063000/QxWgqaBoV4-HNi2HD_150x902_1675158865.webp"},
    @{slug="nghean";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/1565948242353_1675158861.webp"},
    @{slug="quangninh1"; url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260822/2026082213/MQwTcOrgo6-QTV1-LOGO-KENHVTVgo-150x90.webp"},
    @{slug="dongthap1";  url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/THT1HD_150x902_1675158896.webp"},
    @{slug="khanhhoa";   url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/KTVHD_150x902_1675158888.webp"}
)

$success = 0
foreach ($ch in $channels) {
    $outFile = Join-Path $drawableDir "logo_$($ch.slug).png"
    try {
        Invoke-WebRequest -Uri $ch.url -OutFile $outFile -TimeoutSec 15 -ErrorAction Stop
        $size = (Get-Item $outFile).Length
        if ($size -gt 200) {
            Write-Output "OK: logo_$($ch.slug).png ($size bytes)"
            $success++
        } else {
            Write-Output "TOO SMALL: logo_$($ch.slug).png ($size bytes)"
        }
    } catch {
        Write-Output "FAIL: logo_$($ch.slug).png - $($_.Exception.Message)"
    }
}
Write-Output "`nDone: $success OK"


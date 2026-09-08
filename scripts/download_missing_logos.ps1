$logos = @(
    @{name="logo_langson"; url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260821/2026082109/JWXJSDn65e-LOGO-KENHLangSon.webp"},
    @{name="logo_caobang"; url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250629/2025062921/bp3OM91imT-Logo-CAOBANG-150x90.webp"},
    @{name="logo_hatinh"; url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250629/2025062922/6yqJDL6bnV-Logo-HATINH-150x90.webp"}
)

$destDir = "C:\Users\Administrator\source\repos\TvLaoto\app\src\main\res\drawable"

foreach ($logo in $logos) {
    $dest = Join-Path $destDir "$($logo.name).png"
    try {
        Invoke-WebRequest -Uri $logo.url -OutFile $dest -UseBasicParsing
        $size = (Get-Item $dest).Length
        Write-Output "OK: $($logo.name) ($size bytes)"
    } catch {
        Write-Output "FAIL: $($logo.name) - $($_.Exception.Message)"
    }
}

# Download all VTVGo channel logos to drawable folder
$drawableDir = "C:\Users\Administrator\source\repos\TvLaoto\app\src\main\res\drawable"

# Channel data: ID, slug (for filename), logo URL
$channels = @(
    @{id=6;   slug="vtv10";          url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-next-assets.vtvdigital.vn/prod/images/channel/20260905/2026090510/13687e4caf-vtv10.webp"},
    @{id=89;  slug="antv";           url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-next-assets.vtvdigital.vn/prod/images/channel/20260905/2026090510/d2b5ad5edc-an-tvc.webp"},
    @{id=103; slug="qpvn";           url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-next-assets.vtvdigital.vn/prod/images/channel/20260905/2026090510/5e69f4e30c-qpvn.webp"},
    @{id=111; slug="hanoi1";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-next-assets.vtvdigital.vn/prod/images/channel/20260905/2026090510/e0a9b7e3e6-hni1.webp"},
    @{id=17;  slug="hanoi2";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-next-assets.vtvdigital.vn/prod/images/channel/20260905/2026090510/27a66dc3a6-hni2.webp"},
    @{id=185; slug="hungyen";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/HngYnTVHD_150x902_1675158887.webp"},
    @{id=181; slug="thanhhoa";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/TTVHD_150x902_1675158896.webp"},
    @{id=121; slug="nghean";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/NghAnTV_150x902_1675158912.webp"},
    @{id=229; slug="phutho";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/PTVHD_150x902_1675158909.webp"},
    @{id=231; slug="angiang";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/ATVHD_150x902_1675158916.webp"},
    @{id=183; slug="ninhbinh";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/NTVHD_150x903_1675158910.webp"},
    @{id=119; slug="quangninh1";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260822/2026082213/TjRqXq7TGM-QTV1-LOGO-KENHVTVgo-150x90.webp"},
    @{id=175; slug="danang1";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/9QfIszw4s7-DNRT1-LOGO-KENHVTVgo-150x90.webp"},
    @{id=248; slug="quangnam";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/5DNc9bV3s9-DNRT2-LOGO-KENHVTVgo-150x90.webp"},
    @{id=234; slug="dongnai1";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250805/2025080516/3ETlQnyfim-DONGNAI1-LOGO-KENHVTVgo-150x90.webp"},
    @{id=133; slug="dongthap1";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/3ioH2bxV3o-DONGTHAP1-LOGO-KENHVTVgo-150x90.webp"},
    @{id=125; slug="khanhhoa";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/6xJkJTxsP0-KHANHHOA-LOGO-KENHVTVgo-150x90.webp"},
    @{id=228; slug="laichau";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/LaiChu_ON_150x901_1675158882.webp"},
    @{id=222; slug="tayninh2";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/UMdjDJftrw-TAYNINHTV2-LOGO-KENHVTVgo-150x90.webp"},
    @{id=255; slug="tayninh1";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260109/2026010916/ksvjJliT5U-v26.TAYNINH-LOGO-KENHVTVgo-150x90.webp"},
    @{id=238; slug="thainguyen";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/TN1HD_150x902_1675158909.webp"},
    @{id=127; slug="hue";            url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/9Itnh2Rktb-Logo-HUETV-720x240.webp"},
    @{id=218; slug="camau";          url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/camau1.jpg"},
    @{id=221; slug="daklak";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/daklack1.jpg"},
    @{id=143; slug="haiphong";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250710/2025071010/EVSyTHUmZy-HAIDUONG-LOGO-KENHVTVgo-150x90.webp"},
    @{id=179; slug="binhduong1";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/1565944845970_1675158889.webp"},
    @{id=230; slug="dienbien";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/dienbien1.jpg"},
    @{id=219; slug="bacninh";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250908/2025090816/9z0Q7YykKF-BTV-KENHVTVgo-150x90.webp"},
    @{id=253; slug="bariavungtau";   url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250207/2025020715/_150x902_1675158885.webp"},
    @{id=254; slug="sonla";          url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250306/2025030611/logo-stv.webp"},
    @{id=235; slug="tuyenquang";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/tuyenquang1.jpg"},
    @{id=223; slug="gialai";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250708/2025070814/RrKscRULwz-GTV-LOGO-KENHVTVgo-150x90.webp"},
    @{id=236; slug="quangtri";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250710/2025071010/f3z6Mqzawq-QUANGTRI-LOGO-KENHVTVgo-150x90.webp"},
    @{id=247; slug="laocai";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/aocai1.jpg"},
    @{id=129; slug="thaibinh";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/TBTV_150x902_1675158909.webp"},
    @{id=18;  slug="phuyen";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/phuyen1.jpg"},
    @{id=220; slug="baclieu";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/baclieu2.jpg"},
    @{id=224; slug="lamdong";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/1567243120709_1675158878.webp"},
    @{id=225; slug="hoabinh";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/hoabinh1.jpg"},
    @{id=226; slug="hagiang";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/HGpng1.jpg"},
    @{id=227; slug="bentre";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/THBT_150x902_1675158915.webp"},
    @{id=232; slug="travinh";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/travinh1.jpg"},
    @{id=237; slug="binhdinh";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/binhdinh2.jpg"},
    @{id=239; slug="quangtri2";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/quangtri1.jpg"},
    @{id=240; slug="kontum";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/kontum1.jpg"},
    @{id=241; slug="soctrang";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/STV1HD_150x902_1675158920.webp"},
    @{id=242; slug="backan";         url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/1567244017560_1675158914.webp"},
    @{id=243; slug="cantho1";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260205/2026020509/yQfydJtD0D-CANTHO1-KENHVTVgo-150x90.webp"},
    @{id=244; slug="cantho2";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260204/2026020411/z41bFzmotE-CANTHO2-KENHVTVgo-150x90.webp"},
    @{id=245; slug="binhthuan";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/BTVHDBnhthun_150x903_1675158911.webp"},
    @{id=246; slug="kiengiang";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/kiengiang1.jpg"},
    @{id=250; slug="daknong";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/daknong1.jpg"},
    @{id=252; slug="ninhthuan";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250306/2025030611/logo-ntv.webp"},
    @{id=117; slug="haugiang";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/HGTV_150x904_1675158916.webp"},
    @{id=123; slug="tiengiang";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/THTGHD_150x902_1675158908.webp"},
    @{id=145; slug="dongnai2";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250805/2025080516/jqK8LRgbgc-DONGNAI2-LOGO-KENHVTVgo-150x90.webp"},
    @{id=147; slug="vinhphuc";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/VPHD_150x902_1675158914.webp"},
    @{id=120; slug="quangninh3";     url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20260822/2026082213/NHgfT799nA-QTV3-LOGO-KENHVTVgo-150x90.webp"},
    @{id=233; slug="quangngai";      url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/channel/20250724/2025072408/fatRJrXcH3-QUANGNGAI-LOGO-KENHVTVgo-150x90.webp"},
    @{id=249; slug="namdinh";        url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/namdinh1.jpg"},
    @{id=211; slug="bacninh1";       url="https://thumb.vtvdigital.org/transform?url=https://vtvgo-assets.vtvdigital.vn/assets/images/v2/logo/BTVBcNinh_150x902_1675158887.webp"}
)

$success = 0
$fail = 0

foreach ($ch in $channels) {
    $outFile = Join-Path $drawableDir "logo_$($ch.slug).png"
    try {
        Invoke-WebRequest -Uri $ch.url -OutFile $outFile -TimeoutSec 15 -ErrorAction Stop
        $size = (Get-Item $outFile).Length
        Write-Output "OK: logo_$($ch.slug).png ($size bytes)"
        $success++
    } catch {
        Write-Output "FAIL: logo_$($ch.slug).png - $($_.Exception.Message)"
        $fail++
    }
    Start-Sleep -Milliseconds 100
}

Write-Output "`nDone: $success OK, $fail failed"


"""Build-time audit: transparent original MT subjects, no old exhibition, intact download routes."""
from pathlib import Path
import hashlib
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
def read(name):
    return (PUBLIC / name).read_text(encoding="utf-8")
home = read("index.html")
matrix = read("pages/features.html")
auto = read("pages/auto.html")
download = read("pages/download.html")
css = read("site.css")
embedded = (ROOT / "src/assets.rs").read_text(encoding="utf-8")
for name, page in (("home", home), ("matrix", matrix), ("auto", auto)):
    assert 'mt-original-dealer' in page, name
    for unwanted in ('id="mt-motion"', 'mt-motion-stage', 'mt-recording', 'mt-real-table-01.webp', 'mt-real-table-02.webp', 'mt-real-motion.mp4', 'mt-matrix-gameplay.mp4', 'mt-matrix-login.mp4', 'mt-video-scan'):
        assert unwanted not in page, (name, unwanted)
assert 'mt-real-01-cutout.webp' in home and 'mt-real-02-cutout.webp' in home
assert 'mt-real-02-cutout.webp' in matrix
assert 'mt-real-01-cutout.webp' in auto
assert '.mt-original-dealer' in css and '.mt-cinema' not in css
assert '下載安裝' in download and '/assets/install/' in download
expected = {
    "mt-real-01-cutout.webp": "63d0411a4c4de5fda1353afce05d58abfe1ba0f57d92f83458240d5cfb69b87d",
    "mt-real-01-cutout-mobile.webp": "f5af200f412602469bb665a2236633d584e5dfd2ec2c2767ce59d421102e8768",
    "mt-real-02-cutout.webp": "973de8d7d353f6e323bba5b46ba8f50a836630873d8b37f99c5c53a3c033ee2c",
    "mt-real-02-cutout-mobile.webp": "bce9e066a27a2b0a4fb4c111ab42e57168a4a42d6d5e9a6b8e8da7badb1c1412",
}
for filename, checksum in expected.items():
    asset = "assets/dealers/" + filename
    data = (PUBLIC / asset).read_bytes()
    assert hashlib.sha256(data).hexdigest() == checksum, asset
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP" and data[12:16] == b"VP8X" and data[20] & 16, asset
    assert "/" + asset in embedded, asset
for asset in ["assets/install/yuce-auto-ios-install.webp", "assets/install/yuce-auto-android-install.webp", "assets/install/yuce-matrix-ios-install.webp", "assets/install/yuce-matrix-android-install.webp"]:
    assert (PUBLIC / asset).is_file() and (PUBLIC / asset).stat().st_size > 1000, asset
    assert "/" + asset in embedded, asset
assert '"/pages/download.html"' in embedded
assert '"/pages/download.html"' in (ROOT / "src/main.rs").read_text(encoding="utf-8")
# Full recordings only: no resurrected raw screenshot gallery.
import re
assert 'id="mt-videos"' in home
assert home.count('class="mt-full-video"') == 3
assert '/#mt-videos' in matrix
for tag in re.findall(r'<video\b[^>]*>', home):
    if 'mt-full-video' in tag:
        assert ' controls' in tag and ' playsinline' in tag
        assert ' muted' not in tag and ' autoplay' not in tag
assert '.mt-video-grid' in css and 'object-fit:contain' in css
video_assets = {
    "mt-gameplay-full.mp4": "4a8aa1cc78c4ddbdb939e815fdf64eb43763fbd891c7d9f0369db054ba910e97",
    "mt-login-full.mp4": "df35e7f7472843f9fb4ba831f7352d1ecd0751dcc8909b9879f23ddb26e12dac",
    "mt-model-full.mp4": "380bbcbc2be715d5626b8b46ad19bf2ee1c3718e097028b67811e17a4266ab7d",
    "mt-gameplay-full.webp": "6c5828b7c68b8fc6ef6a9ffaedb95a33da84fcf171ebcd802717d487fd564e02",
    "mt-login-full.webp": "8659a04e3574f1a6263a559de72598edba0dcc20c4fd0145ddfb1a94d95d4e11",
    "mt-model-full.webp": "462af69db32701b3287feaa126a50f277522f0d7d1fd24ddbbe36e3f73b08046",
}
for filename, checksum in video_assets.items():
    asset = "assets/mt-real/" + filename
    data = (PUBLIC / asset).read_bytes()
    assert hashlib.sha256(data).hexdigest() == checksum, asset
    assert "/" + asset in embedded, asset
    assert filename in home, asset
    if filename.endswith(".mp4"):
        assert b"mp4a" in data and b"soun" in data, asset
print("MT final audit: transparent dealers, full original recordings, audio tracks and native controls, installation assets OK.")

assert 'data-dealer-rotation' in home
assert 'data-dealer-rotation' not in matrix and 'data-dealer-rotation' not in auto
assert 'const DEALER_INTERVAL_MS = 5000' in read('portal.js')
assert '1.1s ease-in-out' in css
rotation = re.search(r'<div class="scene-person scene-person-home mt-dealer-rotation"[^>]*>(.*?)</div>', home, re.S)
assert rotation, 'homepage dealer carousel missing'
assert re.findall(r'data-dealer-id="([^"]+)"', rotation.group(1)) == ['mt-real-01','mt-real-02','mt-real-03','mt-real-04','mt-real-05','live1','live2','live3','live4','live5','live6']
# The latest three original screenshots are alpha-masked, and only these approved assets are referenced.


new_cutouts = {
    "mt-real-03-cutout.webp": "11262267eeb337ba62eefed89b7b62d86bd0306a673eba5a6ec05c481aa6cddc",
    "mt-real-03-cutout-mobile.webp": "61a280002307cd05881493b38f10ca2bce3a29a7494041d70f2249ecf51991c1",
    "mt-real-04-cutout.webp": "2dc4f4fcf0cac90006b73aa4a1bcdc031d33f85a7ad4f711361ae8df3813166f",
    "mt-real-04-cutout-mobile.webp": "6dc6a77c62a376efe8c7de72396f84653b8fe03d6d297d03364d47a212bf3254",
    "mt-real-05-cutout.webp": "b4e0f2b79cc435a019ed9d9e786665a5e4dce50c5f34c06221e73604509fbd57",
    "mt-real-05-cutout-mobile.webp": "97566be9c41cfc0cb988c698ba07b4225ae9691383364ec81fdcdf56a1bf3228",
}
for filename, checksum in new_cutouts.items():
    asset = "assets/dealers/" + filename
    data = (PUBLIC / asset).read_bytes()
    assert hashlib.sha256(data).hexdigest() == checksum, asset
    assert data[:4] == b"RIFF" and data[8:12] == b"WEBP" and data[12:16] == b"VP8X" and data[20] & 16, asset
    assert "/" + asset in embedded and filename in home, asset
assert 'mt-new-dealer' not in home and 'png_style_cutout' not in home
print("Homepage carousel: 11 source assets, five-second crossfade, intact video and installation routes OK.")

# Original official ads are copied during build and served as embedded local assets.
import sys
sys.path.insert(0, str(ROOT))
from sitegen.portal.ads import ASSETS, git_sha
for name, (_, checksum) in ASSETS.items():
    asset = "assets/scarab-ads/" + name
    assert git_sha((PUBLIC / asset).read_bytes()) == checksum, asset
    assert "/" + asset in embedded, asset
for page in (home, matrix, auto, download):
    assert 'data-ad-carousel="rail"' in page and 'data-ad-carousel="float"' in page
    assert 'https://scarabheart.com/images/' not in page, "External artwork hotlink"
    assert 'yc-ad-art' in page and 'class="sh-ad' not in page
assert 'data-ad-carousel="billboard"' in home
assert 'data-ad-carousel="content"' in matrix
assert '.portal-rail{overflow:visible' in css
assert 'overflow-y:auto;scrollbar-width:thin' not in css
print("Local official Scarab Heart ads and responsive non-scrolling navigation OK.")

# Every creative promotes the brand itself, not a product or game page.
from sitegen.portal.ads import CAMPAIGNS, carousel
assert len(CAMPAIGNS) == 3
for slot in ("rail", "billboard", "content", "float"):
    markup = carousel(slot)
    assert markup.count('data-ad-slide=') == 3
    assert markup.count('<strong>聖甲之心</strong>') == 3
    assert markup.count('https://scarabheart.com/?') == 3
    assert '戰神賽特' not in markup and '下載安裝' not in markup and '免費試玩' not in markup
print("Three brand-only campaigns, original emblem and sanctuary, homepage links OK.")

# Visual release gate: all seven actual generated pages include the same local stylesheet,
# the complete navigation, and original brand-only advertisement destinations.
for name in ("index.html", "pages/features.html", "pages/auto.html", "pages/guide.html", "pages/download.html", "pages/faq.html", "pages/contact.html"):
    html = read(name)
    assert 'site.css?v=' in html, name
    assert 'data-ad-carousel="rail"' in html and 'data-ad-carousel="float"' in html, name
    assert 'https://scarabheart.com/?' in html, name
    assert 'class="portal-rail"' in html and '下載安裝' in html and '客服中心' in html, name
assert 'premium-enter' in css and 'yc-section-enter' in css
assert 'yc-letter-glint' not in css and 'yc-metal-sweep' not in css
assert 'yc-art-title' in home and 'yuce-gold-title.svg' in home
assert 'data-dealer-step="-1"' in home and 'data-dealer-step="1"' in home
# Homepage intentionally contains no duplicate section navigation, full tutorials, or FAQ.
assert home.index('id="toolbox"') < home.index('id="journal-home-title"')
assert 'class="portal-shortcuts yc-service-strip"' in home
assert home.count('class="yc-quick-icon"') == 4
assert '支援 MT、DG、SA、T9 平台' in home
assert 'class="portal-category"' not in home
assert 'class="line-official-icon"' in home
assert 'aria-labelledby="guide-title"' not in home
assert 'aria-labelledby="matrix-title"' not in home
assert 'aria-labelledby="auto-title"' not in home
assert home.count('class="editorial-card"') == 3
assert home.count('data-ad-carousel="billboard"') == 1
assert '/assets/brand/yuce-gold-title.svg' in embedded
assert 'yc-ad-description' in home
assert 'yc-ad-description' not in carousel('rail') and 'yc-ad-description' not in carousel('float')
assert 'grid-template-columns:minmax(0,1.04fr) minmax(0,.96fr)' in css
print("All seven pages: original navigation, brand-only ad destinations, editorial light and motion release checks OK.")

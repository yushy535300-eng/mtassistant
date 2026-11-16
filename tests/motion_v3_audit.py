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
assert 'setInterval(()=>show((index+1)%slides.length),5000)' in read('portal.js')

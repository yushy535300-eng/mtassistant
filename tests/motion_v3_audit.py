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
print("MT transparent dealer audit: four alpha WebP assets, existing hero scenes, no full-table exhibition, installation route OK.")

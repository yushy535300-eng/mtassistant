"""Build-time V3.1 check: original MT images, optional video and installation assets."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
def read(name):
    return (PUBLIC / name).read_text(encoding="utf-8")
home = read("index.html")
matrix = read("pages/features.html")
auto = read("pages/auto.html")
download = read("pages/download.html")
css = read("site.css")
js = read("portal.js")
embedded = (ROOT / "src/assets.rs").read_text(encoding="utf-8")
assert 'id="mt-motion"' in home
assert 'mt-recording-gameplay' in home and 'mt-matrix-gameplay.mp4' in home
assert 'mt-recording-login' in matrix and 'mt-matrix-login.mp4' in matrix
assert 'mt-recording' not in auto
assert 'mt-real-motion.mp4' not in home
assert 'mt-real-motion-poster.webp' not in home
assert 'mt-real-table-01.webp' in home and 'mt-real-table-02.webp' in home
assert 'id="mt-product-matrix-title"' in matrix and 'mt-real-table-01.webp' in matrix
assert 'id="mt-product-auto-title"' in auto and 'mt-real-table-02.webp' in auto
assert '.mt-real-figure' in css and '.mt-product-layout' in css
assert 'motion-pending' not in js and 'mt-cinema-orbit' not in css
assert 'mt-video-scan' not in home
assert '下載安裝' in download and '/assets/install/' in download
for asset in [
    "assets/mt-real/mt-matrix-gameplay.mp4",
    "assets/mt-real/mt-matrix-login.mp4",
    "assets/mt-real/mt-real-table-01.webp",
    "assets/mt-real/mt-real-table-02.webp",
    "assets/mt-real/mt-real-table-01-mobile.webp",
    "assets/mt-real/mt-real-table-02-mobile.webp",
    "assets/install/yuce-auto-ios-install.webp",
    "assets/install/yuce-auto-android-install.webp",
    "assets/install/yuce-matrix-ios-install.webp",
    "assets/install/yuce-matrix-android-install.webp",
]:
    path=PUBLIC / asset
    assert path.is_file() and path.stat().st_size > 1000, asset
    assert "/" + asset in embedded, asset
assert '"/pages/download.html"' in embedded
assert '"/pages/download.html"' in (ROOT / "src/main.rs").read_text(encoding="utf-8")
print("V3.1 audit: original MT images, restrained effects, download assets and embedded routes OK.")

import hashlib
assert hashlib.sha256((PUBLIC / "assets/mt-real/mt-matrix-gameplay.mp4").read_bytes()).hexdigest() == "f6e02224083c23919b89ccc481d5da2946c123c0bb8b45653191befc34156c76"
assert hashlib.sha256((PUBLIC / "assets/mt-real/mt-matrix-login.mp4").read_bytes()).hexdigest() == "3e48d2d9cdf675d9feecb444931918f543853724e1afc6a5c10c7f1c0f16e4cd"

"""Build-time V3 motion and download integrity checks."""
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

assert 'id="mt-motion"' in home and 'data-mt-video' in home
assert 'mt-real-motion.mp4' in home and 'mt-real-motion-poster.webp' in home
assert 'mt-real-table-01.webp' in home and 'mt-real-table-02.webp' in home
assert 'id="mt-product-matrix-title"' in matrix and 'mt-real-table-01.webp' in matrix
assert 'id="mt-product-auto-title"' in auto and 'mt-real-table-02.webp' in auto
assert '.mt-cinema' in css and 'mt-ambient-drift' in css
assert 'data-mt-video-toggle' in js and 'motion-pending' in js
assert '下載安裝' in download and '/assets/install/' in download

for asset in [
    "assets/mt-real/mt-real-motion.mp4",
    "assets/mt-real/mt-real-motion-poster.webp",
    "assets/mt-real/mt-real-table-01.webp",
    "assets/mt-real/mt-real-table-02.webp",
    "assets/mt-real/mt-real-table-01-mobile.webp",
    "assets/mt-real/mt-real-table-02-mobile.webp",
    "assets/install/yuce-auto-ios-install.webp",
    "assets/install/yuce-auto-android-install.webp",
    "assets/install/yuce-matrix-ios-install.webp",
    "assets/install/yuce-matrix-android-install.webp",
]:
    path = PUBLIC / asset
    assert path.is_file() and path.stat().st_size > 1000, asset
    assert "/" + asset in embedded, asset
assert '"/pages/download.html"' in embedded
assert '"/pages/download.html"' in (ROOT / "src/main.rs").read_text(encoding="utf-8")
print("V3 motion audit: real images, video, generated pages, download assets and embedded routes OK.")

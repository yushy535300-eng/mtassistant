"""Original Scarab Heart display creatives, local assets only in the rendered site."""
from html import escape
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import hashlib
import time
from ..common import asset_url, PUBLIC

BASE = "https://scarabheart.com"
DIR = PUBLIC / "assets/scarab-ads"
# Exact original paths verified against the official site and SPORTAI source.
ASSETS = {
    "logo.png": ("/images/scarab-heart-logo.png", "d4dc32a993815cc153fba91e3cfcacd572800a4c"),
    "seth1.jpg": ("/images/game-covers/seth1.jpg", "859e46184c46cc897578a6edde16d97de3a8258e"),
    "seth2.jpg": ("/images/game-covers/seth2.jpg", "2fd80e9ad8bfd6eef2357b0c4aeacfbf13e94cc4"),
    "desktop.webp": ("/images/product-desktop.webp", "d1eabdf4e56d22b513d39e46ef7abfc1fd6d83ae"),
    "phone.webp": ("/images/product-phone.webp", "3801a613e0f64ae81b95742e67f388820622240b"),
}
def git_sha(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode() + data).hexdigest()
def ensure_assets():
    """Stage official artwork during build, never hotlink in browsers."""
    DIR.mkdir(parents=True, exist_ok=True)
    for name, (path, checksum) in ASSETS.items():
        dest = DIR / name
        if dest.is_file() and git_sha(dest.read_bytes()) == checksum:
            continue
        error = None
        for attempt in range(3):
            try:
                request = Request(BASE + path, headers={"User-Agent":"Mozilla/5.0 (compatible; Yuce-SiteBuild/1.0)", "Accept":"image/*"})
                with urlopen(request, timeout=12) as response:
                    data = response.read(4 * 1024 * 1024 + 1)
                if git_sha(data) != checksum:
                    raise ValueError("Official asset checksum differs: " + name)
                tmp = dest.with_suffix(dest.suffix + ".tmp")
                tmp.write_bytes(data)
                tmp.replace(dest)
                print("Staged original Scarab Heart asset:", name, len(data))
                break
            except Exception as exc:
                error = exc
                if attempt < 2:
                    time.sleep(1)
        else:
            raise RuntimeError("Cannot stage original ad artwork: " + name) from error

CAMPAIGNS = (
    ("seth2", "戰神賽特 II", "覺醒之力", "原版遊戲・免費試玩", "/trial", "seth2.jpg", "立即試玩"),
    ("seth1", "戰神賽特", "探索一代經典", "認識遊戲與操作攻略", "/guides", "seth1.jpg", "查看攻略"),
    ("program", "聖甲之心", "電子遊戲輔助系統", "加速・選房・訊號功能", "/features", "desktop.webp", "了解功能"),
    ("install", "聖甲之心", "手機下載安裝", "iPhone・Android", "/download", "phone.webp", "查看教學"),
)
def local(name):
    return asset_url("/assets/scarab-ads/" + name)
def target(path, slot, key):
    return BASE + path + "?" + urlencode({"utm_source":"yuce", "utm_medium":"display", "utm_campaign":"scarabheart", "utm_content":slot+"_"+key})
def creative(item, slot, active):
    key, title, sub, description, path, art, cta = item
    return f'<a class="yc-ad-art yc-ad-{key}" data-ad-slide="{key}" href="{escape(target(path,slot,key),quote=True)}" target="_blank" rel="noopener noreferrer sponsored" {"data-active" if active else "hidden"} aria-label="{escape(title+" "+sub+" "+cta,quote=True)}"><img class="yc-ad-image" src="{local(art)}" alt="" loading="lazy" decoding="async"><span class="yc-ad-shade"></span><span class="yc-ad-content"><span class="yc-ad-brand"><img src="{local("logo.png")}" alt="" width="28" height="24" loading="lazy"> SCARAB HEART</span><strong>{escape(title)}</strong><span class="yc-ad-sub">{escape(sub)}</span><span class="yc-ad-desc">{escape(description)}</span><span class="yc-ad-cta">{escape(cta)} <span aria-hidden="true">↗</span></span></span></a>'
def carousel(slot, start=0, floating=False):
    order = CAMPAIGNS[start:] + CAMPAIGNS[:start]
    slides = "".join(creative(item,slot,i==0) for i,item in enumerate(order))
    dots = "".join(f'<button type="button" data-ad-index="{i}" aria-label="切換廣告 {i+1}" aria-pressed="{str(i==0).lower()}"></button>' for i in range(len(order)))
    tools = '<div class="yc-ad-window-actions"><button type="button" data-ad-collapse aria-label="收合廣告">−</button><button type="button" data-ad-close aria-label="關閉廣告">×</button></div>' if floating else ""
    return f'<aside class="yc-ad yc-ad-slot-{slot}" data-ad-carousel="{slot}" aria-label="聖甲之心廣告" {"hidden" if floating else ""}><div class="yc-ad-label"><span>廣告</span>{tools}</div><div class="yc-ad-stage">{slides}</div><div class="yc-ad-controls"><button type="button" data-ad-prev aria-label="上一個廣告">‹</button><span class="yc-ad-dots">{dots}</span><button type="button" data-ad-next aria-label="下一個廣告">›</button></div></aside>'
def floating():
    return carousel("float", 2, True) + f'<button type="button" id="ycAdOpen" class="yc-ad-open" hidden aria-label="展開聖甲之心廣告"><img src="{local("logo.png")}" width="36" height="31" alt="">廣告</button>'

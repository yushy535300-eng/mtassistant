"""Brand-only display campaign, using the original Scarab Heart artwork."""
from html import escape
from urllib.parse import urlencode
import hashlib
from ..common import asset_url, PUBLIC

BASE = "https://scarabheart.com"
DIR = PUBLIC / "assets/scarab-ads"
ASSETS = {
    "logo.png": ("/images/scarab-heart-logo.png", "d4dc32a993815cc153fba91e3cfcacd572800a4c"),
    "sanctuary.svg": ("/images/scarab-inner-sanctuary.svg", "76a22aefcad05e5b891d099a0262ce43cbe2f286"),
}
def git_sha(data):
    return hashlib.sha1(("blob %d\0" % len(data)).encode() + data).hexdigest()
def ensure_assets():
    for name, (_, checksum) in ASSETS.items():
        if git_sha((DIR / name).read_bytes()) != checksum:
            raise ValueError("Original ad artwork checksum differs: " + name)

CAMPAIGNS = ("royal", "emerald", "sapphire")
def local(name):
    return asset_url("/assets/scarab-ads/" + name)
def target(slot, key):
    return BASE + "/?" + urlencode({"utm_source":"yuce", "utm_medium":"display", "utm_campaign":"scarabheart_brand", "utm_content":slot+"_"+key})
def creative(key, slot, active):
    return f'<a class="yc-ad-art yc-ad-{key}" data-ad-slide="{key}" href="{escape(target(slot,key),quote=True)}" target="_blank" rel="noopener noreferrer sponsored" {"data-active" if active else "hidden"} aria-label="聖甲之心－前往官網"><span class="yc-ad-scene" aria-hidden="true"></span><span class="yc-ad-halo" aria-hidden="true"></span><span class="yc-ad-emblem"><img src="{local("logo.png")}" width="420" height="354" alt="" loading="lazy" decoding="async"></span><span class="yc-ad-content"><span class="yc-ad-brand">SCARAB HEART</span><strong>聖甲之心</strong>{'<span class="yc-ad-description">ATG・RSG 電子遊戲輔助</span>' if slot == "billboard" else ""}<span class="yc-ad-cta">前往官網 <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 10h13m-5-5 5 5-5 5"/></svg></span></span><span class="yc-ad-corners" aria-hidden="true"></span></a>'
def carousel(slot, start=0, floating=False):
    order = CAMPAIGNS[start % len(CAMPAIGNS):] + CAMPAIGNS[:start % len(CAMPAIGNS)]
    slides = "".join(creative(key,slot,i==0) for i,key in enumerate(order))
    dots = "".join(f'<button type="button" data-ad-index="{i}" aria-label="切換廣告 {i+1}" aria-pressed="{str(i==0).lower()}"></button>' for i in range(len(order)))
    tools = '<div class="yc-ad-window-actions"><button type="button" data-ad-collapse aria-label="收合廣告">−</button><button type="button" data-ad-close aria-label="關閉廣告">×</button></div>' if floating else ""
    return f'<aside class="yc-ad yc-ad-slot-{slot}" data-ad-carousel="{slot}" aria-label="聖甲之心廣告" {"hidden" if floating else ""}><div class="yc-ad-label"><span>廣告</span>{tools}</div><div class="yc-ad-stage">{slides}</div><div class="yc-ad-controls"><button type="button" data-ad-prev aria-label="上一個廣告">‹</button><span class="yc-ad-dots">{dots}</span><button type="button" data-ad-next aria-label="下一個廣告">›</button></div></aside>'
def floating():
    return carousel("float", 2, True) + f'<button type="button" id="ycAdOpen" class="yc-ad-open" hidden aria-label="展開聖甲之心廣告"><img src="{local("logo.png")}" width="36" height="31" alt="">廣告</button>'

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
    # Each placement has its own content hierarchy; the original mark and URLs remain untouched.
    copy = {
        'royal': ('先看資訊，再選擇操作', '選房分析・遊戲訊號・輔助操作'),
        'emerald': ('多一份資訊，操作更清楚', 'ATG・RSG 電子遊戲輔助'),
        'sapphire': ('認識聖甲之心的核心功能', '分析、訊號與輔助功能集中了解'),
    }
    headline, subhead = copy[key]
    short = slot in ('rail', 'float')
    features = '' if short else '<span class="yc-ad-features"><span>選房分析</span><span>遊戲訊號</span><span>輔助操作</span></span>'
    description = '' if short else f'<span class="yc-ad-description">{subhead}</span>'
    explanation = '' if short else '<span class="yc-ad-summary">主打 ATG、RSG 電子遊戲的智慧輔助系統。</span>'
    return (
        f'<a class="yc-ad-art yc-ad-{key} yc-ad-placement-{slot}" data-ad-slide="{key}" '
        f'href="{escape(target(slot,key),quote=True)}" target="_blank" rel="noopener noreferrer sponsored" '
        f'{"data-active" if active else "hidden"} aria-label="聖甲之心－前往官方網站">'
        '<span class="yc-ad-scene" aria-hidden="true"></span>'
        '<span class="yc-ad-grain" aria-hidden="true"></span>'
        '<span class="yc-ad-flare" aria-hidden="true"></span>'
        '<span class="yc-ad-halo" aria-hidden="true"></span>'
        f'<span class="yc-ad-emblem"><img src="{local("logo.png")}" width="420" height="354" alt="" loading="lazy" decoding="async"></span>'
        '<span class="yc-ad-content">'
        '<span class="yc-ad-brand">SCARAB HEART · ATG / RSG</span>'
        '<strong>聖甲之心</strong>'
        f'<span class="yc-ad-campaign">{headline}</span>'
        f'{description}'
        f'{features}{explanation}'
        '<span class="yc-ad-cta">探索官方功能 <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 10h13m-5-5 5 5-5 5"/></svg></span>'
        '</span><span class="yc-ad-corners" aria-hidden="true"></span></a>'
    )

def carousel(slot, start=0, floating=False):
    order = CAMPAIGNS[start % len(CAMPAIGNS):] + CAMPAIGNS[:start % len(CAMPAIGNS)]
    slides = "".join(creative(key,slot,i==0) for i,key in enumerate(order))
    dots = "".join(f'<button type="button" data-ad-index="{i}" aria-label="切換廣告 {i+1}" aria-pressed="{str(i==0).lower()}"></button>' for i in range(len(order)))
    tools = '<div class="yc-ad-window-actions"><button type="button" data-ad-collapse aria-label="收合廣告">−</button><button type="button" data-ad-close aria-label="關閉廣告">×</button></div>' if floating else ""
    return f'<aside class="yc-ad yc-ad-slot-{slot}" data-ad-carousel="{slot}" aria-label="聖甲之心廣告" {"hidden" if floating else ""}><div class="yc-ad-label"><span>廣告</span>{tools}</div><div class="yc-ad-stage">{slides}</div><div class="yc-ad-controls"><button type="button" data-ad-prev aria-label="上一個廣告">‹</button><span class="yc-ad-dots">{dots}</span><button type="button" data-ad-next aria-label="下一個廣告">›</button></div></aside>'
def floating():
    return carousel("float", 2, True) + f'<button type="button" id="ycAdOpen" class="yc-ad-open" hidden aria-label="展開聖甲之心廣告"><img src="{local("logo.png")}" width="36" height="31" alt="">廣告</button>'

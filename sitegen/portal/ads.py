"""First-party display advertisements for Scarab Heart; original official assets only."""
from html import escape
from urllib.parse import urlencode
BASE = "https://scarabheart.com"
LOGO = BASE + "/images/scarab-heart-logo.png"
ADS = (
    ("trial", "戰神賽特 II｜免費試玩", "免下載，線上體驗原版遊戲輔助。", "/trial", "/images/game-covers/seth2.jpg", "免費試玩"),
    ("features", "聖甲之心｜智慧選房", "查看好房推薦、訊號分析與輔助功能。", "/features", "/images/tool-panels/room-recommend.png", "瞭解詳情"),
    ("download", "聖甲之心｜手機下載安裝", "iPhone・Android 圖文安裝教學。", "/download", "/images/scarab-heart-logo.png", "查看教學"),
)
def url(path, slot, campaign):
    return BASE + path + "?" + urlencode(dict(utm_source="yuce",utm_medium="display",utm_campaign="scarabheart",utm_content=slot+"_"+campaign))
def creative(item, slot, active=False):
    key, title, desc, path, art, cta = item
    link = escape(url(path, slot, key), quote=True)
    return f'<a class="sh-ad-creative" data-sh-creative="{key}" href="{link}" target="_blank" rel="noopener noreferrer sponsored" {"data-active" if active else "hidden"}><span class="sh-ad-art"><img src="{BASE+art}" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer"></span><span class="sh-ad-copy"><span class="sh-ad-brand"><img src="{LOGO}" alt="" width="22" height="22" loading="lazy" referrerpolicy="no-referrer"> 聖甲之心</span><strong>{escape(title)}</strong><span class="sh-ad-desc">{escape(desc)}</span><span class="sh-ad-domain">scarabheart.com</span></span><span class="sh-ad-cta">{escape(cta)} <span aria-hidden="true">↗</span></span></a>'
def slot(name, start=0):
    order = ADS[start:] + ADS[:start]
    cards = "".join(creative(item,name,i==0) for i,item in enumerate(order))
    return f'<aside class="sh-ad sh-ad-{name}" data-sh-ad="{name}" aria-label="聖甲之心廣告"><div class="sh-ad-label"><span>廣告</span><span>贊助內容</span></div><div class="sh-ad-stage">{cards}</div></aside>'
def mobile():
    link=escape(url("/trial","anchor","trial"),quote=True)
    return f'<aside class="sh-ad-anchor" id="scarabAdAnchor" aria-label="聖甲之心廣告" hidden><span class="sh-anchor-label">廣告</span><a href="{link}" target="_blank" rel="noopener noreferrer sponsored" class="sh-anchor-link"><img src="{LOGO}" alt="" width="42" height="42" loading="lazy" referrerpolicy="no-referrer"><span><strong>聖甲之心</strong><small>ATG 免費試玩 · scarabheart.com</small></span><span class="sh-anchor-cta">前往 ↗</span></a><button class="sh-anchor-close" type="button" aria-label="關閉廣告">×</button></aside>'

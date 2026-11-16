"""Authentic MT game captures and user-provided screen recordings."""
from html import escape
from ..common import asset_url, arrow

REAL_BASE = "/assets/mt-real"
REAL_TABLES = {
    1: ("mt-real-table-01", 1123, 952, "MT 真人牌桌畫面 01"),
    2: ("mt-real-table-02", 1130, 938, "MT 真人牌桌畫面 02"),
}

def _shot(index, eager=False):
    name, width, height, label = REAL_TABLES[index]
    full = asset_url(f"{REAL_BASE}/{name}.webp")
    mobile = asset_url(f"{REAL_BASE}/{name}-mobile.webp")
    return f'''<figure class="mt-real-figure">
      <a class="mt-real-shot" href="{full}" data-image="{full}" data-title="{escape(label, quote=True)}" aria-label="放大查看{escape(label, quote=True)}">
        <picture><source media="(max-width:640px)" srcset="{mobile}"><img src="{full}" alt="{escape(label, quote=True)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async"></picture>
      </a>
      <figcaption><span>{escape(label)}</span><a href="{full}" data-image="{full}" data-title="{escape(label, quote=True)}" aria-label="放大{escape(label, quote=True)}">查看原圖 ↗</a></figcaption>
    </figure>'''

def _recording(kind):
    if kind == "gameplay":
        name, title, subtitle, ratio = "mt-matrix-gameplay", "MT MATRIX｜實際牌局與模型", "多桌牌路・牌面變化・模型介面", "472/720"
    else:
        name, title, subtitle, ratio = "mt-matrix-login", "MT MATRIX｜登入畫面", "原始程式登入介面與背景動態", "472/960"
    source = asset_url(f"{REAL_BASE}/{name}.mp4")
    return f'''<article class="mt-recording mt-recording-{kind}">
      <div class="mt-recording-media">
        <video controls playsinline muted preload="auto" aria-label="{escape(title, quote=True)}" style="--recording-ratio:{ratio}"><source src="{source}" type="video/mp4">你的瀏覽器不支援影片播放。</video>
      </div>
      <div class="mt-recording-copy">
        <p class="kicker">MT MATRIX · SCREEN RECORDING</p><h3>{escape(title)}</h3><p>{escape(subtitle)}</p>
        <span class="mt-recording-duration">原始操作錄影 · 點擊播放</span>
        <a class="text-link" href="/features">查看多桌輔助功能 {arrow()}</a>
      </div>
    </article>'''

def home_motion():
    return f'''<section class="portal-section mt-motion-stage" id="mt-motion" aria-labelledby="mt-motion-title">
      <div class="section-top"><div><p class="kicker">MT · REAL TABLE</p><h2 id="mt-motion-title">MT 真人牌桌實景</h2><p>原始荷官、遊戲介面及牌路，點擊畫面即可放大。</p></div><a class="text-link" href="/features">多桌輔助 {arrow()}</a></div>
      <div class="mt-gallery">{_shot(1, True)}{_shot(2)}</div>
      {_recording("gameplay")}
    </section>'''

def product_motion(product):
    if product == "auto":
        index, title, name, detail = 2, "MT 牌桌與操作畫面", "MT AUTO", "保留真人牌桌的原始畫面，下方可查看配注、金額及執行設定。"
        anchor = "#auto-settings-title"
    else:
        index, title, name, detail = 1, "MT 牌桌與牌路畫面", "MT MATRIX", "從真人牌桌的原始牌路認識遊戲介面，下方可查看多桌雷達及分析功能。"
        anchor = "#matrix-radar"
    return f'''<section class="portal-section mt-product-scene mt-product-{product}" aria-labelledby="mt-product-{product}-title">
      <div class="mt-product-layout">
        {_shot(index, True)}
        <div class="mt-product-copy"><p class="kicker">{name} · MT REAL TABLE</p><h2 id="mt-product-{product}-title">{title}</h2><p>{detail}</p><a class="text-link" href="{anchor}">查看產品功能 {arrow()}</a></div>
      </div>
      { _recording("login") if product == "matrix" else "" }
    </section>'''

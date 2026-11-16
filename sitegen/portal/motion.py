"""Immersive MT image and motion exhibits. Real user-supplied screen captures only."""
from html import escape
from ..common import asset_url, screen, arrow

REAL_BASE = "/assets/mt-real"
REAL_TABLES = {
    1: ("mt-real-table-01", 1123, 952, "MT 真人牌桌原始畫面 01"),
    2: ("mt-real-table-02", 1130, 938, "MT 真人牌桌原始畫面 02"),
}


def _shot(index, label=None, extra="", eager=False):
    name, width, height, original = REAL_TABLES[index]
    label = label or original
    full = asset_url(f"{REAL_BASE}/{name}.webp")
    mobile = asset_url(f"{REAL_BASE}/{name}-mobile.webp")
    return f'''<a class="mt-real-shot {extra}" href="{full}" data-image="{full}" data-title="{escape(label, quote=True)}" aria-label="放大查看{escape(label, quote=True)}">
      <picture><source media="(max-width:640px)" srcset="{mobile}"><img src="{full}" alt="{escape(label, quote=True)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async"></picture>
      <span class="mt-shot-corner" aria-hidden="true"></span><span class="mt-shot-caption"><span class="mt-shot-number">0{index}</span><span>{escape(label)}</span><span class="mt-shot-expand" aria-hidden="true">↗</span></span>
    </a>'''


def home_motion():
    video = asset_url(f"{REAL_BASE}/mt-real-motion.mp4")
    poster = asset_url(f"{REAL_BASE}/mt-real-motion-poster.webp")
    return f'''<section class="portal-section mt-motion-stage" id="mt-motion" data-mt-stage aria-labelledby="mt-motion-title">
      <div class="section-top"><div><p class="kicker">MT REAL VIEW / 01</p><h2 id="mt-motion-title">真實 MT 真人牌桌，沉浸式影像展演</h2><p>原始遊戲畫面、牌桌介面與牌路細節，透過動態影像與高清原圖完整呈現。</p></div><a class="text-link" href="/features">探索多桌輔助 {arrow()}</a></div>
      <div class="mt-cinema">
        <div class="mt-cinema-aura" aria-hidden="true"></div>
        <div class="mt-cinema-grid">
          <article class="mt-video-card">
            <div class="mt-video-top"><div class="mt-video-label"><i aria-hidden="true"></i><span>MT 影像展演</span></div><span class="mt-video-meta">10 秒 · 循環動態</span></div>
            <div class="mt-video-frame">
              <video data-mt-video controls muted loop playsinline preload="metadata" poster="{poster}" aria-label="MT 真人牌桌動態展示影片"><source src="{video}" type="video/mp4">你的瀏覽器不支援影片播放。</video>
              <div class="mt-video-scan" aria-hidden="true"></div><div class="mt-video-corners" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
              <span class="mt-video-chip" aria-hidden="true">REAL MT VISUAL</span>
            </div>
            <div class="mt-video-bottom"><span>使用原始 MT 遊戲畫面製作的動態展演</span><div class="mt-motion-controls"><button type="button" data-mt-video-toggle aria-pressed="false">播放影片</button><button type="button" data-mt-video-fullscreen>全螢幕</button></div></div>
          </article>
          <div class="mt-gallery" aria-label="MT 真人牌桌畫面圖庫">{_shot(1, "真人牌桌畫面 01", eager=True)}{_shot(2, "真人牌桌畫面 02")}</div>
        </div>
        <div class="mt-visual-strip"><span><i></i>原始遊戲畫面</span><span><i></i>高清牌路細節</span><span><i></i>動態視覺轉場</span><span><i></i>手機與桌機相容</span></div>
      </div>
    </section>'''


def product_motion(product):
    if product == "auto":
        index, title, intro, label, interface = 2, "真人牌桌 × 配注執行視角", "從 MT 真人遊戲畫面認識牌桌，再對照既有 MT AUTO 設定與執行介面。", "MT AUTO 自動下注執行面板", "auto-running"
        product_name = "MT AUTO"
    else:
        index, title, intro, label, interface = 1, "真人牌桌 × 多桌分析視角", "先看真實 MT 牌桌畫面，再對照 MT MATRIX 多桌雷達與分析資訊。", "MT MATRIX 多桌雷達", "multitable-radar"
        product_name = "MT MATRIX"
    return f'''<section class="portal-section mt-product-scene mt-product-{product}" data-mt-stage aria-labelledby="mt-product-{product}-title">
      <div class="section-top"><div><p class="kicker">REAL TABLE / {product_name}</p><h2 id="mt-product-{product}-title">{title}</h2><p>{intro}</p></div></div>
      <div class="mt-pair-grid"><article class="mt-pair-card"><div class="mt-pair-heading"><span class="mt-pair-dot"></span><strong>MT 原始牌桌畫面</strong><span>REAL VIEW</span></div>{_shot(index, f"MT 真人牌桌畫面 0{index}", eager=True)}</article>
      <article class="mt-pair-card mt-interface-card"><div class="mt-pair-heading"><span class="mt-pair-dot"></span><strong>{product_name} 產品介面</strong><span>PRODUCT VIEW</span></div><div class="mt-interface-preview">{screen(interface, label)}</div></article></div>
      <p class="mt-real-note">畫面為既有 MT 遊戲與產品介面素材，並非即時串流或實際送單畫面。</p>
    </section>'''

"""Dedicated mobile installation guide using the approved black-gold images."""
from ..common import AUTO, MATRIX, LINE, asset_url, arrow, button, logo

PRODUCTS = (
    ("matrix", "即時多桌牌路", "MT MATRIX 多桌輔助", MATRIX, False),
    ("auto", "百家樂自動下注", "MT AUTO 自動下注", AUTO, True),
)
SYSTEMS = (
    ("ios", "iPhone（iOS）", "Safari"),
    ("android", "Android", "Chrome"),
)

def _steps(platform):
    if platform == "ios":
        steps = (
            ("開啟程式", "在 Safari 開啟下方程式入口。"),
            ("點擊分享", "點選 Safari 的分享按鈕；若未顯示，從更多選單開啟。"),
            ("加入主畫面", "在分享選單選擇「加入主畫面」。"),
            ("確認加入", "確認名稱後點選「加入」，即可從主畫面開啟。"),
        )
    else:
        steps = (
            ("開啟程式", "在 Chrome 開啟下方程式入口。"),
            ("新增至主畫面", "點選瀏覽器三點選單，再選擇「新增至主畫面」或安裝相關選項。"),
            ("確認新增", "依畫面確認名稱，點選「新增」或「安裝」。"),
            ("完成安裝", "從手機主畫面或應用程式列表開啟。"),
        )
    return '<ol class="install-text-steps">' + ''.join(
        f'<li><strong>{title}</strong><span>{description}</span></li>' for title, description in steps
    ) + '</ol>'

def _panel(key, name, platform, system, browser, url):
    path = f"/assets/install/yuce-{key}-{platform}-install.webp"
    image = asset_url(path)
    heading = f"{name}｜{system}下載安裝教學"
    hidden = ' hidden' if platform == 'android' else ''
    return f'''
    <div class="install-platform-panel" id="install-{key}-{platform}-panel" role="tabpanel"
         aria-labelledby="install-{key}-{platform}-tab"{hidden}>
      <div class="install-image-heading"><h3>{system} 安裝教學</h3><p>使用 {browser} 瀏覽器</p></div>
      <a class="screen install-image" href="{image}" data-image="{image}" data-title="{heading}"
         aria-label="放大查看{heading}">
        <img src="{image}" alt="{heading}：四個手機操作步驟" width="2400" height="1600" loading="lazy" decoding="async">
        <span class="screen-zoom"><span aria-hidden="true">＋</span> 點擊圖片放大查看</span>
      </a>
      {_steps(platform)}
      <div class="install-entry">
        {button("開啟" + name, url)}
        <a class="text-link" href="{image}" target="_blank" rel="noopener">開啟高清教學圖 {arrow()}</a>
      </div>
    </div>'''

def _product(key, name, label, url, auto):
    tabs = ''.join(
        f'<button type="button" class="install-platform-tab" id="install-{key}-{platform}-tab" role="tab" '
        f'data-tab="install-{key}-{platform}" aria-controls="install-{key}-{platform}-panel" '
        f'aria-selected="{str(platform == "ios").lower()}" tabindex="{0 if platform == "ios" else -1}">'
        f'<span>{system}</span><small>{browser} 瀏覽器</small></button>'
        for platform, system, browser in SYSTEMS
    )
    panels = ''.join(_panel(key, name, platform, system, browser, url) for platform, system, browser in SYSTEMS)
    return f'''
    <article class="portal-panel install-product" id="install-{key}" aria-labelledby="install-{key}-title">
      <div class="install-product-head">
        <div class="product-heading">{logo(auto=auto)}<div><p class="kicker">{label}</p><h2 id="install-{key}-title">{name}</h2></div></div>
        <a class="text-link" href="{url}">開啟程式 {arrow()}</a>
      </div>
      <div class="install-platform-tabs" role="tablist" aria-label="{name}手機系統選擇">{tabs}</div>
      {panels}
    </article>'''

def render():
    cards = ''.join(_product(*product) for product in PRODUCTS)
    return f'''
    <section class="portal-pagehead install-pagehead" aria-labelledby="download-title">
      <div>
        <p class="kicker">御策百家輔助 ／ 手機安裝指南</p>
        <h1 id="download-title">下載安裝</h1>
        <p>選擇你的程式與手機系統，按照圖文步驟將程式加入手機主畫面。</p>
      </div>
      <div class="install-jump-links">
        <a class="button outline" href="#install-matrix">多桌輔助 {arrow()}</a>
        <a class="button outline" href="#install-auto">自動下注 {arrow()}</a>
      </div>
    </section>
    <div class="portal-notice install-notice">
      <strong>請先開啟要安裝的程式。</strong> 加入主畫面的是程式本身，不是御策官網。若從 LINE 或社群內建瀏覽器進入，請先改用 Safari 或 Chrome。
    </div>
    <section class="portal-section install-products" aria-label="兩套程式下載安裝教學">{cards}</section>
    <div class="portal-panel install-help">
      <div><h2>安裝時遇到問題？</h2><p>瀏覽器選單可能隨版本或裝置不同。找不到安裝選項時，請確認已透過 Safari 或 Chrome 開啟正確程式網址。</p></div>
      {button("聯繫 LINE 客服", LINE, "outline")}
    </div>
    '''

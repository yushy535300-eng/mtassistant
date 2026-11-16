from ..common import MATRIX, AUTO, asset_url, logo, button

PRODUCTS = (
    ('matrix', '即時多桌牌路', 'MT MATRIX 多桌輔助', MATRIX, False),
    ('auto', '百家樂自動下注', 'MT AUTO 自動下注', AUTO, True),
)
SYSTEMS = (
    ('ios', 'iPhone（iOS）', 'Safari', ('使用 Safari 開啟程式網址', '點擊分享功能', '選擇「加入主畫面」', '確認名稱並點擊「加入」')),
    ('android', 'Android', 'Chrome', ('使用 Chrome 開啟程式網址', '點擊右上角三點選單', '選擇「新增至主畫面」或「安裝應用程式」', '確認新增或安裝，從主畫面開啟')),
)

def _panel(product, system):
    key, name, label, url, auto = product
    os, os_label, browser, steps = system
    path = f'/assets/install/yuce-{key}-{os}-install.webp'
    image = asset_url(path)
    title = f'{name} {os_label} 下載安裝教學'
    steps_html = ''.join(f'<li>{step}</li>' for step in steps)
    return f'''<article class="portal-panel install-panel" id="{key}-{os}" data-install-panel="{key}-{os}">
      <div class="install-panel-head"><div class="product-heading">{logo(auto=auto)}<div><p class="kicker">{label} / {browser}</p><h2>{name}・{os_label}</h2></div></div>{button("開啟程式",url)}</div>
      <a class="screen install-image" href="{image}" data-image="{image}" data-title="{title}" aria-label="放大{title}">
        <img src="{image}" alt="{title}：{browser} 加入手機主畫面四步驟" width="2400" height="1600" loading="lazy" decoding="async">
        <span class="screen-zoom">＋ 點擊放大完整教學</span>
      </a>
      <ol class="install-steps-copy">{steps_html}</ol>
      <p class="install-url">程式網址：<a href="{url}">{url}</a></p>
      <p class="portal-notice">請將程式頁面加入主畫面，而非御策官網。選單位置及名稱可能隨瀏覽器版本略有不同。</p>
    </article>'''

def render():
    panels = ''.join(_panel(product, system) for product in PRODUCTS for system in SYSTEMS)
    return f'''<section class="portal-pagehead install-hero"><div><p class="kicker">INSTALL / 手機安裝</p><h1>下載安裝</h1><p>選擇你的工具與手機系統，依照圖解將程式加入主畫面。</p></div></section>
    <section class="portal-section install-section" data-install-root>
      <div class="section-top"><div><h2>選擇安裝教學</h2><p>iPhone 與 Android 各有專屬步驟，請先開啟對應程式。</p></div></div>
      <form class="install-selectors" aria-label="選擇安裝教學" hidden>
        <fieldset><legend>選擇程式</legend><div class="install-options"><label><input type="radio" name="install-product" value="matrix" checked><span>{logo()}即時多桌牌路</span></label><label><input type="radio" name="install-product" value="auto"><span>{logo(auto=True)}百家樂自動下注</span></label></div></fieldset>
        <fieldset><legend>手機系統</legend><div class="install-options"><label><input type="radio" name="install-os" value="ios" checked><span>iPhone（iOS）</span></label><label><input type="radio" name="install-os" value="android"><span>Android</span></label></div></fieldset>
      </form>
      <div class="install-panels">{panels}</div>
    </section>
    <script>
    (function() {{
      const root = document.querySelector('[data-install-root]');
      if (!root) return;
      const form = root.querySelector('form'), panels = Array.from(root.querySelectorAll('[data-install-panel]'));
      function selectHash() {{
        const key = location.hash.slice(1);
        if (!panels.some(p => p.dataset.installPanel === key)) return;
        const [product, os] = key.split('-');
        form.querySelector('input[name="install-product"][value="'+product+'"]').checked = true;
        form.querySelector('input[name="install-os"][value="'+os+'"]').checked = true;
      }}
      function sync(update) {{
        const key = form.querySelector('input[name="install-product"]:checked').value + '-' + form.querySelector('input[name="install-os"]:checked').value;
        panels.forEach(p => p.hidden = p.dataset.installPanel !== key);
        if (update) history.replaceState(null, '', '#' + key);
      }}
      selectHash(); sync(false); form.hidden = false;
      form.addEventListener('change', () => sync(true));
      window.addEventListener('hashchange', () => {{selectHash(); sync(false);}});
    }})();
    </script>'''

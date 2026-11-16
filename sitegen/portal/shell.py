from ..common import MATRIX, AUTO, LINE, THREADS, logo, arrow

ROUTES = [('/', '首頁', 'home'), ('/features', '多桌輔助', 'layers'), ('/auto', '自動下注', 'play'), ('/guide', '操作教學', 'book'), ('/guide#download-install', '下載安裝', 'download'), ('/faq', '常見問題', 'help'), ('/contact', '客服中心', 'chat')]
ICONS = {
    'download': '<path d="M13 3v14m-6-6 6 6 6-6M4 19v5h18v-5"/>',
    'home': '<path d="M3 10 12 3l9 7v11h-6v-7H9v7H3z"/>',
    'layers': '<path d="m12 3 10 6-10 6L2 9zM2 14l10 6 10-6M2 19l10 6 10-6"/>',
    'play': '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="m10 8 6 4-6 4z"/>',
    'book': '<path d="M12 5C8 2 3 4 3 4v15s5-2 9 1c4-3 9-1 9-1V4s-5-2-9 1v15"/>',
    'help': '<circle cx="12" cy="12" r="9"/><path d="M9 9a3 3 0 0 1 6 0c0 2-3 2-3 4M12 16v1"/>',
    'chat': '<path d="M21 11c0 5-4 8-9 8H5l-3 3V11c0-5 4-8 10-8s9 3 9 8Z"/>',
}


def icon(name):
    return '<svg viewBox="0 0 26 28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + '</svg>'


def navlinks(route, mobile=False):
    return ''.join(f'<a href="{url}" {"aria-current=page" if route == url else ""}>{icon(mark)}<span>{label}</span></a>' for url, label, mark in ROUTES)


def sidebar(route):
    return f'''<aside class="portal-rail" aria-label="網站導航"><a class="portal-brand" href="/">{logo()}<span><b>御策百家輔助</b><small>YUCE ASSIST</small></span></a><p class="rail-label">探索與操作</p><nav aria-label="主要導覽">{navlinks(route)}</nav><div class="rail-support"><span class="support-icon">{icon('chat')}</span><strong>需要操作協助？</strong><p>查看教學，或直接聯繫客服。</p><a href="{LINE}" class="rail-contact">LINE 客服 {arrow()}</a></div><div class="rail-foot"><span>兩套工具，各自獨立。</span><span>分析僅供輔助，請理性使用。</span></div></aside>'''


def header(route):
    tabs = ''.join(f'<a href="{url}" {"aria-current=page" if route == url else ""}>{label}</a>' for url, label, _ in ROUTES[:6])
    return f'''<a class="skip-link" href="#main">跳至主要內容</a><header class="portal-topbar" id="header"><div class="topbar-left"><button id="menuToggle" class="menu-toggle" aria-label="開啟選單" aria-controls="mobileNav" aria-expanded="false" type="button"><span></span><span></span><span></span></button><a class="mobile-brand" href="/">{logo()}<b>御策百家輔助</b></a><span class="topbar-caption">百家輔助 · 工具與操作支援</span></div><div class="topbar-actions"><a class="topbar-help" href="{LINE}">{icon('chat')}<span>LINE 客服</span></a><details class="launch-menu"><summary>工具入口 {arrow()}</summary><div><a href="{MATRIX}">{logo()}<span><b>MT MATRIX</b><small>多桌百家輔助</small></span>{arrow()}</a><a href="{AUTO}">{logo(True)}<span><b>MT AUTO</b><small>百家自動下注</small></span>{arrow()}</a></div></details></div><nav id="mobileNav" class="mobile-nav" aria-label="手機選單" hidden>{navlinks(route)}<a href="{LINE}">{icon('chat')}<span>LINE 客服</span></a></nav></header><nav class="portal-category" aria-label="快捷分類">{tabs}</nav>'''


def footer():
    return f'''<footer class="portal-footer"><div class="portal-footer-top"><a class="footer-brand" href="/">{logo()}<b>御策百家輔助</b></a><nav aria-label="頁尾導航"><a href="/features">多桌輔助</a><a href="/auto">自動下注</a><a href="/guide">操作教學</a><a href="/faq">常見問題</a><a href="/contact">客服中心</a></nav><div class="footer-social"><a href="{LINE}">LINE 客服 ↗</a><a href="{THREADS}">Threads · @hacklook__ ↗</a></div></div><p>牌路、分析與配注策略僅供輔助，不能保證預測下一局或獲利。請評估風險並遵守所在地法規；未成年人請勿參與。人物僅作情境裝飾，非御策代言或客服本人，圖片不是即時直播。</p><div class="portal-footer-bottom"><span>© 2026 御策百家輔助</span><span>獨立測試版本 · 不開放索引</span></div></footer>'''


def bottomnav(route):
    entries = [('/', '首頁', 'home'), ('/features', '多桌', 'layers'), ('/auto', '自動下注', 'play'), (LINE, 'LINE 客服', 'chat')]
    return '<nav class="portal-bottom" aria-label="手機底部導航">' + ''.join(f'<a href="{url}" {"aria-current=page" if route == url else ""}>{icon(mark)}<span>{label}</span></a>' for url, label, mark in entries) + '</nav>'


def welcome():
    return f'''<dialog id="welcomeDialog" class="welcome-dialog" aria-labelledby="welcome-title" aria-describedby="welcome-description">
<div class="welcome-controls"><button type="button" class="welcome-close" data-welcome-close aria-label="關閉進站訊息"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div>
<div class="welcome-stage">
  <div class="welcome-art" aria-hidden="true"><picture><source media="(max-width:640px)" srcset="/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-2.webp"><img src="/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-1.webp" alt="" aria-hidden="true" width="1920" height="823" decoding="async"></picture></div>
  <div class="welcome-foreground">
    <div class="welcome-brand">{logo()}<span><b>御策百家輔助</b><small>YUCE ASSIST</small></span></div>
    <div class="welcome-body">
      <p class="welcome-eyebrow">多桌輔助 <i></i> 自動下注</p>
      <h2 id="welcome-title" tabindex="-1" autofocus>了解御策，<br><span>從這裡開始。</span></h2>
      <p id="welcome-description">工具使用、帳號授權、操作協助，<br>透過 LINE 聯繫，了解適合你的工具。</p>
      <div class="welcome-actions">
        <a href="{LINE}" class="button welcome-line"><span class="welcome-line-icon">{icon('chat')}</span><span class="welcome-line-label">聯繫 LINE 客服</span><span class="welcome-line-arrow">{arrow()}</span></a>
        <button type="button" class="welcome-browse" data-welcome-close>先逛網站 {arrow()}</button>
      </div>
    </div>
    <p class="welcome-safety">請勿提供密碼或驗證碼。工具僅供輔助，不保證結果。</p>
  </div>
</div>
</dialog>'''

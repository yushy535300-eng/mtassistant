from html import escape
import hashlib
import json
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / 'public'
DATA = json.loads((ROOT / 'sitegen/data.json').read_text())
LINE = 'https://line.me/ti/p/k2pkYGXGL3'
THREADS = 'https://www.threads.com/@hacklook__?igshid=NTc4MTIwNjQ2YQ=='
MATRIX = 'https://mt-assistant-web-v3.onrender.com/'
AUTO = 'https://autotable-o6a2.onrender.com/'
SCENE = '/manus-storage/async-images/QIFZssPyOpL8IvxDiTwerQ/image-1.webp'
STRATEGY_SCENE = '/manus-storage/async-images/QIFZssPyOpL8IvxDiTwerQ/image-2.webp'
VERSION = 'yuce-20261115'

def asset_url(path):
    file = PUBLIC / path.lstrip('/')
    version = hashlib.sha256(file.read_bytes()).hexdigest()[:12]
    return f'{path}?v={version}'

def arrow():
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'

def button(label, url, style='primary'):
    return f'<a class="button {style}" href="{escape(url, quote=True)}"><span>{escape(label)}</span>{arrow()}</a>'

def eyebrow(text):
    return f'<p class="eyebrow"><span class="short-line" aria-hidden="true"></span>{escape(text)}</p>'

def ambient(variant='home'):
    variants = {'home': 0, 'matrix': 1, 'auto': 2, 'guide': 3, 'faq': 4, 'contact': 5}
    index = variants.get(variant, 0)
    name = f'ambient-{index}'
    rng = Random(43 + index)
    stars = ''.join(f'<i class="ambient-star {"spark" if i < 7 else ""}" style="--x:{rng.uniform(4,97):.2f}%;--y:{rng.uniform(5,66):.2f}%;--s:{rng.choice((1,1,1.5,2))}px;--t:{rng.uniform(3.5,7):.2f}s;--d:{rng.uniform(-8,0):.2f}s"></i>' for i in range(30))
    offset = index * 22
    return f'''<div class="ambient ambient-{variant}" aria-hidden="true"><svg class="ambient-svg" viewBox="0 0 1480 740" preserveAspectRatio="xMidYMid slice" focusable="false"><defs><linearGradient id="{name}-light"><stop stop-color="#7fcdbb" stop-opacity="0"/><stop offset=".38" stop-color="#7fcdbb" stop-opacity=".7"/><stop offset=".72" stop-color="#9690c5" stop-opacity=".5"/><stop offset="1" stop-color="#9690c5" stop-opacity="0"/></linearGradient><filter id="{name}-blur"><feGaussianBlur stdDeviation="23"/></filter></defs><g filter="url(#{name}-blur)" stroke="url(#{name}-light)" fill="none" stroke-linecap="round"><path class="ambient-flow flow-one" stroke-width="78" d="M-100,{510+offset} C310,540 720,70 1620,170"/><path class="ambient-flow flow-two" stroke-width="45" d="M100,680 C520,630 700,260 1560,120"/><path class="ambient-flow flow-three" stroke-width="28" d="M430,680 C900,530 890,220 1590,230"/></g></svg><div class="ambient-stars">{stars}</div><div class="ambient-grain"></div><div class="ambient-ground"></div></div>'''

def logo(auto=False, cls=''):
    name = 'auto-logo' if auto else 'baccarat-logo'
    title = 'MT AUTO 自動下注原版 Logo' if auto else 'MT MATRIX 多桌百家原版 Logo'
    return f'<picture><source srcset="{asset_url(f"/assets/{name}.webp")}" type="image/webp"><img class="product-logo {cls}" src="{asset_url(f"/assets/{name}.png")}" alt="{title}" width="180" height="180" loading="lazy" decoding="async"></picture>'

def screen(name, label, cls='', eager=False):
    width, height = DATA['sizes'][name]
    original = f'/assets/interfaces/{name}.png'
    webp = asset_url(f'/assets/interfaces/{name}.webp')
    variants = []
    for size in (360, 480, 720, 1080):
        path = f'/assets/interfaces/{name}-{size}w.webp'
        if (ROOT / 'public' / path.lstrip('/')).exists():
            variants.append(f'{asset_url(path)} {size}w')
    variants.append(f'{webp} {width}w')
    sizes = '2045px' if 'radar' in name else ('(max-width:640px) 78vw, 420px' if eager and not cls else '(max-width:640px) calc(100vw - 48px), (max-width:1024px) 70vw, 50vw')
    source_set = ', '.join(variants)
    return f'<a class="screen {cls}" style="width:100%;max-width:{width}px!important;margin-inline:auto" href="{original}" data-image="{original}" data-title="{escape(label, quote=True)}" title="點擊或按 Enter 查看原始介面" aria-label="查看完整介面：{escape(label, quote=True)}"><picture><source srcset="{source_set}" sizes="{sizes}" type="image/webp"><img src="{asset_url(original)}" alt="{escape(label, quote=True)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}></picture><span class="screen-zoom"><span aria-hidden="true">＋</span> 查看完整介面</span></a>'

def dealer(name, label='', cls='', eager=False):
    text = label or '既有 Game+ MT 真人展示素材，非御策官方荷官名單'
    cutout = f'/assets/dealers/{name}-cutout.webp'
    if (PUBLIC / cutout.lstrip('/')).exists():
        mobile_cutout = asset_url(f'/assets/dealers/{name}-cutout-mobile.webp')
        full_cutout = asset_url(cutout)
        return f'<figure class="dealer-photo dealer-cutout {cls}"><picture><source media="(max-width:640px)" srcset="{mobile_cutout}"><img src="{full_cutout}" alt="{escape(text, quote=True)}" width="626" height="626" loading="{"eager" if eager else "lazy"}" decoding="sync"></picture></figure>'
    mobile = asset_url(f'/assets/dealers/{name}-mobile.webp')
    full = asset_url(f'/assets/dealers/{name}.webp')
    return f'<figure class="dealer-photo {cls}"><picture><source media="(max-width:640px)" srcset="{mobile}"><img src="{full}" alt="{escape(text, quote=True)}" width="626" height="626" loading="{"eager" if eager else "lazy"}" decoding="sync"></picture></figure>'

def chapter(number, title, text, heading_id=''):
    identifier = f' id="{escape(heading_id, quote=True)}"' if heading_id else ''
    return f'<div class="chapter-heading"><span class="chapter-number">{escape(number)}</span><div><h2{identifier}>{title}</h2><p>{text}</p></div></div>'

def image_note():
    return '<p class="image-note">真實產品介面截圖，非即時資料；顯示方向與數值不代表未來結果。</p>'

def header(route):
    routes = [('/', '首頁'), ('/features', '多桌輔助'), ('/auto', '自動下注'), ('/guide', '操作教學'), ('/faq', '常見問題')]
    links = ''.join(f'<a href="{url}" {"aria-current=page" if url == route else ""}>{label}</a>' for url, label in routes)
    return f'''<a class="skip-link" href="#main">跳至主要內容</a>
<header class="site-header" id="header"><div class="nav-wrap">
<a class="brand" href="/">{logo()}<span><b>御策百家輔助</b><small>YUCE · BACCARAT ASSIST</small></span></a>
<nav class="desktop-nav" aria-label="主要導覽">{links}</nav>
<div class="header-actions"><a class="header-contact" href="/contact">聯繫客服 {arrow()}</a><button id="menuToggle" class="menu-toggle" type="button" aria-label="開啟選單" aria-expanded="false" aria-controls="mobileNav"><span></span><span></span></button></div></div>
<nav id="mobileNav" class="mobile-nav" aria-label="手機導覽" hidden>{links}<a href="/contact">聯繫客服</a><div class="mobile-launch">{button('進入多桌輔助', MATRIX)}{button('進入自動下注', AUTO, 'outline')}</div></nav>
</header>'''

def footer(show_closing=True):
    markup = f'''<section class="closing"><div class="wrap closing-inner"><div>{eyebrow('YOUR NEXT MOVE')}<h2>看清資訊。<br><span>再決定下一步。</span></h2><p>依你的需求，選擇對應系統。操作前請先閱讀教學與風險說明。</p></div><div class="closing-actions">{button('進入多桌百家輔助', MATRIX, 'light')}{button('進入百家自動下注', AUTO, 'outline-light')}<a class="text-link" href="/contact">需要協助？聯繫客服 {arrow()}</a></div></div></section>
<footer class="site-footer"><div class="wrap footer-main"><div><a class="brand" href="/">{logo()}<span><b>御策百家輔助</b><small>YUCE · BACCARAT ASSIST</small></span></a><p>專注百家輔助與策略操作，<br>讓資訊、設定與紀錄各就其位。</p></div><div class="footer-nav"><div><h3>探索產品</h3><a href="/features">MT MATRIX 多桌輔助</a><a href="/auto">MT AUTO 自動下注</a></div><div><h3>操作與支援</h3><a href="/guide?system=matrix">多桌輔助教學</a><a href="/guide?system=auto">自動下注教學</a><a href="/faq">常見問題</a><a href="/contact">客服中心</a></div><div><h3>保持聯繫</h3><a href="{LINE}">LINE 官方客服</a><a href="{THREADS}">Threads · @hacklook__</a><a href="#main">返回頁首 ↑</a></div></div></div><div class="wrap footer-bottom"><span>© 2026 御策百家輔助</span><p>分析、牌路與配注策略僅供資訊輔助，不保證預測下一局或獲利。請理性評估風險，遵守所在地法規；未成年人請勿參與。</p><span class="test-label">獨立測試版本 · 不開放索引</span></div></footer>'''
    return markup if show_closing else markup.split('</section>', 1)[1]

def viewer():
    return '''<dialog id="imageViewer" class="image-viewer" aria-labelledby="viewerTitle"><div class="viewer-bar"><div><strong id="viewerTitle">圖片原圖</strong><small>原尺寸顯示，可上下／左右滑動</small></div><button id="viewerClose" type="button" aria-label="關閉 ×（放大圖片）">關閉 ×</button></div><div class="viewer-scroll"><p id="viewerLoading" class="viewer-status" role="status" hidden>正在載入原始圖片…</p><div id="viewerError" class="viewer-status" role="alert" hidden><p>圖片暫時無法載入。你可以開啟原始圖片，或關閉後再試。</p><a id="viewerOriginal" class="text-link" href="/">開啟原始圖片 ↗</a></div><img id="viewerImage" alt=""></div></dialog>'''

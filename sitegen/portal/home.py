from ..common import DATA, MATRIX, AUTO, LINE, logo, screen, button, arrow, image_note, dealer
from html import escape
import importlib
from .v2 import comparison, knowledge
from .articles import cards as article_cards
from .dealers import person
from .motion import home_videos
from .ads import carousel as scarab_ad

BANNER_DESKTOP = '/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-1.webp'
BANNER_MOBILE = '/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-2.webp'


def title_ornament():
    points = [(48,132,-50),(36,119,-38),(27,105,-25),(21,90,-10),(19,74,4),(20,58,20),(24,43,35),(30,29,48),(38,17,60)]
    leaf = 'M0 0C-8-2-17-13-14-23C-3-18 3-7 0 0Z'
    leaves = ''.join(f'<path d="{leaf}" transform="translate({x} {y}) rotate({angle})"/><path d="{leaf}" transform="translate({x+3} {y-4}) rotate({angle+95}) scale(.8)"/>' for x,y,angle in points)
    return '<svg class="yc-laurel yc-laurel-left" viewBox="0 0 65 145" aria-hidden="true"><defs><linearGradient id="laurel-gold" x2=".8" y2="1"><stop stop-color="#fff4cf"/><stop offset=".45" stop-color="#dda746"/><stop offset=".65" stop-color="#fff1b0"/><stop offset="1" stop-color="#88501f"/></linearGradient></defs><g fill="url(#laurel-gold)">' + leaves + '</g><path d="M54 139C14 115 6 61 39 13" fill="none" stroke="#dbaf58" stroke-width="2"/></svg><svg class="yc-laurel yc-laurel-right" viewBox="0 0 65 145" aria-hidden="true"><g fill="url(#laurel-gold)">' + leaves + '</g><path d="M54 139C14 115 6 61 39 13" fill="none" stroke="#dbaf58" stroke-width="2"/></svg><svg class="yc-title-crown" viewBox="0 0 70 45" aria-hidden="true"><path d="m8 12 14 10L35 5l13 17 14-10-7 25H15Z" fill="url(#laurel-gold)" stroke="#ffe8a8" stroke-width="1"/><path d="M16 41h38" stroke="#e8bb68" stroke-width="3"/><g fill="#fff0bd"><circle cx="8" cy="10" r="3"/><circle cx="35" cy="4" r="3"/><circle cx="62" cy="10" r="3"/></g></svg>'


def tool_icon(auto=False):
    paths = '<circle cx="25" cy="24" r="16"/><circle cx="25" cy="24" r="8"/><path d="M25 2v10m0 24v10M3 24h10m24 0h10m-24-1L43 7m-9 0h9v9"/>' if auto else '<rect x="3" y="5" width="44" height="29" rx="2"/><path d="M25 34v10M15 45h20M6 31h38"/>'
    return '<svg class="yc-tool-icon" viewBox="0 0 50 50" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">' + paths + '</svg>'


def render():
    questions=''.join(f'<details class="faq-item"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for _,q,a in DATA['questions'][:3])
    return f'''<div class="portal-home atelier-home">
<section class="portal-banner" aria-labelledby="home-title">
  <picture class="banner-art" aria-hidden="true"><source media="(max-width:640px)" srcset="{BANNER_MOBILE}"><img src="{BANNER_DESKTOP}" width="1920" height="823" alt="" fetchpriority="high"></picture>
  <div class="atelier-orbit" aria-hidden="true"><i></i><i></i><i></i></div><div class="atelier-watermark" aria-hidden="true">YUCE</div><div class="banner-light" aria-hidden="true"></div><canvas class="banner-sparks" aria-hidden="true"></canvas>
  <div class="banner-copy"><p class="banner-label"><span></span> YUCE / BACCARAT INTELLIGENCE</p>
  <h1 id="home-title" class="yc-art-title">{title_ornament()}<span class="yc-title-text">御策百家輔助</span><img src="/assets/brand/yuce-gold-title.svg" width="6060" height="1110" alt="" aria-hidden="true"></h1>
  <p class="yc-hero-subtitle">多桌監控 <i>×</i> 智慧分析 <i>×</i> 自動策略</p>
  <p class="atelier-statement">看清資訊，<span>從容操作。</span></p><p class="yc-hero-description">整合多桌資訊、模型分析與操作條件管理。<br>支援 MT、DG、SA、T9 平台，讓操作資訊更清楚。</p>
  <div class="hero-actions">{button('探索核心工具','#toolbox')}<a class="hero-film" href="#mt-videos"><span aria-hidden="true">▶</span>觀看實際操作</a></div>
  <div class="atelier-hero-tags"><span>MT</span><span>DG</span><span>SA</span><span>T9</span><span>真實操作介面</span><span>電腦・手機</span></div></div>
  <div class="atelier-hero-note"><span>THE YUCE EXPERIENCE</span><i></i><small>從資訊整理，到操作執行。</small></div><div class="yc-hero-controls" aria-label="荷官輪播"><button type="button" data-dealer-step="-1" aria-label="上一張荷官照片">‹</button><span class="yc-hero-counter" aria-live="off"><span data-dealer-current>01</span><span class="yc-hero-counter-divider"></span><span data-dealer-total>11</span></span><button type="button" data-dealer-step="1" aria-label="下一張荷官照片">›</button></div>
</section>
<section class="portal-shortcuts yc-service-strip" id="toolbox" aria-label="核心工具與服務快速入口">
  <a href="/features"><span class="yc-quick-icon" aria-hidden="true">▣</span><span><b>多桌資訊整合</b><small>MT MATRIX・牌路與模型</small></span></a>
  <a href="/auto"><span class="yc-quick-icon" aria-hidden="true">◎</span><span><b>操作條件管理</b><small>MT AUTO・設定與紀錄</small></span></a>
  <a href="/download"><span class="yc-quick-icon" aria-hidden="true">▤</span><span><b>手機輕鬆使用</b><small>iPhone・Android</small></span></a>
  <a href="/contact"><span class="yc-quick-icon" aria-hidden="true">◉</span><span><b>專人操作支援</b><small>教學・連線・客服</small></span></a>
</section>
{home_videos()}
<section class="portal-section premium-journal" aria-labelledby="journal-home-title">
  <div class="section-top"><div><p class="kicker">BACCARAT EDITORIAL</p><h2 id="journal-home-title">百家樂精選文章</h2><p>規則、路單與常見觀念；新文章發布後會自動更新精選內容。</p></div><a class="text-link" href="/articles">全部文章 {arrow()}</a></div>
  {article_cards(3, topic='baccarat')}
</section>
{scarab_ad('billboard',0)}
<p class="home-risk">分析工具僅供輔助，不保證預測遊戲結果或獲利。</p>
</div>'''
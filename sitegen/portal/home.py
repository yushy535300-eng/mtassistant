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
  <p class="atelier-statement">看清資訊，<span>從容操作。</span></p><p class="yc-hero-description">多桌觀察、模型分析與條件管理。<br>為你的每一步，建立清楚的操作順序。</p>
  <div class="hero-actions">{button('探索雙核心工具','#toolbox')}<a class="hero-film" href="#mt-videos"><span aria-hidden="true">▶</span>觀看實際操作</a></div>
  <div class="atelier-hero-tags"><span>多平台資訊</span><span>真實操作介面</span><span>電腦・手機</span></div></div>
  <div class="atelier-hero-note"><span>THE YUCE EXPERIENCE</span><i></i><small>從資訊整理，到操作執行。</small></div><div class="yc-hero-controls" aria-label="荷官輪播"><button type="button" data-dealer-step="-1" aria-label="上一張荷官照片">‹</button><span class="yc-hero-counter" aria-live="off"><span data-dealer-current>01</span><span class="yc-hero-counter-divider"></span><span data-dealer-total>11</span></span><button type="button" data-dealer-step="1" aria-label="下一張荷官照片">›</button></div>
</section>
<nav class="atelier-section-nav" aria-label="首頁內容導覽"><a href="#toolbox" aria-current="location">工具總覽</a><a href="#matrix-title">多桌輔助</a><a href="#auto-title">自動下注</a><a href="#guide-title">使用教學</a><a href="#mt-videos">操作影片</a><a href="#journal-home-title">使用指南</a><span>SCROLL TO EXPLORE ↓</span></nav>
<section class="portal-section yc-tool-showcase" id="toolbox" aria-labelledby="tools-title"><div class="section-top"><div><p class="kicker">TWO TOOLS. ONE CLEAR WORKFLOW.</p><h2 id="tools-title">觀察與執行，<em>各有專長。</em></h2><p>兩套獨立系統，各自清楚、彼此有序。</p></div></div>
<div class="portal-tool-grid">
<article class="tool-tile atelier-matrix"><div class="atelier-product-head"><div class="atelier-product-code">01 <span>MT MATRIX</span></div>{tool_icon()}<h3>多桌百家輔助</h3><p>把桌台、牌路與模型資訊，放進同一個觀察視野。</p></div><div class="atelier-product-canvas"><span class="atelier-canvas-label">ACTUAL PRODUCT INTERFACE</span>{screen('matrix-assist','多桌百家輔助・真實分析主面板',eager=True)}<div class="atelier-canvas-shadow" aria-hidden="true"></div></div><div class="atelier-product-bottom"><div class="atelier-product-tags"><span>多桌雷達</span><span>AI 綜合</span><span>四式・奇偶</span></div><div class="inline-actions">{button('探索多桌功能','/features')}<a class="text-link" href="{MATRIX}">進入系統 {arrow()}</a></div></div></article>
<article class="tool-tile auto atelier-auto"><div class="atelier-product-head"><div class="atelier-product-code">02 <span>MT AUTO</span></div>{tool_icon(True)}<h3>百家自動下注</h3><p>從配注條件到執行紀錄，讓操作步驟清楚可循。</p></div><div class="atelier-product-canvas atelier-auto-canvas"><span class="atelier-canvas-label">SETUP / EXECUTION / HISTORY</span><div class="atelier-auto-main">{screen('auto-running','百家自動下注・真實執行面板',eager=True)}</div><div class="atelier-auto-setting">{screen('auto-strategy','百家自動下注・真實配注設定')}</div><div class="atelier-canvas-shadow" aria-hidden="true"></div></div><div class="atelier-product-bottom"><div class="atelier-product-tags"><span>配注設定</span><span>停止條件</span><span>執行紀錄</span></div><div class="inline-actions">{button('了解自動下注','/auto')}<a class="text-link" href="{AUTO}">進入系統 {arrow()}</a></div></div></article>
</div></section>
<nav class="portal-shortcuts yc-service-strip" aria-label="首頁快速入口"><a href="/features">{tool_icon()}<span><b>多桌資訊整合</b><small>桌台・牌路・模型</small></span></a><a href="/auto">{tool_icon(True)}<span><b>操作條件管理</b><small>配注・限制・紀錄</small></span></a><a href="/download"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="8" y="2" width="16" height="28" rx="3"/><path d="M13 26h6M16 7v12m-4-4 4 4 4-4"/></svg><span><b>手機輕鬆使用</b><small>iPhone・Android</small></span></a><a href="/contact"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 17v-3a11 11 0 0 1 22 0v3M5 16H3v9h6v-9H5Zm22 0h-4v9h6v-9h-2Zm0 9c0 3-4 4-9 4"/></svg><span><b>專人操作支援</b><small>帳號・連線・教學</small></span></a></nav>
<section class="portal-section premium-product-story" aria-labelledby="matrix-title"><div class="story-copy"><p class="kicker">01 ／ OBSERVE WITH CLARITY</p><h2 id="matrix-title">資訊再多，<br><em>也要看得清楚。</em></h2><p>先確認桌台與連線，再選擇分析模型。MT MATRIX 將多桌觀察、AI 綜合、四式算牌與終值奇偶，整理成清楚的操作路徑。</p><ul class="story-points"><li><span>01</span>多桌雷達與平台連線</li><li><span>02</span>AI 綜合與模型切換</li><li><span>03</span>牌面、公式與終值核對</li></ul><a class="text-link" href="/features">探索多桌百家輔助 {arrow()}</a></div>
<div class="story-stage"><div class="stage-top"><span>MT MATRIX</span><span>真實程式內頁</span></div><div class="focus-tabs" role="tablist" aria-label="MT MATRIX 介面展示"><button type="button" id="tab-cards" data-tab="cards" role="tab" aria-controls="focus-cards" aria-selected="true">四式算牌</button><button type="button" id="tab-parity" data-tab="parity" role="tab" aria-controls="focus-parity" aria-selected="false" tabindex="-1">終值奇偶</button><button type="button" id="tab-assist" data-tab="assist" role="tab" aria-controls="focus-assist" aria-selected="false" tabindex="-1">AI 綜合</button></div><div id="focus-cards" role="tabpanel" aria-labelledby="tab-cards">{screen('four-formulas','MT MATRIX V38 四式算牌')}</div><div id="focus-parity" role="tabpanel" aria-labelledby="tab-parity" hidden>{screen('parity-model','MT MATRIX 終值奇偶模型')}</div><div id="focus-assist" role="tabpanel" aria-labelledby="tab-assist" hidden>{screen('matrix-assist','MT MATRIX AI 綜合分析')}</div><p class="stage-caption">原始介面截圖，可點擊放大查看。</p></div></section>
<section class="portal-section premium-product-story auto-story" aria-labelledby="auto-title"><div class="story-stage auto-stage"><div class="stage-top"><span>MT AUTO</span><span>設定與執行</span></div><div class="auto-stage-inner"><div class="auto-screen">{screen('auto-running','MT AUTO 自動下注執行面板')}</div><div class="auto-settings"><div><span>01</span><h3>配注方式</h3><p>核對推薦來源與開始條件。</p></div><div><span>02</span><h3>金額與限制</h3><p>確認單注、上限與停止條件。</p></div><div><span>03</span><h3>執行紀錄</h3><p>掌握狀態，回看操作資訊。</p></div></div></div><p class="stage-caption">畫面為原始截圖，實際狀態以程式為準。</p></div><div class="story-copy"><p class="kicker">02 ／ EXECUTE WITH CONTROL</p><h2 id="auto-title">設定有條理，<br><em>執行有紀錄。</em></h2><p>啟動前，逐項確認配注、金額與停止條件；開始後，查看執行面板與紀錄。把設定與狀態分開理解，操作更有順序。</p><a class="text-link" href="/auto">了解自動下注設定 {arrow()}</a><a class="story-reading" href="/articles/auto-checklist">開始前必讀：五項設定核對清單 {arrow()}</a></div></section>
<section class="portal-section premium-guide" aria-labelledby="guide-title"><div class="section-top"><div><p class="kicker">START WITH THE RIGHT STEPS</p><h2 id="guide-title">把第一步，走得更順。</h2><p>從開啟程式，到熟悉操作，找到你需要的完整教學。</p></div><a class="text-link" href="/guide">全部操作教學 {arrow()}</a></div><div class="premium-guide-grid"><a class="guide-entry" href="/download"><span class="guide-number">01</span><div><h3>選擇你的裝置</h3><p>iPhone、Android 與電腦使用方式。</p></div>{arrow()}</a><a class="guide-entry" href="/guide?system=matrix"><span class="guide-number">02</span><div><h3>熟悉多桌輔助</h3><p>五步確認連線、桌台與模型。</p></div>{arrow()}</a><a class="guide-entry" href="/guide?system=auto"><span class="guide-number">03</span><div><h3>完成自動下注設定</h3><p>六步核對配注、金額與停止條件。</p></div>{arrow()}</a></div></section>
{home_videos()}
<section class="portal-section premium-journal" aria-labelledby="journal-home-title"><div class="section-top"><div><p class="kicker">THE YUCE JOURNAL</p><h2 id="journal-home-title">真正實用的操作內容。</h2><p>不只介紹功能，也把使用方法與判讀重點說清楚。</p></div><a class="text-link" href="/articles">探索文章專區 {arrow()}</a></div>{article_cards(3)}</section>
{scarab_ad('billboard',0)}
<section class="portal-section premium-support" aria-labelledby="help-title"><div><p class="kicker">WE ARE HERE TO HELP</p><h2 id="help-title">問題，留給我們一起解決。</h2><p>登入授權、連線或操作設定，從常見問題開始，或直接聯繫客服。</p><div class="inline-actions">{button('LINE 操作支援',LINE)}<a class="text-link" href="/faq">查看全部問題 {arrow()}</a></div></div><div class="home-faq">{questions}</div></section>
<p class="home-risk">分析與配注策略僅供輔助，無法保證預測下一局或獲利。請先理解工具用途與限制。</p>
</div>'''

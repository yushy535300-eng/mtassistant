from ..common import DATA, MATRIX, AUTO, LINE, logo, screen, button, arrow, image_note, dealer
from html import escape
import importlib
from .v2 import comparison, knowledge
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
    questions = ''.join(f'<details class="faq-item"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for _, q, a in DATA['questions'][:3])
    return f'''<div class="portal-home">
<section class="portal-banner" aria-labelledby="home-title"><picture class="banner-art" aria-hidden="true"><source media="(max-width:640px)" srcset="{BANNER_MOBILE}"><img src="{BANNER_DESKTOP}" width="1920" height="823" alt="" fetchpriority="high"></picture><div class="banner-light" aria-hidden="true"></div><canvas class="banner-sparks" aria-hidden="true"></canvas><div class="banner-copy"><p class="banner-label">M T &nbsp; A S S I S T A N T</p><h1 id="home-title" class="yc-art-title">{title_ornament()}<span class="yc-title-text">御策百家輔助</span><img src="/assets/brand/yuce-gold-title.svg" width="6060" height="1110" alt="" aria-hidden="true"></h1><p class="yc-hero-subtitle">多桌監控 <i>×</i> 智慧分析 <i>×</i> 自動策略</p><p class="yc-hero-description">兩套獨立輔助工具，專注牌路觀察與策略執行。</p>{button('立即體驗', '#toolbox')}<span class="banner-risk">分析與策略僅供輔助，不保證結果。</span></div><div class="yc-hero-controls" aria-label="荷官輪播"><button type="button" data-dealer-step="-1" aria-label="上一張荷官照片">‹</button><span class="yc-hero-counter" aria-live="off"><span data-dealer-current>01</span><span class="yc-hero-counter-divider"></span><span data-dealer-total>11</span></span><button type="button" data-dealer-step="1" aria-label="下一張荷官照片">›</button></div></section>





<section class="portal-section yc-tool-showcase" id="toolbox" aria-labelledby="tools-title"><div class="section-top"><div><h2 id="tools-title">御策雙核心系統</h2><p>多桌觀察與策略執行，兩套系統各自獨立。</p></div><a class="text-link" href="/guide">查看教學 {arrow()}</a></div><div class="portal-tool-grid">
<article class="tool-tile"><div class="tool-tile-copy"><div class="product-heading">{tool_icon()}<div><span>MT MATRIX</span><h3>多桌百家輔助</h3></div></div><p>把桌台、牌路與分析資訊集中查看。支援雷達、AI 綜合、四式算牌與終值奇偶。</p><div class="inline-actions">{button('進入系統', MATRIX)}<a href="/features" class="text-link">了解多桌功能 {arrow()}</a></div></div><div class="tool-tile-preview">{screen('matrix-assist', '多桌百家輔助・真實分析主面板', eager=True)}</div></article>
<article class="tool-tile auto"><div class="tool-tile-copy"><div class="product-heading">{tool_icon(True)}<div><span>MT AUTO</span><h3>百家自動下注</h3></div></div><p>確認配注策略、金額與停止條件，再查看執行狀態與紀錄。</p><div class="inline-actions">{button('進入系統', AUTO)}<a href="/auto" class="text-link">了解設定流程 {arrow()}</a></div></div><div class="tool-tile-preview">{screen('auto-running', '百家自動下注・真實執行面板', eager=True)}</div></article>
</div></section>
<nav class="portal-shortcuts yc-service-strip" aria-label="首頁快速入口"><a href="/features"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="26" height="19" rx="2"/><path d="M10 29h12M16 24v5M8 18l5-5 4 3 7-8"/></svg><span class="yc-shortcut-copy"><b>多桌監控</b><small>多桌牌路・雷達分析</small></span></a><a href="/auto"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="16" cy="16" r="10"/><circle cx="16" cy="16" r="4"/><path d="M16 2v6m0 16v6M2 16h6m16 0h6"/></svg><span class="yc-shortcut-copy"><b>策略設定</b><small>配注條件・執行紀錄</small></span></a><a href="/guide"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M16 6c-5-3-10-3-13-1v21c4-2 9-2 13 1 4-3 9-3 13-1V5c-3-2-8-2-13 1Zm0 0v21"/></svg><span class="yc-shortcut-copy"><b>操作教學</b><small>完整步驟・快速上手</small></span></a><a href="/contact"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 17v-3a11 11 0 0 1 22 0v3M5 16H3v9h6v-9H5Zm22 0h-4v9h6v-9h-2Zm0 9c0 3-4 4-9 4"/></svg><span class="yc-shortcut-copy"><b>專人客服</b><small>LINE 聯繫・操作支援</small></span></a></nav>
<section class="portal-section" aria-labelledby="guide-title"><div class="section-top"><div><h2 id="guide-title">操作教學</h2><p>兩套工具各自的教學，不混用入口與流程。</p></div><a class="text-link" href="/guide">完整操作教學 {arrow()}</a></div><div class="two-column"><a class="guide-entry" href="/guide?system=matrix"><span class="guide-number">05</span><div>{logo()}<h3>MT MATRIX 教學</h3><p>帳號授權 → 平台連線 → 模型 → 四式 → 奇偶</p></div>{arrow()}</a><a class="guide-entry" href="/guide?system=auto"><span class="guide-number">06</span><div>{logo(True)}<h3>MT AUTO 教學</h3><p>連線 → 配注 → 金額 → 時間 → 停止 → 執行</p></div>{arrow()}</a></div></section>
{scarab_ad('billboard', 0)}
{home_videos()}
{comparison()}

<section class="portal-section" aria-labelledby="matrix-title"><div class="section-top"><div><p class="kicker">MT MATRIX</p><h2 id="matrix-title">多桌資訊，集中查看</h2></div><a class="text-link" href="/features">全部功能 {arrow()}</a></div><div class="matrix-overview"><div class="portal-panel"><div class="radar-scroll">{screen('multitable-radar', 'MT MATRIX 多桌雷達完整介面')}</div>{image_note()}</div><div class="feature-list"><article><span class="feature-index">01</span><div><h3>多桌雷達與平台連線</h3><p>先確認連線狀態，再選擇要觀察的桌台。</p></div></article><article><span class="feature-index">02</span><div><h3>AI 綜合與四式算牌</h3><p>切換分析模型，對照不同方式的資訊。</p></div></article><article><span class="feature-index">03</span><div><h3>終值奇偶與牌路</h3><p>將牌路與模型數據放在同一個觀察流程。</p></div></article></div></div></section>

<section class="portal-section" aria-labelledby="auto-title"><div class="section-top"><div><p class="kicker">MT AUTO</p><h2 id="auto-title">設定條件，再查看執行</h2></div><a class="text-link" href="/auto">了解自動下注 {arrow()}</a></div><div class="three-column auto-summary"><article class="portal-panel"><span class="feature-index">01</span><h3>推薦與配注策略</h3><p>設定平台、房間、推薦方式與配注方法。</p>{screen('auto-strategy', 'MT AUTO 配注與推薦策略')}</article><article class="portal-panel"><span class="feature-index">02</span><h3>金額與停止條件</h3><p>確認單注、上限、時間、止損與止盈。</p>{screen('auto-limits', 'MT AUTO 止損止盈設定')}</article><article class="portal-panel"><span class="feature-index">03</span><h3>執行與紀錄</h3><p>查看目前狀態與累積紀錄，實際結果以系統為準。</p>{screen('auto-history', 'MT AUTO 執行紀錄')}</article></div>{image_note()}</section>

<section class="portal-section" aria-labelledby="preview-title"><div class="section-top"><div><h2 id="preview-title">產品介面速覽</h2><p>切換功能，點擊圖片查看完整原圖。</p></div></div><div class="portal-panel interface-browser"><div class="focus-tabs" role="tablist" aria-label="MT MATRIX 介面展示"><button type="button" id="tab-cards" data-tab="cards" role="tab" aria-controls="focus-cards" aria-selected="true">四式算牌</button><button type="button" id="tab-parity" data-tab="parity" role="tab" aria-controls="focus-parity" aria-selected="false" tabindex="-1">終值奇偶</button><button type="button" id="tab-assist" data-tab="assist" role="tab" aria-controls="focus-assist" aria-selected="false" tabindex="-1">AI 綜合</button></div><div id="focus-cards" role="tabpanel" aria-labelledby="tab-cards">{screen('four-formulas', 'MT MATRIX V38 四式算牌')}</div><div id="focus-parity" role="tabpanel" aria-labelledby="tab-parity" hidden>{screen('parity-model', 'MT MATRIX 終值奇偶模型')}</div><div id="focus-assist" role="tabpanel" aria-labelledby="tab-assist" hidden>{screen('matrix-assist', 'MT MATRIX AI 綜合分析')}</div>{image_note()}</div></section>



{knowledge()}

<section class="portal-section brand-section" aria-labelledby="brand-title"><div class="brand-scene">{person('mt-real-02', 'brand')}<div class="brand-scene-light" aria-hidden="true"></div></div><div class="brand-copy"><p class="kicker">御策百家輔助</p><h2 id="brand-title">用途清楚，操作有序。</h2><p>御策整理多桌觀察與策略執行的工具資訊，提供真實介面、操作教學與聯繫方式。資訊輔助不能消除風險，請先理解用途和限制。</p><a class="text-link" href="/faq">了解使用方式與風險 {arrow()}</a></div></section>

<section class="portal-section" aria-labelledby="help-title"><div class="section-top"><div><h2 id="help-title">常見問題與操作支援</h2></div><a class="text-link" href="/faq">全部問題 {arrow()}</a></div><div class="support-overview"><div>{questions}</div><aside class="portal-panel support-panel"><h3>遇到操作問題？</h3><p>提供系統名稱、裝置與錯誤畫面，方便客服協助。請勿提供密碼或驗證碼。</p>{button('聯繫 LINE 客服', LINE)}<a class="text-link" href="/contact">聯繫前準備 {arrow()}</a></aside></div></section>
</div>'''

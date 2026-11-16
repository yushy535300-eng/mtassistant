from ..common import DATA, MATRIX, AUTO, LINE, logo, screen, button, arrow, image_note, dealer
from html import escape
import importlib
from .v2 import comparison, knowledge
from .dealers import person
from .motion import home_videos

BANNER_DESKTOP = '/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-1.webp'
BANNER_MOBILE = '/manus-storage/async-images/5IpvgHPwOi5uABZyAx9lXZ/image-2.webp'


def render():
    questions = ''.join(f'<details class="faq-item"><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for _, q, a in DATA['questions'][:3])
    return f'''<div class="portal-home">
<section class="portal-banner" aria-labelledby="home-title"><picture class="banner-art" aria-hidden="true"><source media="(max-width:640px)" srcset="{BANNER_MOBILE}"><img src="{BANNER_DESKTOP}" width="1920" height="823" alt="" fetchpriority="high"></picture><div class="banner-light" aria-hidden="true"></div><canvas class="banner-sparks" aria-hidden="true"></canvas><div class="banner-copy"><p class="banner-label">MT MATRIX × MT AUTO</p><h1 id="home-title">百家輔助工具，<br>一次掌握。</h1><p>多桌牌路與配注設定。<br>兩套工具，各自獨立。</p>{button('聯繫 LINE 客服', LINE)}<span class="banner-risk">分析與策略僅供輔助，不保證結果。</span></div></section>

<div class="portal-direct-tools" aria-label="直接選擇工具"><a href="{MATRIX}" class="button">{logo()}多桌輔助 {arrow()}</a><a href="{AUTO}" class="button outline">{logo(True)}自動下注 {arrow()}</a></div>
<nav class="portal-shortcuts" aria-label="首頁快速入口"><a href="/features"><span>MT MATRIX</span><b>多桌輔助</b>{arrow()}</a><a href="/auto"><span>MT AUTO</span><b>自動下注</b>{arrow()}</a><a href="/guide"><span>開始之前</span><b>操作教學</b>{arrow()}</a><a href="/contact"><span>需要協助</span><b>聯繫客服</b>{arrow()}</a></nav>


<section class="portal-section" id="toolbox" aria-labelledby="tools-title"><div class="section-top"><div><h2 id="tools-title">選擇你的工具</h2><p>多桌觀察與策略執行，兩套系統各自獨立。</p></div><a class="text-link" href="/guide">查看教學 {arrow()}</a></div><div class="portal-tool-grid">
<article class="tool-tile"><div class="tool-tile-copy"><div class="product-heading">{logo()}<div><span>MT MATRIX</span><h3>多桌百家輔助</h3></div></div><p>把桌台、牌路與分析資訊集中查看。支援雷達、AI 綜合、四式算牌與終值奇偶。</p><div class="inline-actions">{button('進入系統', MATRIX)}<a href="/features" class="text-link">了解多桌功能 {arrow()}</a></div></div><div class="tool-tile-preview">{screen('matrix-assist', 'MT MATRIX 多桌百家輔助主面板')}</div></article>
<article class="tool-tile auto"><div class="tool-tile-copy"><div class="product-heading">{logo(True)}<div><span>MT AUTO</span><h3>百家自動下注</h3></div></div><p>確認配注策略、金額與停止條件，再查看執行狀態與紀錄。</p><div class="inline-actions">{button('進入系統', AUTO)}<a href="/auto" class="text-link">了解設定流程 {arrow()}</a></div></div><div class="tool-tile-preview">{screen('auto-running', 'MT AUTO 自動下注執行面板')}</div></article>
</div></section>
{home_videos()}
{comparison()}

<section class="portal-section" aria-labelledby="matrix-title"><div class="section-top"><div><p class="kicker">MT MATRIX</p><h2 id="matrix-title">多桌資訊，集中查看</h2></div><a class="text-link" href="/features">全部功能 {arrow()}</a></div><div class="matrix-overview"><div class="portal-panel"><div class="radar-scroll">{screen('multitable-radar', 'MT MATRIX 多桌雷達完整介面')}</div>{image_note()}</div><div class="feature-list"><article><span class="feature-index">01</span><div><h3>多桌雷達與平台連線</h3><p>先確認連線狀態，再選擇要觀察的桌台。</p></div></article><article><span class="feature-index">02</span><div><h3>AI 綜合與四式算牌</h3><p>切換分析模型，對照不同方式的資訊。</p></div></article><article><span class="feature-index">03</span><div><h3>終值奇偶與牌路</h3><p>將牌路與模型數據放在同一個觀察流程。</p></div></article></div></div></section>

<section class="portal-section" aria-labelledby="auto-title"><div class="section-top"><div><p class="kicker">MT AUTO</p><h2 id="auto-title">設定條件，再查看執行</h2></div><a class="text-link" href="/auto">了解自動下注 {arrow()}</a></div><div class="three-column auto-summary"><article class="portal-panel"><span class="feature-index">01</span><h3>推薦與配注策略</h3><p>設定平台、房間、推薦方式與配注方法。</p>{screen('auto-strategy', 'MT AUTO 配注與推薦策略')}</article><article class="portal-panel"><span class="feature-index">02</span><h3>金額與停止條件</h3><p>確認單注、上限、時間、止損與止盈。</p>{screen('auto-limits', 'MT AUTO 止損止盈設定')}</article><article class="portal-panel"><span class="feature-index">03</span><h3>執行與紀錄</h3><p>查看目前狀態與累積紀錄，實際結果以系統為準。</p>{screen('auto-history', 'MT AUTO 執行紀錄')}</article></div>{image_note()}</section>

<section class="portal-section" aria-labelledby="preview-title"><div class="section-top"><div><h2 id="preview-title">產品介面速覽</h2><p>切換功能，點擊圖片查看完整原圖。</p></div></div><div class="portal-panel interface-browser"><div class="focus-tabs" role="tablist" aria-label="MT MATRIX 介面展示"><button type="button" id="tab-cards" data-tab="cards" role="tab" aria-controls="focus-cards" aria-selected="true">四式算牌</button><button type="button" id="tab-parity" data-tab="parity" role="tab" aria-controls="focus-parity" aria-selected="false" tabindex="-1">終值奇偶</button><button type="button" id="tab-assist" data-tab="assist" role="tab" aria-controls="focus-assist" aria-selected="false" tabindex="-1">AI 綜合</button></div><div id="focus-cards" role="tabpanel" aria-labelledby="tab-cards">{screen('four-formulas', 'MT MATRIX V38 四式算牌')}</div><div id="focus-parity" role="tabpanel" aria-labelledby="tab-parity" hidden>{screen('parity-model', 'MT MATRIX 終值奇偶模型')}</div><div id="focus-assist" role="tabpanel" aria-labelledby="tab-assist" hidden>{screen('matrix-assist', 'MT MATRIX AI 綜合分析')}</div>{image_note()}</div></section>

<section class="portal-section" aria-labelledby="guide-title"><div class="section-top"><div><h2 id="guide-title">跟著步驟開始</h2><p>兩套工具各自的教學，不混用入口與流程。</p></div><a class="text-link" href="/guide">完整操作教學 {arrow()}</a></div><div class="two-column"><a class="guide-entry" href="/guide?system=matrix"><span class="guide-number">05</span><div>{logo()}<h3>MT MATRIX 教學</h3><p>帳號授權 → 平台連線 → 模型 → 四式 → 奇偶</p></div>{arrow()}</a><a class="guide-entry" href="/guide?system=auto"><span class="guide-number">06</span><div>{logo(True)}<h3>MT AUTO 教學</h3><p>連線 → 配注 → 金額 → 時間 → 停止 → 執行</p></div>{arrow()}</a></div></section>

{knowledge()}

<section class="portal-section brand-section" aria-labelledby="brand-title"><div class="brand-scene">{person('mt-real-02', 'brand')}<div class="brand-scene-light" aria-hidden="true"></div></div><div class="brand-copy"><p class="kicker">御策百家輔助</p><h2 id="brand-title">用途清楚，操作有序。</h2><p>御策整理多桌觀察與策略執行的工具資訊，提供真實介面、操作教學與聯繫方式。資訊輔助不能消除風險，請先理解用途和限制。</p><a class="text-link" href="/faq">了解使用方式與風險 {arrow()}</a></div></section>

<section class="portal-section" aria-labelledby="help-title"><div class="section-top"><div><h2 id="help-title">常見問題與操作支援</h2></div><a class="text-link" href="/faq">全部問題 {arrow()}</a></div><div class="support-overview"><div>{questions}</div><aside class="portal-panel support-panel"><h3>遇到操作問題？</h3><p>提供系統名稱、裝置與錯誤畫面，方便客服協助。請勿提供密碼或驗證碼。</p>{button('聯繫 LINE 客服', LINE)}<a class="text-link" href="/contact">聯繫前準備 {arrow()}</a></aside></div></section>
</div>'''

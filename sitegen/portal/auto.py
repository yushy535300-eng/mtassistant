from html import escape

from ..common import AUTO, DATA, LINE, MATRIX, arrow, button, image_note, logo, screen
import importlib


def _step_links(references):
    if not references:
        return ''
    links = []
    for anchor, label in references:
        links.append(f'<a class="text-link" href="#{escape(anchor, quote=True)}">{escape(label)} {arrow()}</a>')
    return '<div class="inline-actions">' + ''.join(links) + '</div>'


def _flow_steps():
    items = []
    for number, step in enumerate(DATA['auto_steps'], start=1):
        title, summary, detail, references = step
        items.append(
            f'''<li>
                <strong>{number:02d} · {escape(title)}</strong>
                <p>{escape(summary)}</p>
                <span>{escape(detail)}</span>
                {_step_links(references)}
            </li>'''
        )
    return '<ol class="feature-list">' + ''.join(items) + '</ol>'


def render():
    return f'''
<section class="portal-pagehead">
  <div>
    <p class="kicker">MT AUTO · 設定與執行</p>
    <h1>MT AUTO 自動下注</h1>
    <p>集中核對推薦、配注、金額與停止條件，再查看執行狀態與紀錄。實際登入、送單與結算由既有 MT AUTO 系統處理。</p>
  </div>
  <div class="pagehead-actions">
    {button('開啟 MT AUTO', AUTO)}
    <a class="text-link" href="/guide?system=auto">查看自動下注教學 {arrow()}</a>
  </div>
</section>

<section class="portal-section" aria-labelledby="auto-settings-title">
  <div class="section-top">
    <h2 id="auto-settings-title">先完成設定，再開始執行</h2>
    <p>推薦與配注、投注金額、停止時間及止損止盈分開核對；不要把預設值視為本次操作設定。</p>
  </div>
  <div class="two-column">
    <div class="portal-panel">
      <h3>設定要核對的項目</h3>
      <ul class="feature-list">
        <li><strong>推薦與配注</strong><p>確認推薦來源、開始方式與配注方式。選擇馬丁時，先閱讀跨局階梯及多桌限制說明。</p></li>
        <li><strong>基本單注與單筆上限</strong><p>確認基本單注與每筆上限，避免沿用不符合本次需求的金額。</p></li>
        <li><strong>自動停止時間</strong><p>確認分鐘數；時間到後停止新增下注，已接受注單的後續結算依程式顯示。</p></li>
        <li><strong>止損與止盈</strong><p>設定停止條件，並在送單前重新核對配注與金額限制。</p></li>
      </ul>
      <div class="portal-notice"><strong>核對提醒</strong><br>百家樂結果具有不確定性；分析方向與配注策略不保證預測下一局或獲利。</div>
    </div>
    <div class="portal-panel">
      <div class="product-heading">
        {logo(auto=True)}
        <div><h3>MT AUTO 設定面板</h3><p>推薦方式、配注策略與開始條件。</p></div>
      </div>
      <div class="media-display" id="auto-strategy">
        {screen('auto-strategy', '自動下注推薦與配注設定', eager=True)}
      </div>
      {image_note()}
    </div>
  </div>
</section>


<section class="portal-section" aria-labelledby="auto-visuals-title">
  <div class="section-top">
    <h2 id="auto-visuals-title">設定畫面與執行紀錄</h2>
    <p>以下為既有產品介面截圖，用來辨識設定位置與狀態欄位；不是即時桌台或實際送單畫面。</p>
  </div>
  <div class="two-column">
    <div class="portal-panel">
      <h3>金額、時間與限制</h3>
      <div class="media-display" id="auto-amount">
        {screen('auto-amount', '自動下注投注金額設定')}
      </div>
      <div class="media-display" id="auto-timer">
        {screen('auto-timer', '自動停止時間設定')}
      </div>
      <div class="media-display" id="auto-limits">
        {screen('auto-limits', '止損與止盈設定')}
      </div>
      {image_note()}
    </div>
    <div class="portal-panel">
      <h3>開始後查看狀態</h3>
      <div class="media-display narrow-media" id="auto-running">
        {screen('auto-running', '自動下注執行面板')}
      </div>
      <div class="media-display" id="auto-history">
        {screen('auto-history', '執行紀錄與目前狀態')}
      </div>
      <p class="portal-notice">需要停止時使用程式內的停止按鈕。若畫面顯示已停止，先讀取停止原因，再依提示確認是否需要手動重新開始。</p>
    </div>
  </div>
</section>

<section class="portal-section" aria-labelledby="auto-flow-title">
  <div class="section-top">
    <h2 id="auto-flow-title">六步使用流程</h2>
    <p>照順序確認，不跳過金額與停止條件；完整步驟與介面定位也可在自動下注教學查看。</p>
  </div>
  <div class="portal-panel">
    {_flow_steps()}
  </div>
</section>

<section class="portal-section" aria-labelledby="tool-difference-title">
  <div class="section-top">
    <h2 id="tool-difference-title">MT MATRIX 與 MT AUTO 的分工</h2>
    <p>兩套工具入口分開，請依要查看的資訊或要設定的執行條件進入對應系統。</p>
  </div>
  <div class="two-column">
    <div class="portal-panel">
      <div class="product-heading">
        {logo()}
        <div><h3>MT MATRIX 多桌百家輔助</h3><p>整理桌台、牌路、AI 分析、V38 四式與終值奇偶資訊。</p></div>
      </div>
      <div class="inline-actions">{button('進入 MT MATRIX', MATRIX, 'outline')}</div>
    </div>
    <div class="portal-panel">
      <div class="product-heading">
        {logo(auto=True)}
        <div><h3>MT AUTO 自動下注</h3><p>集中處理推薦與配注、金額、停止條件、執行狀態與紀錄。</p></div>
      </div>
      <div class="inline-actions">{button('進入 MT AUTO', AUTO)}</div>
    </div>
  </div>
</section>

<section class="action-strip" aria-label="自動下注下一步">
  <div>
    <h2>準備查看設定？</h2>
    <p>先讀完六步教學，再由既有入口登入 MT AUTO。登入或授權問題請聯繫官方 LINE，請勿提供密碼。</p>
  </div>
  <div class="inline-actions">
    {button('閱讀自動下注教學', '/guide?system=auto', 'outline')}
    {button('開啟 MT AUTO', AUTO)}
    <a class="text-link" href="{LINE}">LINE 官方客服 {arrow()}</a>
  </div>
</section>
'''

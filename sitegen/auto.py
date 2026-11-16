from .common import (
    AUTO,
    DATA,
    LINE,
    MATRIX,
    arrow,
    ambient,
    button,
    chapter,
    dealer,
    eyebrow,
    image_note,
    logo,
    screen,
)


def render():
    """Return the MT AUTO page body; the site builder adds head, header and footer."""
    return f'''
<div class="auto-page" id="auto-page">
  <section class="auto-hero" aria-labelledby="auto-hero-title">
    {ambient('auto')}
    <div class="wrap auto-hero-layout">
      <div class="auto-hero-copy">
        <div class="auto-hero-kicker"><span></span>MT AUTO／自動下注</div>
        <div class="auto-hero-identity">
          {logo(auto=True, cls='auto-hero-logo')}
          <div><strong>MT AUTO</strong><small>自動下注工具</small></div>
        </div>
        {eyebrow('條件設定・策略管理・執行紀錄')}
        <h1 id="auto-hero-title">先把條件<br><em>設定清楚。</em></h1>
        <p>從推薦與配注，到注額、時間、止損止盈，<br>每一次執行都先留下可以核對的設定。</p>
        <div class="auto-hero-actions">
          {button('開啟 MT AUTO', AUTO, 'primary')}
          {button('閱讀自動下注教學', '/guide?system=auto', 'outline')}
        </div>
        <p class="auto-hero-limit">官網只展示介面與操作脈絡，不建立送單或自動下注控制；所有限制以程式內顯示為準。</p>
      </div>
      <div class="auto-hero-visual">
        <div class="auto-visual-meta"><span>MT AUTO／執行面板</span><span>原比例・可放大</span></div>
        <div class="auto-running-frame">
          {screen('auto-running', '百家自動下注執行面板', 'auto-screen auto-running-screen', eager=True)}
        </div>
        <p class="auto-visual-caption">主畫面為實際 MT AUTO 介面；點擊可查看原始尺寸。</p>
      </div>
    </div>
    <div class="wrap auto-hero-baseline">
      <span>設定完成，再開始。</span>
      <div><b>01 策略</b><i></i><b>02 條件</b><i></i><b>03 紀錄</b></div>
      <a href="#auto-strategy">向下閱讀 {arrow()}</a>
    </div>
  </section>

  <nav class="auto-section-index" aria-label="自動下注頁面段落導覽">
    <div class="wrap">
      <a href="#auto-strategy"><span>01</span>策略與配注</a>
      <a href="#auto-amount"><span>02</span>金額與時間</a>
      <a href="#auto-limits"><span>03</span>止損止盈</a>
      <a href="#auto-history"><span>04</span>執行紀錄</a>
      <a href="#auto-difference"><span>05</span>兩套工具差異</a>
    </div>
  </nav>

  <section class="auto-story auto-story-paper" id="auto-strategy" aria-labelledby="auto-strategy-title">
    <div class="wrap auto-story-layout">
      <div class="auto-story-copy">
        {chapter('01', '策略先行，<br><em>再讓設定落地。</em>', '在「推薦與配注」確認配注方式、開始方式及推薦來源。若選擇馬丁，請先閱讀程式內的跨局階梯與多桌限制說明。', 'auto-strategy-title')}
        <div class="auto-numbered-notes">
          <div><b>01</b><span>選擇配注方式</span></div>
          <div><b>02</b><span>確認開始方式與基本額</span></div>
          <div><b>03</b><span>選擇推薦來源</span></div>
        </div>
        <a class="text-link auto-copy-link" href="/guide?system=auto#auto-step2">查看推薦與配注教學 {arrow()}</a>
      </div>
      <div class="auto-story-image auto-portrait-frame">
        {screen('auto-strategy', '推薦與配注設定', 'auto-screen')}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="auto-story auto-amount" id="auto-amount" aria-labelledby="auto-amount-title">
    <div class="wrap auto-story-layout auto-story-reverse">
      <div class="auto-story-copy">
        {eyebrow('02／投注金額與停止時間')}
        <h2 id="auto-amount-title">注額與時間，<br><em>先設清楚。</em></h2>
        <p>在「投注金額」設定基本單注與單筆上限，再確認「自動停止時間（分鐘）」欄位。開始前逐項核對，操作中查看執行狀態。</p>
        <div class="auto-rule-list">
          <div><span>基本單注</span><strong>先確認再開始</strong></div>
          <div><span>單筆上限</span><strong>避免沿用錯誤設定</strong></div>
          <div><span>停止時間</span><strong>時間到後停止新增下注</strong></div>
        </div>
      </div>
      <div class="auto-setting-stack">
        <div class="auto-setting-card auto-setting-wide">
          <span>投注金額</span>{screen('auto-amount', '投注金額設定', 'auto-screen')}
        </div>
        <div class="auto-setting-card auto-setting-timer">
          <span>自動停止時間</span>{screen('auto-timer', '自動停止時間設定', 'auto-screen')}
        </div>
        <p class="auto-setting-note">真實介面截圖，數值只代表畫面內容。</p>
      </div>
    </div>
  </section>

  <section class="auto-story auto-story-paper auto-limits" id="auto-limits" aria-labelledby="auto-limits-title">
    <div class="wrap auto-story-layout">
      <div class="auto-story-copy">
        {chapter('03', '停止條件。<br><em>也要先確認。</em>', '查看止損與止盈設定、核對說明，確認停止條件後再執行。已接受注單的後續結算方式與各項限制，以程式內顯示為準。', 'auto-limits-title')}
        <div class="auto-limit-callout">
          <span>執行前核對</span>
          <p>不要把歷史畫面、配注策略或任何分析方向理解為下一局結果的保證。</p>
        </div>
        <a class="text-link auto-copy-link" href="/faq">查看自動下注相關常見問題 {arrow()}</a>
      </div>
      <div class="auto-story-image auto-limit-frame">
        {screen('auto-limits', '止損與止盈設定', 'auto-screen')}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="auto-story auto-history" id="auto-history" aria-labelledby="auto-history-title">
    <div class="wrap auto-story-layout auto-story-reverse">
      <div class="auto-story-copy">
        {eyebrow('04／執行狀態與紀錄')}
        <h2 id="auto-history-title">執行紀錄。<br><em>隨時能回看。</em></h2>
        <p>依序查看送出、接受與結算事件。遇到停止狀態時，先閱讀面板原因，再確認後續操作；需要停止時，使用程式內的停止按鈕。</p>
        <p class="auto-subtle-note">本頁介面截圖中的金額與紀錄僅為畫面內容，不代表即時或未來結果。</p>
        <a class="text-link auto-copy-link" href="/guide?system=auto#auto-step6">閱讀執行與紀錄步驟 {arrow()}</a>
      </div>
      <div class="auto-history-stage">
        <div class="auto-history-label"><span>執行紀錄</span><span>送出／接受／結算</span></div>
        {screen('auto-history', '執行紀錄與目前狀態', 'auto-screen')}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="auto-scene" aria-label="設定前的提醒">
    <div class="wrap auto-scene-layout">
      <div class="auto-scene-copy">
        {eyebrow('設定前／先看清楚')}
        <h2>不是按下開始，<br><em>才想起限制。</em></h2>
        <p>停止時間、止損止盈、基本單注與單筆上限，都應在開始前逐項確認。這一頁是資訊整理，不是即時桌台，也不代替程式內的提示與核對。</p>
      </div>
    </div>
  </section>

  <section class="auto-human-section auto-story-paper" aria-labelledby="auto-human-title">
    <div class="wrap auto-human-layout">
      <div class="auto-human-copy">
        {eyebrow('獨立情境／非產品介面')}
        <h2 id="auto-human-title">留給操作的，<br><em>是清楚的節奏。</em></h2>
        <p>這一段只作品牌情境閱讀，不代表御策百家輔助官方荷官名單，也不代表任何合作或代言。MT 真人圖片為既有 Game+ 公開素材，商業授權尚未核實。</p>
        <p class="auto-source-note">來源註記：Game+ MT 人物展示素材／完整原圖，不裁切、不放大超過原始清晰度。</p>
      </div>
      <div class="auto-human-photo">
        {dealer('live2', label='Game+ MT 真人展示素材，非御策官方荷官名單')}
        <p>既有 Game+ 素材；非御策官方合作名單。</p>
      </div>
    </div>
  </section>

  <section class="auto-difference auto-story-paper" id="auto-difference" aria-labelledby="auto-difference-title">
    <div class="wrap">
      <div class="auto-section-intro">
        {eyebrow('兩套工具／各就其位')}
        <h2 id="auto-difference-title">先分清楚，<br><em>再選對入口。</em></h2>
        <p>MT MATRIX 與 MT AUTO 是兩套不同的產品。這一頁只說明自動下注的設定脈絡，不混用多桌輔助的功能與畫面。</p>
      </div>
      <div class="auto-difference-table" role="table" aria-label="MT MATRIX 與 MT AUTO 功能差異">
        <div class="auto-difference-row auto-difference-head" role="row">
          <span role="columnheader">比較面向</span><strong role="columnheader">MT MATRIX／多桌輔助</strong><strong role="columnheader">MT AUTO／自動下注</strong>
        </div>
        <div class="auto-difference-row" role="row"><span role="rowheader">主要任務</span><span role="cell">整理桌台、牌路與分析資訊</span><span role="cell">管理配注、條件與執行紀錄</span></div>
        <div class="auto-difference-row" role="row"><span role="rowheader">頁面內容</span><span role="cell">多桌雷達、AI 綜合、四式算牌、終值奇偶</span><span role="cell">策略、注額、時間、止損止盈、狀態</span></div>
        <div class="auto-difference-row" role="row"><span role="rowheader">正確入口</span><span role="cell"><a href="{MATRIX}">進入多桌輔助 {arrow()}</a></span><span role="cell"><a href="{AUTO}">進入自動下注 {arrow()}</a></span></div>
      </div>
      <div class="auto-difference-foot"><span>不確定要使用哪套？</span><a class="text-link" href="/faq">先閱讀常見問題 {arrow()}</a></div>
    </div>
  </section>

  <section class="auto-device" aria-labelledby="auto-device-title">
    <div class="wrap auto-device-layout">
      <div class="auto-device-copy">
        {eyebrow('裝置與瀏覽器')}
        <h2 id="auto-device-title">從瀏覽器進入，<br><em>不必另行安裝。</em></h2>
        <p>電腦、Android 手機與 iPhone 可使用瀏覽器開啟系統；實際平台、登入授權與遊戲操作方式，以登入後的程式介面為準。</p>
      </div>
      <ol class="auto-device-list">
        <li><b>01</b><span>電腦</span><small>適合完整查看設定與紀錄</small></li>
        <li><b>02</b><span>手機</span><small>Android 與 iPhone 以瀏覽器開啟</small></li>
        <li><b>03</b><span>開始前</span><small>確認平台、桌台、連線與目前狀態</small></li>
      </ol>
    </div>
  </section>

  <section class="auto-faq auto-story-paper" aria-labelledby="auto-faq-title">
    <div class="wrap auto-faq-layout">
      <div class="auto-faq-intro">
        {eyebrow('自動下注／常見問題')}
        <h2 id="auto-faq-title">開始之前，<br><em>把問題問完。</em></h2>
        <p>以下先整理本頁最相關的設定與狀態；完整分類與搜尋功能請前往常見問題。</p>
        <a class="text-link" href="/faq">前往完整 FAQ {arrow()}</a>
      </div>
      <div class="auto-faq-list">
        <details open><summary><span>開始前要確認哪些設定？</span><b>＋</b></summary><p>請確認配注方式、推薦來源、基本單注、單筆上限、止損、止盈及停止時間，再查看執行狀態。各項限制與核對方式以程式內說明為準。</p></details>
        <details><summary><span>畫面顯示停止時該怎麼處理？</span><b>＋</b></summary><p>先查看目前狀態與停止原因。若顯示頁面進入背景而停止新增操作，返回後依面板提示確認是否需要手動重新開始。</p></details>
        <details><summary><span>策略可以保證獲利嗎？</span><b>＋</b></summary><p>不可以。百家樂結果具有不確定性；分析方向、公式及配注策略都不保證可以預測下一局或獲利。</p></details>
      </div>
    </div>
  </section>

  <section class="auto-next" aria-labelledby="auto-next-title">
    <div class="wrap auto-next-layout">
      <div>
        {eyebrow('下一步／由你確認')}
        <h2 id="auto-next-title">設定完成，<br><em>再開始。</em></h2>
        <p>需要先讀教學，或已經知道要進入哪一套工具？</p>
      </div>
      <div class="auto-next-actions">
        {button('開啟 MT AUTO', AUTO, 'light')}
        {button('閱讀自動下注教學', '/guide?system=auto', 'outline-light')}
        <a class="text-link auto-next-link" href="/contact">需要協助？聯繫客服 {arrow()}</a>
      </div>
    </div>
  </section>

  <aside class="auto-disclaimer" aria-label="使用限制與素材聲明">
    <div class="wrap">
      <p><strong>使用提醒</strong> 本頁只作產品資訊與介面展示，不保證預測下一局或獲利；不建立送單或自動下注控制。請依所在地法規與個人風險承受度理性評估，未成年人請勿參與。</p>
      <p><strong>素材聲明</strong> 產品截圖為真實介面展示，真人素材來源為 Game+，非御策官方荷官名單；商業授權尚未核實，正式部署前需確認。</p>
    </div>
  </aside>
</div>
'''

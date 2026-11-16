from ..common import AUTO, DATA, LINE, MATRIX, arrow, button, dealer, eyebrow, image_note, logo, screen
def render():
    data_steps = DATA['auto_steps']
    prepare = data_steps[0]
    step_rows = []
    for index, (title, summary, detail, images) in enumerate(data_steps[1:], start=2):
        media = ''.join(screen(name, label, 'auto-screen') for name, label in images)
        if index == 6:
            media = f'<div class="media-stack">{media}</div>'
        row_class = 'feature-row reverse' if index % 2 == 0 else 'feature-row'
        step_rows.append(f'''
      <article class="{row_class}" id="auto-step{index}" aria-labelledby="auto-step{index}-title">
        <div class="feature-copy">
          {eyebrow(f'AUTO STEP {index:02d}')}
          <h2 id="auto-step{index}-title">{title}</h2>
          <p><strong>{summary}</strong></p>
          <p>{detail}</p>
          <a class="text-link" href="/guide?system=auto#auto-step{index}">查看第 {index} 步教學 {arrow()}</a>
        </div>
        <div class="feature-media">
          <div class="product-caption"><span>MT AUTO</span><span>點擊查看完整介面</span></div>{media}
          {image_note()}
        </div>
      </article>''')
    return f'''
<section class="page-hero" aria-labelledby="auto-title">
  <div class="wrap hero-layout">
    <div class="hero-copy">
      {eyebrow('MT AUTO／自動下注')}
      {logo(auto=True)}
      <h1 id="auto-title">先確認設定，<br><span>再開始執行。</span></h1>
      <p>從推薦與配注、投注金額、停止時間，到止損止盈、執行及紀錄，逐項核對後再進入 MT AUTO。</p>
      <div class="hero-actions">{button('開啟 MT AUTO', AUTO, 'primary')}{button('閱讀自動下注教學', '/guide?system=auto', 'outline')}</div>
      <p class="note">介面為展示截圖，非即時桌台；實際狀態以程式內顯示為準。</p>
    </div>
    <div class="hero-media">
      <div class="portrait-stage auto-portrait">
        {dealer('live2', label='Game+ MT 真人展示素材，非御策官方荷官名單', eager=True)}
        <div class="stage-screen"><div class="product-caption"><span>MT AUTO</span><span>執行面板</span></div>{screen('auto-running', 'MT AUTO 自動下注執行面板', 'hero-screen', eager=True)}</div>
      </div>
    </div>
  </div>
</section>
<nav class="section-nav" aria-label="自動下注步驟導覽">
  <div class="wrap">
    <a href="#auto-step1"><span>01</span>登入與準備</a>
    <a href="#auto-step2"><span>02</span>推薦與配注</a>
    <a href="#auto-step3"><span>03</span>投注金額</a>
    <a href="#auto-step4"><span>04</span>停止時間</a>
    <a href="#auto-step5"><span>05</span>止損止盈</a>
    <a href="#auto-step6"><span>06</span>執行與紀錄</a>
  </div>
</nav>
<section class="content-section" id="auto-workflow" aria-labelledby="workflow-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('六步設定流程')}
      <h2 id="workflow-title">每一項先核對，<br><span>再進入下一步。</span></h2>
      <p>以下內容依 MT AUTO 的操作教學整理。推薦來源、配注方式、金額與停止條件都以程式內提示為準。</p>
    </div>
    <div class="feature-grid" id="auto-step1">
      <article aria-labelledby="auto-step1-title">
        {eyebrow('AUTO STEP 01')}
        <h3 id="auto-step1-title">{prepare[0]}</h3>
        <p><strong>{prepare[1]}</strong></p>
        <p>{prepare[2]}</p>
        <a class="text-link" href="/guide?system=auto#auto-step1">查看第 1 步教學 {arrow()}</a>
      </article>
      <article>
        <h3>開始前的基本核對</h3>
        <ul>
          <li>確認使用的平台、桌台、帳號授權與連線狀態。</li>
          <li>確認配注、基本單注、單筆上限與停止條件。</li>
          <li>需要停止時，使用程式內的停止按鈕並閱讀狀態原因。</li>
        </ul>
      </article>
    </div>
    <div class="facts" aria-label="MT AUTO 設定重點">
      <div><strong>策略</strong><span>推薦來源與配注方式</span></div>
      <div><strong>條件</strong><span>金額、時間、止損與止盈</span></div>
      <div><strong>回看</strong><span>執行狀態與歷史紀錄</span></div>
    </div>
    {''.join(step_rows)}
  </div>
</section>
<section class="surface-section" aria-labelledby="scene-title">
  <div class="wrap feature-row">
    <div class="feature-copy">
      {eyebrow('操作情境／非即時畫面')}
      <h2 id="scene-title">把條件寫清楚，<br><span>再由你確認開始。</span></h2>
      <p>開始前確認止損與止盈，實際限制、執行狀態與接受金額，請以正式程式面板為準。</p>
      <p class="note">圖片僅供介面說明，不能保證執行結果或獲利。</p>
    </div>
    <div class="feature-media">
      {screen('auto-limits', 'MT AUTO 開始前核對停止條件')}
    </div>
  </div>
</section>
<section class="content-section" id="auto-difference" aria-labelledby="difference-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('兩套工具／入口分開')}
      <h2 id="difference-title">MT AUTO 不等於 MATRIX，<br><span>請依用途選入口。</span></h2>
      <p>兩套產品各自處理不同工作，不混用功能或畫面。</p>
    </div>
    <div class="feature-grid">
      <article>
        {logo(auto=True)}<h3>MT AUTO／自動下注</h3>
        <p>管理推薦與配注、投注金額、停止時間、止損止盈，以及執行狀態與紀錄。</p>
        <a class="text-link" href="{AUTO}">進入 MT AUTO {arrow()}</a>
      </article>
      <article>
        {logo()}<h3>MT MATRIX／多桌輔助</h3>
        <p>整理多桌雷達、牌路、AI 綜合分析、四式算牌與終值奇偶，不是本頁的自動下注入口。</p>
        <a class="text-link" href="{MATRIX}">進入 MT MATRIX {arrow()}</a>
      </article>
    </div>
  </div>
</section>
<section class="surface-section" id="auto-compatibility" aria-labelledby="compatibility-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('相容性與風險')}
      <h2 id="compatibility-title">先了解使用邊界，<br><span>再決定是否進入。</span></h2>
      <p>可用電腦、Android 手機與 iPhone 的瀏覽器開啟，不必另行安裝；實際平台、登入授權與遊戲操作方式，以登入後的程式介面為準。</p>
    </div>
    <div class="facts">
      <div><strong>裝置</strong><span>電腦、Android、iPhone</span></div>
      <div><strong>狀態</strong><span>以程式內連線與目前狀態為準</span></div>
      <div><strong>風險</strong><span>配注策略不保證下一局或獲利</span></div>
    </div>
    <div class="feature-grid">
      <article><h3>畫面顯示停止時</h3><p>先查看目前狀態與停止原因；返回頁面後依面板提示確認是否需要手動重新開始。</p></article>
      <article><h3>畫面與結果</h3><p>本頁介面截圖不是即時資料或實際送單畫面；百家樂結果具有不確定性，請依所在地法規與個人風險承受度評估。</p></article>
    </div>
    <p class="note">不要把歷史畫面、分析方向或配注策略理解為結果保證；未成年人請勿參與。</p>
  </div>
</section>
<section class="cta-section" aria-labelledby="auto-cta-title">
  <div class="wrap cta-layout">
    <div>
      {eyebrow('下一步／由你確認')}
      <h2 id="auto-cta-title">設定完成，<br><span>再選正確入口。</span></h2>
      <p>需要先讀教學，或已經知道要使用 MT AUTO？</p>
    </div>
    <div class="hero-actions">
      {button('開啟 MT AUTO', AUTO, 'light')}{button('閱讀自動下注教學', '/guide?system=auto', 'outline-light')}
      <a class="text-link" href="{LINE}">需要協助？聯繫 LINE 客服 {arrow()}</a>
    </div>
  </div>
</section>
'''

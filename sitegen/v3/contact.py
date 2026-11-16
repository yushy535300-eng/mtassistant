from ..common import DATA, MATRIX, AUTO, LINE, logo, screen, button, eyebrow, dealer, arrow, image_note


def render():
    """Return the new contact page main content without the document shell."""
    return f'''
<section class="page-hero contact-hero" aria-labelledby="contact-title">
    <div class="wrap hero-layout">
      <div class="hero-copy">
        {eyebrow('客服中心 / 直接聯繫')}
        <h1 id="contact-title">需要協助？<br><span>我們幫你確認。</span></h1>
        <p>帳號授權、功能操作或連線問題，都可以從 LINE 客服開始。提供使用系統、裝置與錯誤畫面，方便客服從正確步驟協助確認。</p>
        <div class="hero-actions">
          {button('直接開啟 LINE 客服', LINE, 'light')}
          {button('準備聯繫資料', '#contact-checklist', 'outline-light')}
        </div>
        <p class="note">請只提供必要的帳號與錯誤畫面；勿提供密碼或驗證碼。</p>
      </div>
      <div class="hero-media" aria-label="LINE 客服 QR 入口">
        <a class="contact-qr" href="{LINE}">
        <div class="product-caption"><span>LINE 客服入口</span><span>掃描或直接點擊</span></div>
        <img src="/assets/contact-line-qr.png" width="370" height="370" alt="掃描 QR 開啟御策指定 LINE 客服，手機可直接點擊" loading="eager" decoding="async">
        <span class="contact-qr__copy"><strong>桌機掃描，手機直接開啟 LINE</strong><small>使用共用客服連結前往</small></span>
      </a>
    </div>
  </div>
</section>

<nav class="section-nav" aria-label="客服中心內容導覽">
  <div class="wrap"><a href="#contact-checklist">聯繫前清單</a><a href="#contact-systems">選擇系統</a><a href="#contact-community">社群與風險</a></div>
</nav>

<section class="content-section" id="contact-checklist" aria-labelledby="checklist-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('01 / 聯繫前準備')}
      <h2 id="checklist-title">一段清楚的訊息，<br><span>就能從正確位置開始。</span></h2>
      <p>不用整理成長篇報告，請依序提供下面四項資料，讓客服了解你正在使用的系統與實際狀況。</p>
    </div>
    <ol class="contact-checklist">
      <li><strong>會員帳號</strong><span>提供需要查詢的會員帳號；不提供密碼。</span></li>
      <li><strong>使用系統</strong><span>說明目前使用 MT MATRIX 多桌百家輔助，或 MT AUTO 百家自動下注。</span></li>
      <li><strong>裝置、瀏覽器與時間</strong><span>例如電腦或手機、瀏覽器名稱，以及問題發生的時間。</span></li>
      <li><strong>錯誤步驟與截圖</strong><span>附上錯誤畫面截圖，並說明從哪一步開始出現問題。</span></li>
    </ol>
    <p class="note"><strong>安全提醒：</strong>客服不需要密碼、驗證碼或其他私密資料。請先遮蔽截圖中不必要的個人資訊。</p>
  </div>
</section>

<section class="surface-section" id="contact-systems" aria-labelledby="systems-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('02 / 選擇正確入口')}
      <h2 id="systems-title">兩套工具各自獨立，<br><span>教學與入口分開走。</span></h2>
      <p>先確認問題對應的產品，再閱讀該產品教學；客服訊息也請標註使用中的系統。</p>
    </div>
    <div class="contact-links">
      <article class="contact-link">
        <div class="contact-link__identity">{logo()}<div><span>MT MATRIX</span><h3>多桌百家輔助</h3></div></div>
        <p>整理多桌、牌路與分析資訊；雷達、AI 綜合分析、四式算牌與終值奇偶問題，先查看這套教學。</p>
        <div class="hero-actions"><a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>{button('進入多桌輔助', MATRIX, 'outline-light')}</div>
      </article>
      <article class="contact-link">
        <div class="contact-link__identity">{logo(True)}<div><span>MT AUTO</span><h3>百家自動下注</h3></div></div>
        <p>處理配注方式、投注金額、停止時間、止損止盈與執行紀錄；開始前先閱讀設定說明。</p>
        <div class="hero-actions"><a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>{button('進入自動下注', AUTO, 'outline-light')}</div>
      </article>
    </div>
  </div>
</section>

<section class="content-section" id="contact-community" aria-labelledby="community-title">
  <div class="wrap">
    <div class="section-intro">
      {eyebrow('03 / 其他聯繫方式')}
      <h2 id="community-title">需要協助時，<br><span>使用可核對的入口。</span></h2>
    </div>
    <div class="contact-links">
      <article class="contact-link">
        <h3>LINE 官方客服</h3>
        <p>帳號、系統、裝置、時間與錯誤截圖，請集中在同一段訊息中。</p>
        {button('開啟 LINE 客服', LINE, 'light')}
      </article>
      <article class="contact-link">
        <h3>Threads · @uss0857</h3>
        <p>查看公開動態；需要處理帳號或操作問題，仍請回到 LINE 提供完整資料。</p>
        <a class="text-link" href="https://www.threads.net/@uss0857">查看 Threads 公開動態 {arrow()}</a>
      </article>
    </div>
    <p class="note"><strong>風險說明：</strong>本頁連結導向各自的原始系統入口；展示與客服說明不代表即時桌台、實際送單結果或獲利保證。分析、公式與配注策略不能保證預測下一局。請閱讀教學，依所在地法規評估風險。</p>
  </div>
</section>
'''

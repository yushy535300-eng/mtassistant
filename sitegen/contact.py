from .common import AUTO, LINE, MATRIX, ambient, arrow, button, chapter, eyebrow, logo


def render():
    """Return the contact page's main content without the document shell."""
    return f'''<div class="contact-page">
  <section class="contact-page__hero section">
    {ambient('contact')}
    <div class="wrap contact-page__hero-grid">
      <div class="contact-page__hero-copy">
        {eyebrow('客服中心 / 直接聯繫')}
        <h1>需要協助？<br><span>我們幫你釐清。</span></h1>
        <p class="contact-page__hero-lede">帳號授權、功能使用或連線問題，都可從 LINE 客服開始。提供使用系統、裝置與問題截圖，我們協助你確認下一步。</p>
        <div class="contact-page__hero-actions">
          {button('開啟 LINE 客服', LINE, 'light')}
          {button('查看使用系統', '#contact-page-systems', 'outline-light')}
        </div>
        <p class="contact-page__hero-note">文字聯繫，不設表單；請只提供必要的帳號與畫面資訊。</p>
      </div>
      <div class="contact-page__hero-mark" aria-label="LINE 客服服務入口">
        <div class="contact-page__mark-heading">
          <span>LINE 客服入口</span>
          <span>掃描或直接點擊</span>
        </div>
        <a class="contact-qr" href="{LINE}">
          <img src="/assets/contact-line-qr.png" width="370" height="370" alt="掃描 QR 開啟御策指定 LINE 客服，或直接點擊前往">
          <span class="contact-qr__copy"><strong>把問題，交給對的人。</strong><small>桌機掃描／手機直接點擊</small></span>
        </a>
      </div>
    </div>
  </section>

  <section class="contact-page__service section" id="contact-page-support">
    <div class="wrap">
      <div class="contact-page__service-heading">
        <div>
          {eyebrow('01 / 直接聯繫')}
          <h2>御策百家客服中心</h2>
        </div>
        <p>沒有複雜流程，也不需要填寫表單。開啟 LINE 後，依照下方清單描述目前狀況即可。</p>
      </div>
      <div class="contact-page__service-line">
        <div class="contact-page__service-label">
          <span class="contact-page__service-dot" aria-hidden="true"></span>
          <span>LINE 客服</span>
        </div>
        <div class="contact-page__service-main">
          <h3>從一段清楚的訊息開始。</h3>
          <p>請留下會員帳號、問題描述與錯誤截圖，方便客服確認。<strong>請勿提供密碼。</strong></p>
        </div>
        <div class="contact-page__service-action">
          {button('開啟 LINE 客服', LINE, 'primary')}
          <span>透過共用客服連結前往</span>
        </div>
      </div>
      <div class="contact-page__service-note">
        <span>安全提醒</span>
        <p>客服確認問題只需要必要的帳號與畫面資訊；密碼、驗證碼及其他私密資料都不需要提供。</p>
      </div>
    </div>
  </section>

  <section class="contact-page__brief section">
    <div class="wrap">
      {chapter('02 / 聯繫前準備', '把資訊放在同一條訊息裡。', '描述越接近實際畫面，越容易從正確的系統、裝置與步驟開始確認。')}
      <div class="contact-page__brief-grid">
        <div class="contact-page__brief-intro">
          <span class="contact-page__brief-kicker">聯繫前清單</span>
          <p>不必整理成長篇報告，依序提供這幾項就夠了。</p>
          <span class="contact-page__brief-rule" aria-hidden="true"></span>
        </div>
        <ol class="contact-page__checklist">
          <li><b>01</b><span><strong>會員帳號</strong>提供需要查詢的會員帳號；不提供密碼。</span></li>
          <li><b>02</b><span><strong>使用系統</strong>說明目前使用多桌百家或自動下注。</span></li>
          <li><b>03</b><span><strong>裝置、瀏覽器與時間</strong>例如電腦或手機、瀏覽器名稱，以及問題發生時間。</span></li>
          <li><b>04</b><span><strong>錯誤畫面與步驟</strong>附上錯誤截圖，並說明從哪一步開始出現問題。</span></li>
        </ol>
      </div>
    </div>
  </section>

  <section class="contact-page__systems section" id="contact-page-systems">
    <div class="wrap">
      <div class="contact-page__systems-heading">
        {eyebrow('03 / 選擇正確入口')}
        <h2>先選對工具。<br>再取得協助。</h2>
        <p>客服訊息中註明對應系統，能更快對焦到正確的操作流程。兩套工具各自獨立，請從原始入口前往。</p>
      </div>
      <div class="contact-page__system-list">
        <article class="contact-page__system contact-page__system--matrix">
          <div class="contact-page__system-identity">{logo()}<div><span>MT MATRIX</span><h3>多桌百家輔助</h3></div></div>
          <p>整理多桌、牌路與分析資訊；若問題涉及雷達、模型或多桌畫面，先查看這套系統的操作說明。</p>
          <div class="contact-page__system-links">
            <a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>
            {button('進入多桌輔助', MATRIX, 'outline-light')}
          </div>
        </article>
        <article class="contact-page__system contact-page__system--auto">
          <div class="contact-page__system-identity">{logo(True)}<div><span>MT AUTO</span><h3>百家自動下注</h3></div></div>
          <p>處理配注方式、金額、停止條件與執行紀錄；開始前請先閱讀設定與風險說明。</p>
          <div class="contact-page__system-links">
            <a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>
            {button('進入自動下注', AUTO, 'outline-light')}
          </div>
        </article>
      </div>
      <div class="contact-page__systems-disclosure">
        <span>來源與風險</span>
        <p>本頁連結導向各自的原始系統入口；頁面展示與客服說明不代表即時桌台、送單結果或獲利保證。操作前請閱讀教學與程式內提示，並依所在地法規評估風險。</p>
      </div>
      <a class="contact-page__social" href="https://www.threads.net/@uss0857">
        <span class="contact-page__social-index">社群聯繫</span>
        <span class="contact-page__social-name">Threads · @uss0857</span>
        <span class="contact-page__social-action">查看公開動態 {arrow()}</span>
      </a>
    </div>
  </section>
</div>'''

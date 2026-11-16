from .v2 import support
from ..common import AUTO, LINE, MATRIX, THREADS, arrow, button, logo


def render():
    """Return the compact customer-support page content without the site shell."""
    return f'''
<section class="portal-pagehead" aria-labelledby="contact-page-title">
  <div>
    <p class="kicker">客服中心</p>
    <h1 id="contact-page-title">需要協助，直接找我們</h1>
    <p>帳號授權、連線、畫面操作或設定問題，都可以透過官方客服聯繫。我們會依你提供的狀況協助確認下一步。</p>
  </div>
  <div class="pagehead-actions">
    {button("開啟 LINE 客服", LINE)}
  </div>
</section>

<section class="portal-section" aria-labelledby="contact-direct-title">
  <div class="section-top">
    <div>
      <h2 id="contact-direct-title">直接聯絡</h2>
      <p>選擇方便的方式聯繫；桌機可掃描 QR，手機可直接點擊 LINE。</p>
    </div>
  </div>
  <div class="two-column">
    <article class="portal-panel">
      <div class="product-heading">
        <div>
          <h3>LINE 官方客服</h3>
          <p>處理登入、授權、連線與功能使用問題。</p>
        </div>
      </div>
      <div class="feature-list">
        <div>
          <h3>客服連結</h3>
          <p><a class="text-link" href="{LINE}">開啟官方 LINE {arrow()}</a></p>
        </div>
        <div>
          <h3>公開社群</h3>
          <p><a class="text-link" href="{THREADS}">Threads · @hacklook__ {arrow()}</a></p>
        </div>
      </div>
      <div class="inline-actions">
        {button("直接開啟 LINE", LINE, "outline")}
      </div>
    </article>

    <article class="portal-panel">
      <details class="refine-qr qr-disclosure" data-phone-collapse open><summary>另一台裝置：展開 LINE QR</summary>
      <div class="section-top">
        <div>
          <h3>掃描 LINE QR</h3>
          <p>桌機或另一台裝置可掃碼；正在用手機請直接點擊 LINE。</p>
        </div>
      </div>
      <a class="media-display" href="{LINE}" aria-label="掃描 QR 開啟御策官方 LINE 客服">
        <img src="/assets/contact-line-qr.png" width="370" height="370" alt="御策官方 LINE 客服 QR Code" loading="eager" decoding="async">
      </a>
      <p class="portal-notice">客服只需要必要的帳號與畫面資訊；請勿提供密碼、驗證碼或其他私密資料。</p>
      </details>
    </article>
  </div>
</section>

{support()}

<section class="portal-section" aria-labelledby="contact-checklist-title">
  <div class="section-top">
    <div>
      <h2 id="contact-checklist-title">聯繫前準備這些資料</h2>
      <p>不用整理長篇說明，依照目前狀況提供以下資訊即可，我們會陪你逐項確認。</p>
    </div>
  </div>
  <div class="portal-panel">
    <div class="feature-list">
      <div>
        <h3>會員帳號</h3>
        <p>提供需要查詢的會員帳號，方便客服找到正確資料。</p>
      </div>
      <div>
        <h3>使用系統</h3>
        <p>說明目前使用 MT MATRIX 多桌輔助，或 MT AUTO 自動下注。</p>
      </div>
      <div>
        <h3>裝置與瀏覽器</h3>
        <p>告知使用電腦或手機、瀏覽器名稱，以及問題發生的大約時間。</p>
      </div>
      <div>
        <h3>畫面與操作步驟</h3>
        <p>附上錯誤畫面或截圖，並描述從哪一步開始出現問題。</p>
      </div>
    </div>
    <p class="portal-notice"><strong>安全提醒：</strong>客服不會要求密碼或驗證碼。若畫面要求重新登入，請回到原系統入口操作，不要把私密資料貼在訊息中。</p>
  </div>
</section>

<section class="portal-section" aria-labelledby="contact-tools-title">
  <div class="section-top">
    <div>
      <h2 id="contact-tools-title">先看對應教學，再進入工具</h2>
      <p>客服訊息中註明使用哪套系統，能更快對焦到正確操作。兩套工具各自獨立，請從原始入口前往。</p>
    </div>
  </div>
  <div class="two-column">
    <article class="portal-panel">
      <div class="product-heading">
        {logo()}
        <div>
          <h3>MT MATRIX</h3>
          <p>多桌百家輔助</p>
        </div>
      </div>
      <p>查看多桌雷達、平台連線、AI 綜合、V38 四式與終值奇偶等資訊。</p>
      <div class="inline-actions">
        <a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>
        {button("進入多桌輔助", MATRIX, "outline")}
      </div>
    </article>
    <article class="portal-panel">
      <div class="product-heading">
        {logo(True)}
        <div>
          <h3>MT AUTO</h3>
          <p>百家自動下注</p>
        </div>
      </div>
      <p>查看推薦與配注、基本單注、單筆上限、停止時間、止損止盈與執行紀錄。</p>
      <div class="inline-actions">
        <a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>
        {button("進入自動下注", AUTO, "outline")}
      </div>
    </article>
  </div>
  <div class="action-strip">
    <p class="portal-notice">兩套工具的分析、公式與配注策略都不保證預測下一局或獲利；實際畫面與限制以登入後程式內提示為準，請依所在地法規評估風險。</p>
    <a class="text-link" href="/faq">先查看常見問題 {arrow()}</a>
  </div>
</section>
'''

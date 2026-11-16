from .common import arrow, button, dealer, eyebrow, image_note, logo, screen, SCENE


def render():
    return f'''
<section class="home-hero" aria-labelledby="home-title">
  <div class="wrap home-hero-layout">
    <div class="home-copy">
      {eyebrow('御策百家輔助')}
      <p class="hero-kicker">MT MATRIX × MT AUTO</p>
      <h1 id="home-title">多桌輔助。<br><span>自動下注。</span></h1>
      <p class="hero-description">看牌路、查分析，或設定配注與停止條件。<br>依你的用途，選擇對應工具。</p>
      <div class="hero-actions">
        {button('了解多桌輔助', '/features', 'light')}
        {button('了解自動下注', '/auto', 'outline-light')}
      </div>
      <p class="hero-devices">電腦、手機與平板，透過瀏覽器使用。</p>
    </div>
    <div class="home-visual" aria-label="真人情境與 MT MATRIX 真實介面展示">
      <div class="hero-dealer">{dealer('live1', '既有 Game+ 公開 MT 人物素材；非御策官方荷官名單', eager=True)}</div>
      <div class="hero-product">
        <div class="product-caption"><span>MT MATRIX</span><span>介面預覽</span></div>
        {screen('matrix-assist', 'MT MATRIX 多桌百家輔助真實主面板', cls='hero-screen', eager=True)}
      </div>
    </div>
  </div>
  <div class="wrap hero-baseline"><p>分析與策略僅供輔助，不保證結果。</p><a href="#brand-story">選擇你的工具 {arrow()}</a></div>
</section>

<section class="brand-story section" id="brand-story" aria-labelledby="choose-title">
  <div class="wrap">
    <div class="tools-intro">{eyebrow('認識兩套工具')}<h2 id="choose-title">用途不同，<span>入口分開。</span></h2><p>MT MATRIX 專注牌路與分析；MT AUTO 專注設定與執行。兩套系統各有對應教學。</p></div>
    <div class="tool-choices">
      <article class="tool-choice">
        <div class="tool-choice-heading">{logo()}<div><p>MT MATRIX</p><h3>多桌百家輔助</h3></div></div>
        <p>從多桌雷達選擇桌台，集中查看牌路、AI 綜合分析、四式算牌與終值奇偶。</p>
        <div class="tool-choice-links"><a href="/features">查看功能 {arrow()}</a><a href="/guide?system=matrix">操作教學</a></div>
      </article>
      <article class="tool-choice">
        <div class="tool-choice-heading">{logo(True)}<div><p>MT AUTO</p><h3>百家自動下注</h3></div></div>
        <p>確認配注、基本單注、停止時間與條件，再透過執行面板查看狀態與紀錄。</p>
        <div class="tool-choice-links"><a href="/auto">查看功能 {arrow()}</a><a href="/guide?system=auto">操作教學</a></div>
      </article>
    </div>
  </div>
</section>

<section class="matrix-launch section" id="products">
  <div class="wrap">
    <div class="launch-top">
      <div>{eyebrow('MT MATRIX 多桌輔助')}<h2>一個畫面，<br><span class="muted">查看多桌資訊。</span></h2></div>
      <div><p>先透過雷達找到桌台，<br>再查看對應牌路、分析與計算內容。</p>{button('查看完整功能', '/features', 'outline-light')}</div>
    </div>
    <div class="radar-showcase">
      <div class="product-caption"><span>多桌雷達</span><span>左右滑動查看 →</span></div>
      <div class="radar-scroll" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">{screen('multitable-radar', 'MT MATRIX 多桌雷達完整桌台資訊')}</div>
    </div>
    <div class="launch-details">
      <div><span>01</span><h3>多桌雷達</h3><p>並列桌台與分析資訊。</p></div>
      <div><span>02</span><h3>AI 綜合分析</h3><p>集中檢視不同模型與牌路。</p></div>
      <div><span>03</span><h3>四式算牌・終值奇偶</h3><p>查看牌值與計算過程。</p></div>
    </div>
    {image_note()}
  </div>
</section>

<section class="auto-launch section">
  <div class="wrap auto-launch-layout">
    <div class="auto-launch-copy">
      {eyebrow('MT AUTO 自動下注')}
      <h2>先確認設定，<br><span class="muted">再開始執行。</span></h2>
      <p>從配注與注額，到停止時間與條件。<br>開始之前，逐項確認你的設定。</p>
      <div class="auto-launch-facts"><span>策略與配注</span><span>止損與止盈</span><span>狀態與紀錄</span></div>
      <div class="hero-actions">{button('查看自動下注', '/auto')}{button('閱讀操作教學', '/guide?system=auto', 'text')}</div>
      <p class="small-note">MT AUTO 為獨立產品，與多桌輔助介面分開。</p>
    </div>
    <div class="auto-launch-visual">
      <div class="auto-frame"><div class="product-caption"><span>MT AUTO</span><span>執行面板</span></div>{screen('auto-running', 'MT AUTO 自動下注執行面板')}</div>
      <p class="image-note">真實介面截圖，非即時送單畫面。</p>
    </div>
  </div>
</section>

<section class="cinema-section">
  <img class="cinema-background" src="{SCENE}" alt="原創非人物百家樂牌桌與撲克牌情境" width="1536" height="864" loading="lazy">
  <div class="cinema-shade"></div>
  <div class="wrap cinema-copy">{eyebrow('理性使用，了解風險')}<h2>你的判斷，<br>始終在你手中。</h2><p>牌路與模型是輔助資訊，不是結果保證。<br>了解工具用途，再依自己的判斷操作。</p><p class="asset-caption">牌桌情境為原創視覺，非即時遊戲畫面。</p></div>
</section>

<section class="home-focus section">
  <div class="wrap focus-layout">
    <div>{eyebrow('真實功能展示')}<h2>看清面板，<br><span class="muted">也了解計算。</span></h2><p>切換畫面，查看牌面、牌值與公式。<br>點擊圖片即可放大原始介面。</p>
      <div class="focus-tabs" role="tablist" aria-label="MT MATRIX 功能畫面">
        <button type="button" role="tab" id="focus-tab-cards" aria-controls="focus-cards" aria-selected="true" data-tab="cards"><span>01</span> V38 四式算牌 {arrow()}</button>
        <button type="button" role="tab" id="focus-tab-parity" aria-controls="focus-parity" aria-selected="false" tabindex="-1" data-tab="parity"><span>02</span> 終值奇偶模型 {arrow()}</button>
        <button type="button" role="tab" id="focus-tab-assist" aria-controls="focus-assist" aria-selected="false" tabindex="-1" data-tab="assist"><span>03</span> AI 綜合分析 {arrow()}</button>
      </div>
    </div>
    <div class="focus-stage">
      <div class="product-caption"><span>MT MATRIX</span><span>點圖查看完整介面 ＋</span></div>
      <div role="tabpanel" id="focus-cards" aria-labelledby="focus-tab-cards">{screen('four-formulas', 'MT MATRIX V38 四式算牌完整面板')}</div>
      <div role="tabpanel" id="focus-parity" aria-labelledby="focus-tab-parity" hidden>{screen('parity-model', 'MT MATRIX 終值奇偶模型完整面板')}</div>
      <div role="tabpanel" id="focus-assist" aria-labelledby="focus-tab-assist" hidden>{screen('matrix-assist', 'MT MATRIX AI 綜合分析主面板')}</div>
      {image_note()}
    </div>
  </div>
</section>

<section class="home-guides section">
  <div class="wrap">
    <div class="guides-intro">{eyebrow('操作教學')}<h2>選對系統，<span class="muted">照步驟操作。</span></h2><p>兩套工具的操作流程與畫面分開，請閱讀對應教學。</p></div>
    <div class="guide-paths">
      <a href="/guide?system=matrix"><span class="path-number">01</span><div><span class="eyebrow">MT MATRIX · 五個步驟</span><h3>多桌輔助操作教學</h3><p>登入與連線 → 雷達 → AI 分析 → 算牌與奇偶</p></div>{arrow()}</a>
      <a href="/guide?system=auto"><span class="path-number">02</span><div><span class="eyebrow">MT AUTO · 六個步驟</span><h3>自動下注操作教學</h3><p>配注 → 注額 → 停止時間與條件 → 執行紀錄</p></div>{arrow()}</a>
    </div>
  </div>
</section>

<section class="home-knowledge section">
  <div class="wrap knowledge-layout">
    <div>{eyebrow('常見問題與支援')}<h2>有疑問，<br><span class="muted">先找到答案。</span></h2><p>了解裝置、授權與工具風險。<br>需要操作協助，也可以聯繫客服。</p><a class="text-link" href="/faq">查看常見問題 {arrow()}</a></div>
    <div class="knowledge-list">
      <a href="/faq#faqSearch"><span>01</span><h3>多桌輔助與自動下注，有什麼不同？</h3>{arrow()}</a>
      <a href="/faq#faqSearch"><span>02</span><h3>電腦與手機，可以直接使用嗎？</h3>{arrow()}</a>
      <a href="/faq#faqSearch"><span>03</span><h3>分析或策略，可以保證獲利嗎？</h3>{arrow()}</a>
      <p class="risk-inline">不可以。歷史牌路、模型與配注策略都不能保證下一局或獲利。</p>
    </div>
  </div>
</section>
'''

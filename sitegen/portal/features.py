from html import escape

from ..common import (
    DATA,
    LINE,
    MATRIX,
    arrow,
    button,
    image_note,
    logo,
    screen,
)
import importlib


def _link(label, url):
    """Render a compact text action using the portal contract's link treatment."""
    return (
        f'<a class="text-link" href="{escape(url, quote=True)}">'
        f'{escape(label)} {arrow()}</a>'
    )


def _matrix_steps():
    """Keep the five source teaching steps visible without duplicating their data."""
    items = []
    for number, step in enumerate(DATA["matrix_steps"], 1):
        short, title, description, _shots = step
        items.append(
            f'<li><strong>{number:02d}／{escape(short)}</strong>'
            f'<span>{escape(title)}</span>'
            f'<small>{escape(description)}</small></li>'
        )
    return "".join(items)


def render():
    """Return the MT MATRIX page body; the parent builder supplies site chrome."""
    return f'''
<div class="portal-page">
  <section class="portal-pagehead" aria-labelledby="matrix-page-title">
    <div>
      <p class="kicker">MT MATRIX／多桌輔助</p>
      <h1 id="matrix-page-title">MT MATRIX 多桌輔助</h1>
      <p>整理多桌雷達、平台連線、AI 綜合、V38 四式與終值奇偶；以下以原始介面截圖說明功能位置。</p>
    </div>
    <div class="pagehead-actions">
      {button("進入 MATRIX", MATRIX)}
      {button("閱讀操作教學", "/guide?system=matrix", "outline")}
      {_link("觀看完整操作影片", "/#mt-videos")}
    </div>
  </section>


  <section class="portal-section" aria-labelledby="matrix-map-title">
    <div class="section-top">
      <div>
        <h2 id="matrix-map-title">先看功能位置，再進入畫面</h2>
        <p>MT MATRIX 將桌台、牌路、模型與算牌入口集中在同一套多桌工作流程。</p>
      </div>
    </div>
    <div class="portal-panel">
      <div class="product-heading">
        {logo()}
        <div><strong>MT MATRIX</strong><span>多桌資訊整理與分析入口</span></div>
      </div>
      <nav class="inline-actions" aria-label="MATRIX 功能導覽">
        <a class="text-link" href="#matrix-radar">01 多桌雷達與連線 {arrow()}</a>
        <a class="text-link" href="#matrix-analysis">02 AI 綜合分析 {arrow()}</a>
        <a class="text-link" href="#matrix-formulas">03 V38 四式與終值奇偶 {arrow()}</a>
        <a class="text-link" href="#matrix-device">04 裝置與教學 {arrow()}</a>
      </nav>
      <p class="portal-notice">本頁圖片是既有產品介面展示，不是即時桌台或實際送單畫面；欄位與狀態以登入後的程式介面為準。</p>
    </div>
  </section>

  <section class="portal-section" id="matrix-radar" aria-labelledby="matrix-radar-title"><span id="radar" class="legacy-anchor"></span>
    <div class="section-top">
      <div>
        <h2 id="matrix-radar-title">多桌雷達與平台連線</h2>
        <p>先確認平台與連線狀態，再從雷達選擇要觀察的桌台。雷達原圖較寬，請在下方區域左右滑動。</p>
      </div>
    </div>
    <div class="portal-panel">
      <div class="radar-scroll" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">
        <div class="media-display">
          {screen("multitable-radar", "多桌雷達完整介面")}
        </div>
      </div>
      {image_note()}
    </div>
    <div class="two-column">
      <article class="portal-panel">
        <h3>平台連線</h3>
        <p>登入並完成授權後，查看目前選擇的平台與連線狀態，再由對應入口進入。</p>
        <ul class="feature-list">
          <li><strong>選擇平台</strong><span>核對正在使用的平台名稱。</span></li>
          <li><strong>查看連線</strong><span>以程式內顯示的連線與授權狀態為準。</span></li>
          <li><strong>切換觀察</strong><span>連線完成後再查看多桌雷達資料。</span></li>
        </ul>
      </article>
      <article class="portal-panel">
        <h3>連線狀態畫面</h3>
        <div class="media-display">
          {screen("platform-connection", "百家輔助平台連線與切換")}
        </div>
        {image_note()}
      </article>
    </div>
  </section>


  <section class="portal-section" id="matrix-analysis" aria-labelledby="matrix-analysis-title"><span id="analysis" class="legacy-anchor"></span>
    <div class="section-top">
      <div>
        <h2 id="matrix-analysis-title">AI 綜合分析與主面板</h2>
        <p>開啟模型選單確認分析來源，再回到主面板查看當局牌型、推薦資訊與 AI 分析內容。</p>
      </div>
    </div>
    <div class="two-column">
      <article class="portal-panel">
        <h3>模型選單</h3>
        <ul class="feature-list">
          <li><strong>切換分析來源</strong><span>依需要選擇分析來源或牌路策略。</span></li>
          <li><strong>回看主面板</strong><span>確認目前模型與主面板欄位是否一致。</span></li>
          <li><strong>自行評估</strong><span>AI 方向僅供資訊整理，不保證下一局結果。</span></li>
        </ul>
        <div class="media-display">
          {screen("analysis-models", "AI 綜合模型選單")}
        </div>
        {image_note()}
      </article>
      <article class="portal-panel">
        <h3>百家輔助主面板</h3>
        <p>主面板集中顯示桌台、牌路、推薦資訊與分析內容；實際顯示欄位以登入後程式為準。</p>
        <div class="media-display">
          {screen("matrix-assist", "百家輔助主面板與 AI 分析")}
        </div>
        {image_note()}
      </article>
    </div>
  </section>

  <section class="portal-section" id="matrix-formulas" aria-labelledby="matrix-formulas-title"><span id="formulas" class="legacy-anchor"></span>
    <div class="section-top">
      <div>
        <h2 id="matrix-formulas-title">V38 四式與終值奇偶</h2>
        <p>兩個模型分開核對：先看牌面與公式欄位，再查看牌值、計算過程、終值與顯示方向。</p>
      </div>
    </div>
    <div class="two-column">
      <article class="portal-panel">
        <h3>V38 四式算牌</h3>
        <div class="media-display">
          {screen("four-formulas", "V38 四式算牌完整面板")}
        </div>
        {image_note()}
        <ul class="feature-list">
          <li><strong>牌面與點數</strong><span>核對 Shoe、Round、閒莊牌面與點數。</span></li>
          <li><strong>四式結果</strong><span>查看 A 公式、B 公式、MUL 與 ADD 的顯示。</span></li>
          <li><strong>下一局投票</strong><span>查看面板提供的方向欄位，不視為結果保證。</span></li>
        </ul>
      </article>
      <article class="portal-panel">
        <h3 id="parity">終值奇偶模型</h3>
        <div class="media-display">
          {screen("parity-model", "終值奇偶模型完整面板")}
        </div>
        {image_note()}
        <ul class="feature-list">
          <li><strong>牌面與牌值</strong><span>依序查看模型使用的牌面及牌值。</span></li>
          <li><strong>計算過程與終值</strong><span>回看中間計算、終值與顯示方向。</span></li>
          <li><strong>使用限制</strong><span>模型資訊不保證下一局結果，也不代表獲利。</span></li>
        </ul>
      </article>
    </div>
  </section>

  <section class="portal-section" id="matrix-device" aria-labelledby="matrix-device-title">
    <div class="section-top">
      <div>
        <h2 id="matrix-device-title">裝置相容性與五步教學</h2>
        <p>以瀏覽器開啟系統，不需要另行下載安裝檔；登入、平台與操作狀態以正式程式介面為準。</p>
      </div>
    </div>
    <div class="two-column">
      <article class="portal-panel">
        <h3>使用方式</h3>
        <ul class="feature-list">
          <li><strong>電腦</strong><span>可用瀏覽器查看完整桌台、分析與算牌畫面。</span></li>
          <li><strong>Android 手機</strong><span>直接由瀏覽器開啟 MT MATRIX。</span></li>
          <li><strong>iPhone</strong><span>直接由瀏覽器開啟 MT MATRIX。</span></li>
          <li><strong>開始前</strong><span>先確認帳號授權、使用平台、桌台與連線狀態。</span></li>
        </ul>
        <p class="portal-notice">使用前確認帳號授權與連線狀態，實際功能以登入後顯示為準。</p>
      </article>
      <article class="portal-panel">
        <h3>多桌輔助五步操作</h3>
        <ol class="feature-list">{_matrix_steps()}</ol>
        <div class="inline-actions">
          {_link("開啟完整多桌輔助教學", "/guide?system=matrix")}
          {_link("查看常見問題", "/faq")}
        </div>
      </article>
    </div>
    <div class="action-strip">
      <div>
        <strong>讀完畫面，再進入 MT MATRIX</strong>
        <p>需要登入或授權協助時，請聯繫官方 LINE；不要提供密碼。</p>
      </div>
      <div class="inline-actions">
        {button("進入 MATRIX", MATRIX)}
        {_link("聯繫 LINE 客服", LINE)}
      </div>
    </div>
  </section>
</div>
'''

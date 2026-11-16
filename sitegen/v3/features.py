from html import escape

from ..common import (
    AUTO,
    DATA,
    LINE,
    MATRIX,
    arrow,
    button,
    dealer,
    eyebrow,
    image_note,
    logo,
    screen,
)


def _matrix_feature(index, step, anchor, surface=False):
    title, lead, body, visuals = step
    media_items = []
    for name, label in visuals:
        media_items.append(screen(name, label, cls="feature-screen", eager=index == 0))
    media = "".join(media_items)
    if len(media_items) > 1:
        media = f'<div class="media-stack">{media}</div>'
    if anchor == "radar":
        media = f'<div class="radar-scroll" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">{media}</div>'
    direction = " reverse" if index in (2, 4) else ""
    section_class = "surface-section" if surface else "content-section"
    heading_id = f"matrix-{anchor}-title"
    return f'''
<section class="{section_class}" id="{anchor}" aria-labelledby="{heading_id}">
  <div class="wrap">
    <article class="feature-row{direction}">
      <div class="feature-media">
        <div class="product-caption"><span>MT MATRIX</span><span>{escape(title)}</span></div>
        {media}
        {image_note()}
      </div>
      <div class="feature-copy">
        {eyebrow(f"步驟 {index + 1:02d}")}
        <h2 id="{heading_id}">{escape(title)}</h2>
        <p class="feature-lead">{escape(lead)}</p>
        <p>{escape(body)}</p>
        <ul><li>欄位、連線與資料狀態以登入後的程式介面為準。</li></ul>
      </div>
    </article>
  </div>
</section>'''


def _matrix_features():
    steps = DATA["matrix_steps"]
    anchors = ("platform", "radar", "analysis", "formulas", "parity")
    return "".join(
        _matrix_feature(index, step, anchors[index], surface=index in (1, 3))
        for index, step in enumerate(steps)
    )


def render():
    """Return the new MT MATRIX feature page main content."""
    live6 = dealer(
        "live6",
        label="Game+ 公開 MT 人物展示素材，非御策官方荷官名單",
        cls="hero-dealer",
        eager=True,
    )
    return f'''
<div class="features-page">
  <section class="page-hero" aria-labelledby="matrix-page-title">
    <div class="wrap hero-layout">
      <div class="hero-copy">
        <div class="hero-product-mark">{logo()}<span><b>MT MATRIX</b><small>多桌百家輔助</small></span></div>
        {eyebrow("平台・雷達・分析・算牌")}
        <h1 id="matrix-page-title">多桌資訊，<br><span>集中查看。</span></h1>
        <p>先確認平台連線，再從多桌雷達找到要觀察的桌台；AI 模型、四式算牌與終值奇偶集中在同一套觀察流程裡。</p>
        <div class="hero-actions">
          {button("進入 MATRIX 多桌輔助", MATRIX)}
          {button("閱讀五步操作教學", "/guide?system=matrix", "outline")}
        </div>
        <p class="note">分析方向、公式與顯示數值僅供資訊輔助，不保證預測下一局或獲利。</p>
      </div>
      <div class="hero-media" aria-label="MT MATRIX 真實介面與人物展示">
        <div class="portrait-stage">
          {live6}
          <div class="stage-screen">
            <div class="product-caption"><span>MT MATRIX</span><span>主面板預覽</span></div>
            {screen("matrix-assist", "MT MATRIX 多桌百家輔助主面板", cls="hero-screen", eager=True)}
          </div>
        </div>
      </div>
    </div>
  </section>

  <nav class="section-nav" aria-label="MT MATRIX 功能導覽">
    <div class="wrap">
      <span>頁內導覽</span>
      <a href="#platform">平台連線</a>
      <a href="#radar">多桌雷達</a>
      <a href="#analysis">AI 模型</a>
      <a href="#formulas">四式算牌</a>
      <a href="#parity">終值奇偶</a>
    </div>
  </nav>

  <section class="content-section" aria-labelledby="matrix-overview-title">
    <div class="wrap">
      <div class="section-intro">
        {eyebrow("MT MATRIX 工作面")}
        <h2 id="matrix-overview-title">從連線開始，逐層核對資訊。</h2>
        <p>MT MATRIX 是多桌資訊整理工具，不代替你的判斷。下面依原操作順序整理五個功能層，圖片可點擊放大查看原始介面。</p>
      </div>
      <div class="feature-grid">
        <article><span class="eyebrow">01</span><h3>平台連線</h3><p>確認帳號授權、平台選擇與目前連線狀態。</p></article>
        <article><span class="eyebrow">02</span><h3>多桌雷達</h3><p>並列桌台、方向與可信度，再選擇要觀察的桌台。</p></article>
        <article><span class="eyebrow">03</span><h3>分析與計算</h3><p>查看 AI 綜合、四式結果、牌值與終值奇偶欄位。</p></article>
      </div>
    </div>
  </section>

  {_matrix_features()}

  <section class="surface-section" aria-labelledby="matrix-support-title">
    <div class="wrap">
      <div class="section-intro">
        {eyebrow("相容性與使用界線")}
        <h2 id="matrix-support-title">瀏覽器開啟，先看清限制。</h2>
        <p>不用另行下載安裝檔，直接用瀏覽器開啟系統；實際平台與遊戲操作方式，以登入後的程式介面為準。</p>
      </div>
      <div class="feature-grid">
        <article><h3>相容性</h3><div class="facts"><span>電腦</span><span>Android 手機</span><span>iPhone</span></div><p>可在上述裝置使用瀏覽器進入 MT MATRIX。</p></article>
        <article><h3>風險提醒</h3><p>百家樂結果具有不確定性，AI 分析、歷史牌路與公式方向都不能保證下一局或獲利。</p><p class="note">展示圖片是介面截圖，不是即時桌台或實際送單畫面；請理性評估風險並遵守所在地法規。</p></article>
        <article><h3>需要協助</h3><p>登入或授權有問題時，請提供會員帳號、問題描述與錯誤畫面；不要提供密碼。</p><a class="text-link" href="{escape(LINE, quote=True)}">聯繫官方 LINE 客服 {arrow()}</a></article>
      </div>
    </div>
  </section>

  <section class="cta-section" aria-labelledby="matrix-cta-title">
    <div class="wrap cta-layout">
      <div><p class="eyebrow">五步操作順序已整理</p><h2 id="matrix-cta-title">先讀懂畫面，<br><span>再進入 MATRIX。</span></h2><p>登入與連線 → 多桌雷達 → AI 綜合 → 四式算牌 → 終值奇偶。</p></div>
      <div class="hero-actions">{button("進入 MATRIX 多桌輔助", MATRIX)}{button("查看完整操作教學", "/guide?system=matrix", "outline")}</div>
    </div>
  </section>
</div>
'''

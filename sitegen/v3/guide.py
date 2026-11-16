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


def _text(value):
    return escape(str(value))


def _preview(system, initial_system):
    is_auto = system == "auto"
    hidden = " hidden" if system != initial_system else ""
    title = "MT AUTO 自動下注推薦與配注" if is_auto else "MT MATRIX 多桌百家輔助主面板"
    image = "auto-strategy" if is_auto else "matrix-assist"
    product = "百家自動下注" if is_auto else "多桌百家輔助"
    return f'''
      <div class="guide-preview guide-preview-{'auto' if is_auto else 'matrix'}" id="guide-preview-{system}" data-guide-preview="{system}"{hidden}>
        <div class="product-caption"><span>{product}</span><span>介面預覽</span></div>
        {screen(image, title, "guide-hero-screen", eager=True)}
        <p class="preview-caption">{("配注・注額・停止條件・執行紀錄" if is_auto else "連線・多桌雷達・AI 分析・算牌")}</p>
      </div>'''


def _step_media(shots):
    if not shots:
        return '<p class="note">本步驟未提供獨立介面截圖，請以程式內顯示的登入、授權與連線狀態為準。</p>'
    images = []
    for name, label in shots:
        image = screen(name, label, f"step-screen guide-screen-{name}")
        if name == "multitable-radar":
            image = f'''<div class="radar-scroll" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">{image}</div>'''
        images.append(image)
    media_class = "step-media media-stack" if len(images) > 1 else "step-media"
    return f'<div class="{media_class}">{"".join(images)}</div>'


def _step(system, number, step):
    short, title, description, shots = step
    return f'''
      <article class="guide-step" id="{system}-step{number}">
        <div class="step-heading">
          <span class="step-number" aria-hidden="true">{number:02d}</span>
          <div><span class="step-kicker">{_text(short)}</span><h2>{_text(title)}</h2></div>
        </div>
        <p class="step-description">{_text(description)}</p>
        {_step_media(shots)}
      </article>'''


def _panel(system, steps, initial_system):
    is_auto = system == "auto"
    hidden = " hidden" if system != initial_system else ""
    product = "MT AUTO 百家自動下注" if is_auto else "MT MATRIX 多桌百家輔助"
    intro = (
        "從登入、配注與注額，到停止條件及執行紀錄；每一項先確認，再進入對應系統。"
        if is_auto else
        "從平台連線、多桌雷達到分析模型，把不同觀察角度放回同一條清楚路徑。"
    )
    entry = button("進入自動下注", AUTO) if is_auto else button("進入多桌百家輔助", MATRIX)
    links = "".join(
        f'<a href="#{system}-step{index}"><span>{index:02d}</span><span>{_text(step[0])}</span></a>'
        for index, step in enumerate(steps, 1)
    )
    articles = "".join(_step(system, index, step) for index, step in enumerate(steps, 1))
    return f'''
    <section class="guide-panel content-section guide-panel-{system}" id="guide-panel-{system}" role="tabpanel" aria-labelledby="guide-tab-{system}"{hidden}>
      <div class="wrap">
        <div class="section-intro guide-panel-intro">
          <div>{eyebrow(product)}<h2>{"先設定，再執行。" if is_auto else "先連線，再看清。"}</h2><p>{intro}</p></div>
          {logo(auto=is_auto, cls="guide-panel-logo")}
        </div>
        <div class="guide-layout">
          <aside class="guide-sidebar" aria-label="{product}步驟導覽">
            <p class="sidebar-label">{product}／使用流程</p>
            <nav aria-label="{product}章節">{links}</nav>
            <a class="text-link" href="/contact">需要操作協助 {arrow()}</a>
          </aside>
          <div class="guide-steps">
            {articles}
            <div class="note">{image_note()}</div>
            <div class="guide-finish"><div><span class="finish-label">完成閱讀</span><h3>確認設定，再開始。</h3><p>畫面中的資料僅供介面說明；實際狀態與限制以進入系統後的程式顯示為準。</p></div>{entry}</div>
          </div>
        </div>
      </div>
    </section>'''


def _tabs(initial_system):
    matrix_selected = "true" if initial_system == "matrix" else "false"
    auto_selected = "true" if initial_system == "auto" else "false"
    return f'''
    <section class="guide-system-tabs surface-section" aria-label="選擇操作教學系統">
      <div class="wrap">
        <div class="guide-tabs" role="tablist" aria-label="操作教學分類">
          <button type="button" class="guide-tab guide-tab-matrix" id="guide-tab-matrix" role="tab" aria-selected="{matrix_selected}" aria-controls="guide-panel-matrix" data-guide="matrix" tabindex="{'0' if initial_system == 'matrix' else '-1'}">{logo(cls="guide-tab-logo")}<span><b>多桌百家輔助</b><small>MT MATRIX · 五步</small></span>{arrow()}</button>
          <button type="button" class="guide-tab guide-tab-auto" id="guide-tab-auto" role="tab" aria-selected="{auto_selected}" aria-controls="guide-panel-auto" data-guide="auto" tabindex="{'0' if initial_system == 'auto' else '-1'}">{logo(auto=True, cls="guide-tab-logo")}<span><b>百家自動下注</b><small>MT AUTO · 六步</small></span>{arrow()}</button>
        </div>
      </div>
    </section>'''


def render(initial_system="matrix"):
    initial = "auto" if initial_system == "auto" else "matrix"
    matrix_steps = DATA["matrix_steps"]
    auto_steps = DATA["auto_steps"]
    return f'''
<div class="guide-page" data-guide-page data-guide-system="{initial}">
  <section class="page-hero guide-hero" aria-labelledby="guide-title">
    <div class="wrap hero-layout">
      <div class="hero-copy">
        {eyebrow("操作教學／系統選擇")}
        <h1 id="guide-title">先看懂流程，<br><em>再進入工具。</em></h1>
        <p>依用途選擇多桌百家輔助或自動下注，沿著對應步驟與真實介面，完成操作前的確認。</p>
        <div class="hero-actions">{button("閱讀多桌輔助五步", "#matrix-step1")}{button("閱讀自動下注六步", "#auto-step1", "outline")}</div>
        <p class="note">介面截圖為展示素材，非即時資料；實際狀態與限制以程式內顯示為準。</p>
      </div>
      <div class="hero-media" aria-label="兩套工具的真實介面預覽">
        {_preview("matrix", initial)}
        {_preview("auto", initial)}
      </div>
    </div>
  </section>

  {_tabs(initial)}
  {_panel("matrix", matrix_steps, initial)}
  {_panel("auto", auto_steps, initial)}

  <section class="content-section guide-afterword">
    <div class="wrap cta-layout">
      <div>{eyebrow("操作前提醒")}<h2>資訊是輔助，<br>判斷仍在你手中。</h2><p>若對登入、授權或畫面狀態有疑問，請聯繫客服協助確認；不要提供密碼。</p></div>
      <div class="hero-actions"><a class="text-link" href="/contact">聯繫客服 {arrow()}</a><a class="text-link" href="{LINE}">LINE 官方客服 {arrow()}</a></div>
    </div>
  </section>
</div>'''

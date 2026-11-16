from html import escape

from ..common import AUTO, DATA, MATRIX, arrow, button, image_note, logo, screen


_SYSTEMS = ("matrix", "auto")


def _text(value):
    """Escape text loaded from the original data contract."""
    return escape(str(value))


def _preview(system, initial, eager=False):
    is_auto = system == "auto"
    preview_id = f"guide-preview-{system}"
    hidden = " hidden" if system != initial else ""
    product_name = "MT AUTO" if is_auto else "MT MATRIX"
    product_label = "百家自動下注" if is_auto else "多桌百家輔助"
    image_name = "auto-strategy" if is_auto else "matrix-assist"
    image_label = "自動下注推薦與配注設定" if is_auto else "百家輔助主面板與 AI 分析"
    image = screen(image_name, image_label, eager=eager)
    return f'''
    <article id="{preview_id}" data-guide-preview="{system}" class="guide-preview-card"{hidden}>
      <div class="product-heading">
        {logo(auto=is_auto)}
        <div>
          <h3>{product_name}</h3>
          <p>{product_label}／介面預覽</p>
        </div>
      </div>
      <div class="guide-preview-thumb">{image}</div>
    </article>'''


def _tabs(initial):
    matrix_selected = "true" if initial == "matrix" else "false"
    auto_selected = "true" if initial == "auto" else "false"
    matrix_tabindex = "0" if initial == "matrix" else "-1"
    auto_tabindex = "0" if initial == "auto" else "-1"
    return f'''
    <div class="product-tabs" role="tablist" aria-label="操作教學系統">
      <button type="button" class="product-tab" id="guide-tab-matrix" role="tab"
        aria-selected="{matrix_selected}" aria-controls="guide-panel-matrix"
        data-guide="matrix" tabindex="{matrix_tabindex}">
        {logo()}
        <span><strong>多桌百家輔助</strong><small>MT MATRIX／五步教學</small></span>
        <span aria-hidden="true">{arrow()}</span>
      </button>
      <button type="button" class="product-tab" id="guide-tab-auto" role="tab"
        aria-selected="{auto_selected}" aria-controls="guide-panel-auto"
        data-guide="auto" tabindex="{auto_tabindex}">
        {logo(auto=True)}
        <span><strong>百家自動下注</strong><small>MT AUTO／六步教學</small></span>
        <span aria-hidden="true">{arrow()}</span>
      </button>
    </div>'''


def _step_media(shots):
    if not shots:
        return (
            '<p class="portal-notice">本步驟未提供獨立介面截圖，請以程式內顯示的登入、'
            '授權與連線狀態為準。</p>'
        )

    rendered = []
    for name, label in shots:
        image = screen(name, label)
        if name == "multitable-radar":
            image = f'''
            <div class="radar-scroll" tabindex="0" role="region" aria-label="左右滑動查看完整多桌雷達">
              {image}
            </div>'''
        rendered.append(f'<div class="media-display">{image}</div>')

    return f'<div class="two-column">{"".join(rendered)}</div>' if len(rendered) > 1 else rendered[0]


def _step(system, number, step):
    short, title, description, shots = step
    step_id = f"{system}-step{number}"
    return f'''
    <article id="{step_id}" class="portal-panel guide-step-panel">
      <div class="section-top">
        <div>
          <p class="kicker">{number:02d}／{_text(short)}</p>
          <h3>{_text(title)}</h3>
          <p>{_text(description)}</p>
        </div>
      </div>
      {_step_media(shots)}
      {f'<a class="text-link refine-next" href="#{system}-step{number+1}">下一步：{_text(DATA[system+"_steps"][number][0])} {arrow()}</a>' if number < len(DATA[system+"_steps"]) else f'<a class="text-link refine-next" href="{AUTO if system == "auto" else MATRIX}">完成核對後，進入系統 {arrow()}</a>'}
    </article>'''


def _sidebar(system, steps, product_name):
    links = "".join(
        f'<a href="#{system}-step{i}"><span>{i:02d}</span>{_text(step[0])}</a>'
        for i, step in enumerate(steps, 1)
    )
    return f'''
    <aside class="guide-sidebar" aria-label="{_text(product_name)}步驟目錄">
      <p class="kicker">{_text(product_name)}／操作目錄</p>
      <details class="refine-directory" data-phone-collapse open><summary>查看步驟目錄</summary><nav aria-label="{_text(product_name)}教學步驟">{links}</nav></details>
      <a class="text-link" href="/contact">需要操作協助 {arrow()}</a>
    </aside>'''


def _panel(system, steps, initial):
    is_auto = system == "auto"
    product_name = "MT AUTO 百家自動下注" if is_auto else "MT MATRIX 多桌百家輔助"
    title = "自動下注六步設定" if is_auto else "多桌輔助五步操作"
    intro = (
        "依序確認推薦與配注、金額、停止條件，再查看執行狀態與紀錄。"
        if is_auto
        else "依序完成登入連線、雷達觀察、AI 綜合、四式算牌與終值奇偶查看。"
    )
    entry_url = AUTO if is_auto else MATRIX
    entry_label = "進入自動下注" if is_auto else "進入多桌百家輔助"
    hidden = " hidden" if initial != system else ""
    steps_markup = "".join(_step(system, i, step) for i, step in enumerate(steps, 1))
    return f'''
    <section id="guide-panel-{system}" role="tabpanel" aria-labelledby="guide-tab-{system}"
      class="portal-section" data-guide-panel="{system}"{hidden}>
      <div class="section-top">
        <div>
          <p class="kicker">{_text(product_name)}</p>
          <h2>{title}</h2>
          <p>{intro}</p>
        </div>
        <div class="product-heading">
          {logo(auto=is_auto)}
          <div>
            <h3>{"MT AUTO" if is_auto else "MT MATRIX"}</h3>
            <p>{"百家自動下注" if is_auto else "多桌百家輔助"}</p>
          </div>
        </div>
      </div>
      <p class="refine-progress" data-refine-progress="{system}" role="status">共{len(steps)}步，依順序操作。</p>
      <div class="guide-layout">
        {_sidebar(system, steps, product_name)}
        <div class="guide-steps">
          {steps_markup}
          {image_note()}
          <div class="action-strip">
            <p class="portal-notice">畫面中的資料僅供介面說明；實際狀態、限制與操作結果以登入後程式顯示為準。分析、公式與配注策略不保證預測下一局或獲利。</p>
            <div class="inline-actions">
              {button(entry_label, entry_url, "outline")}
              <a class="text-link" href="/contact">需要客服協助 {arrow()}</a>
            </div>
          </div>
        </div>
      </div>
    </section>'''


def render(system="matrix"):
    """Return the compact guide content for the portal shell."""
    initial = system if system in _SYSTEMS else "matrix"
    matrix_steps = DATA["matrix_steps"]
    auto_steps = DATA["auto_steps"]
    return f'''
    <section class="portal-pagehead" aria-labelledby="guide-page-title">
      <div>
        <p class="kicker">操作教學／兩套系統</p>
        <h1 id="guide-page-title">兩套系統的操作步驟</h1>
        <p>依產品選擇教學，從登入、分析或設定到執行與紀錄，逐步核對介面。</p>
      </div>
      <div class="pagehead-actions">
        {button("進入多桌輔助", MATRIX)}
        {button("進入自動下注", AUTO, "outline")}
      </div>
    </section>

    <section class="portal-section" aria-labelledby="guide-choice-title">
      <div class="section-top">
        <div>
          <h2 id="guide-choice-title">選擇教學系統</h2>
          <p>兩套產品分開閱讀；切換分頁或使用下方步驟目錄，直接前往對應內容。</p>
        </div>
      </div>
      {_tabs(initial)}
      <div class="guide-preview-wrap">
        {_preview("matrix", initial, eager=initial == "matrix")}
        {_preview("auto", initial, eager=initial == "auto")}
      </div>
    </section>

    {_panel("matrix", matrix_steps, initial)}
    {_panel("auto", auto_steps, initial)}
    '''

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



def _install_card(auto=False):
    name = "百家自動下注" if auto else "多桌百家輔助"
    url = AUTO if auto else MATRIX
    key = "auto" if auto else "matrix"
    def steps(ios):
        labels = [("開啟 Safari", "開啟下方程式入口"), ("點選分享", "按 Safari 的分享圖示"), ("加入主畫面", "選擇加入主畫面，再點加入")] if ios else [("開啟 Chrome", "開啟下方程式入口"), ("點選選單", "點右上角 ⋮"), ("加入主畫面", "選擇安裝應用程式或加入主畫面，確認新增")]
        marks = ["↗", "↑" if ios else "⋮", "+"]
        return "".join(f'''<figure class="install-step"><svg viewBox="0 0 200 250" role="img" aria-label="步驟 {i+1}：{label}（操作示意）"><rect x="36" y="7" width="128" height="236" rx="17" fill="#202128" stroke="#555662" stroke-width="2"/><rect x="43" y="16" width="114" height="218" rx="12" fill="#30323b"/><rect x="76" y="18" width="48" height="8" rx="4" fill="#101116"/><rect x="50" y="42" width="100" height="15" rx="5" fill="#51535f"/><text x="100" y="53" text-anchor="middle" fill="#fff" font-size="8">{'Safari' if ios else 'Chrome'}</text><rect x="53" y="70" width="94" height="104" rx="8" fill="#19191f"/><image href="/assets/{'auto-logo' if auto else 'baccarat-logo'}.png" x="75" y="88" width="50" height="50"/><rect x="54" y="183" width="92" height="40" rx="8" fill="#a83765"/><text x="100" y="211" text-anchor="middle" font-size="27" fill="white">{marks[i]}</text><circle cx="148" cy="30" r="13" fill="#e04e86"/><text x="148" y="35" text-anchor="middle" font-size="13" font-weight="bold" fill="white">{i+1}</text></svg><figcaption><strong>{i+1}. {label}</strong><p>{detail}</p></figcaption></figure>''' for i,(label,detail) in enumerate(labels))
    return f'''<article class="portal-panel install-card" id="install-{key}"><div class="product-heading">{logo(auto=auto)}<div><h3>{name}</h3><p>將此工具加入手機主畫面</p></div></div><div class="inline-actions">{button("開啟"+name, url)}</div><h4>iPhone｜Safari</h4><div class="install-steps">{steps(True)}</div><h4>Android｜Chrome</h4><div class="install-steps">{steps(False)}</div><p class="portal-notice">請從程式入口開啟瀏覽器，不要將御策官網加入主畫面。瀏覽器選單名稱可能因版本不同而異。</p></article>'''

def _install_section():
    return f'''<section class="portal-section" id="download-install" aria-labelledby="download-title" style="scroll-margin-top:100px"><div class="section-top"><div><p class="kicker">下載安裝／手機主畫面</p><h2 id="download-title">下載安裝教學</h2><p>選擇你的工具，依照手機系統完成加入主畫面。下方為操作示意圖。</p></div></div><style>.install-card{{margin-bottom:20px}}.install-card h4{{margin:20px 0 10px}}.install-steps{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.install-step{{margin:0;padding:12px;border:1px solid #41414d;border-radius:14px;background:#202128;text-align:center}}.install-step svg{{width:100%;max-width:200px;height:auto}}.install-step p{{font-size:13px;margin:6px 0 0}}@media(max-width:600px){{.install-steps{{grid-template-columns:1fr}}.install-step{{display:grid;grid-template-columns:110px 1fr;align-items:center;text-align:left}}}}</style>{_install_card()}{_install_card(True)}</section>'''

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

    {_install_section()}
    {_panel("matrix", matrix_steps, initial)}
    {_panel("auto", auto_steps, initial)}
    '''

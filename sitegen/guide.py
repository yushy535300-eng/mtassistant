from html import escape

from .common import (
    AUTO,
    DATA,
    MATRIX,
    arrow,
    ambient,
    button,
    chapter,
    eyebrow,
    image_note,
    logo,
    screen,
)


def _text(value):
    """Escape data-provided copy before placing it in the page body."""
    return escape(str(value))


def _preview_matrix(initial):
    hidden = ' hidden' if initial != 'matrix' else ''
    return f'''
    <div class="guide-preview guide-preview-matrix" id="guide-preview-matrix" data-guide-preview="matrix"{hidden}>
      <div class="guide-preview-topline">
        <div class="guide-preview-product">
          {logo(cls="guide-preview-logo")}
          <div><span>多桌百家輔助</span><strong>MT MATRIX</strong></div>
        </div>
      </div>
      <div class="guide-preview-screen">{screen("matrix-assist", "百家輔助教學主面板", "guide-hero-screen", eager=True)}</div>
      <div class="guide-preview-footer">
        <span>連線・多桌雷達・AI 分析・算牌</span>
      </div>
    </div>'''


def _preview_auto(initial):
    hidden = ' hidden' if initial != 'auto' else ''
    return f'''
    <div class="guide-preview guide-preview-auto" id="guide-preview-auto" data-guide-preview="auto"{hidden}>
      <div class="guide-preview-topline">
        <div class="guide-preview-product">
          {logo(auto=True, cls="guide-preview-logo")}
          <div><span>百家自動下注</span><strong>MT AUTO</strong></div>
        </div>
      </div>
      <div class="guide-auto-preview-body">
        <div class="guide-auto-summary">
          <strong>設定完成，再開始。</strong>
          <ul>
            <li>配注方式與推薦來源</li>
            <li>基本單注與單筆上限</li>
            <li>停止時間與停止條件</li>
            <li>執行狀態與紀錄</li>
          </ul>
        </div>
        <div class="guide-preview-screen guide-preview-screen-auto">{screen("auto-strategy", "自動下注推薦與配注設定", "guide-hero-screen")}</div>
      </div>
      <div class="guide-preview-footer">
        <span>配注・注額・停止條件・執行紀錄</span>
      </div>
    </div>'''


def _step_media(system, shots):
    if not shots:
        return '<p class="guide-step-no-media">本步驟未提供獨立介面截圖，請以程式內顯示的登入、授權與連線狀態為準。</p>'

    rendered = []
    for name, label in shots:
        image = screen(name, label, f"guide-step-screen guide-screen-{name}")
        if name == "multitable-radar":
            image = f'''
            <div class="guide-radar-viewport" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">
              {image}
            </div>'''
        rendered.append(image)

    layout = " guide-media-multiple" if len(rendered) > 1 else ""
    return f'<div class="guide-step-media{layout}">{"".join(rendered)}</div>'


def _step_article(system, number, step):
    short, title, description, shots = step
    compact_titles = {
        ('matrix', 3): '切換來源，檢視分析。',
        ('matrix', 4): '核對牌值與公式。',
        ('auto', 2): '選擇配注與來源。',
        ('auto', 3): '核對單注與上限。',
    }
    title = compact_titles.get((system, number), title)
    return f'''
    <article class="guide-step" id="{system}-step{number}">
      <div class="guide-step-marker" aria-hidden="true">
        <span>{number:02d}</span>
        <i></i>
      </div>
      <div class="guide-step-main">
        <div class="guide-step-kicker">{number:02d} ／ {_text(short)}</div>
        <h3>{_text(title)}</h3>
        <p class="guide-step-description">{_text(description)}</p>
        {_step_media(system, shots)}
      </div>
    </article>'''


def _panel(system, steps, initial):
    hidden = ' hidden' if initial != system else ''
    is_auto = system == "auto"
    title = "自動下注教學" if is_auto else "百家輔助教學"
    eyebrow_text = "自動下注／逐項設定" if is_auto else "多桌輔助／逐步觀察"
    chapter_title = "先設定，再執行。" if is_auto else "先連線，再看清。"
    chapter_text = (
        "從登入、配注與注額，到停止條件及執行紀錄；每一項先確認，再進入對應系統。"
        if is_auto
        else "從平台連線、多桌雷達到分析模型，把不同觀察角度放回同一條清楚路徑。"
    )
    aside_links = "".join(
        f'<a href="#{system}-step{i}"><span>{i:02d}</span>{_text(step[0])}</a>'
        for i, step in enumerate(steps, 1)
    )
    articles = "".join(_step_article(system, i, step) for i, step in enumerate(steps, 1))
    entry_label = "進入自動下注" if is_auto else "進入多桌百家輔助"
    entry_url = AUTO if is_auto else MATRIX

    return f'''
    <section id="guide-panel-{system}" role="tabpanel" aria-labelledby="guide-tab-{system}" class="guide-panel guide-panel-{system} paper"{hidden}>
      <div class="wrap">
        <div class="guide-panel-intro">
          <div class="guide-panel-title">
            {eyebrow(eyebrow_text)}
            {chapter("", chapter_title, chapter_text)}
          </div>
          <div class="guide-panel-identity">
            {logo(auto=is_auto, cls="guide-panel-logo")}
            <span>{title}</span>
          </div>
        </div>
        <div class="guide-layout">
          <aside class="guide-aside" aria-label="{title}步驟導覽">
            <span class="guide-aside-title">{title}／使用流程</span>
            <nav aria-label="{title}章節">
              {aside_links}
            </nav>
            <a class="text-link guide-support-link" href="/contact">需要操作協助 {arrow()}</a>
          </aside>
          <div class="guide-steps">
            {articles}
            <div class="guide-panel-note">{image_note()}</div>
            <div class="guide-finish">
              <div>
                <span class="guide-finish-label">完成閱讀</span>
                <h3>確認設定，再開始。</h3>
                <p>畫面中的資料僅供介面說明；實際狀態與限制以進入系統後的程式顯示為準。</p>
              </div>
              {button(entry_label, entry_url, "primary")}
            </div>
          </div>
        </div>
      </div>
    </section>'''


def _tabs(initial):
    matrix_active = 'true' if initial == 'matrix' else 'false'
    auto_active = 'true' if initial == 'auto' else 'false'
    matrix_index = '0' if initial == 'matrix' else '-1'
    auto_index = '0' if initial == 'auto' else '-1'
    return f'''
    <section class="guide-system-tabs" aria-label="選擇操作教學系統">
      <div class="wrap">
        <div class="guide-tabs-heading">
          <span>選擇一套流程</span>
          <p>兩套系統分開閱讀，步驟與介面不相互混用。</p>
        </div>
        <div class="guide-tabs" role="tablist" aria-label="操作教學分類">
          <button type="button" class="guide-tab guide-tab-matrix" id="guide-tab-matrix" role="tab" aria-selected="{matrix_active}" aria-controls="guide-panel-matrix" data-guide="matrix" tabindex="{matrix_index}">
            {logo(cls="guide-tab-logo")}
            <span><b>多桌百家輔助</b><small>MT MATRIX</small></span>
            <i aria-hidden="true">↗</i>
          </button>
          <button type="button" class="guide-tab guide-tab-auto" id="guide-tab-auto" role="tab" aria-selected="{auto_active}" aria-controls="guide-panel-auto" data-guide="auto" tabindex="{auto_index}">
            {logo(auto=True, cls="guide-tab-logo")}
            <span><b>百家自動下注</b><small>MT AUTO</small></span>
            <i aria-hidden="true">↗</i>
          </button>
        </div>
      </div>
    </section>'''


def render(system='matrix'):
    """Return the guide page's main content without document chrome."""
    initial = 'auto' if system == 'auto' else 'matrix'
    matrix_steps = DATA["matrix_steps"]
    auto_steps = DATA["auto_steps"]
    return f'''
    <div class="guide-page" data-guide-page>
      <section class="guide-hero section">
        <div class="guide-hero-ambient" aria-hidden="true">{ambient('guide')}</div>
        <div class="wrap guide-hero-layout">
          <div class="guide-hero-copy">
            {eyebrow("操作教學／系統選擇")}
            <h1>操作教學。<br><em>選對工具。</em></h1>
            <p>選擇「多桌百家輔助」或「自動下注」，<br>沿著各自的步驟與真實介面，完成操作前的確認。</p>
            <div class="guide-hero-actions">
              <a class="guide-jump-link" href="#guide-panel-matrix"><span>01</span>閱讀多桌輔助流程 {arrow()}</a>
              <a class="guide-jump-link" href="#guide-panel-auto"><span>02</span>閱讀自動下注流程 {arrow()}</a>
            </div>
            <div class="guide-hero-note"><span aria-hidden="true"></span><p>介面截圖為展示素材，非即時資料；操作前請以程式內狀態為準。</p></div>
          </div>
          <div class="guide-hero-stage">
            {_preview_matrix(initial)}
            {_preview_auto(initial)}
          </div>
        </div>
      </section>

      <section class="guide-introduction section paper">
        <div class="wrap guide-introduction-layout">
          <div>
            {eyebrow("兩套系統／兩條路徑")}
            <h2>每一步，都有對應的畫面。</h2>
          </div>
          <p>多桌輔助著重桌台、牌路與分析視角；自動下注著重配注、注額、停止條件與紀錄。以下內容分開整理，保留原始步驟文字與對應截圖。</p>
        </div>
      </section>

      {_tabs(initial)}
      {_panel("matrix", matrix_steps, initial)}
      {_panel("auto", auto_steps, initial)}

      <section class="guide-afterword section">
        <div class="wrap guide-afterword-layout">
          <span class="guide-afterword-index">教學／03</span>
          <div>
            <h2>讀懂流程。<br><em>再進入工具。</em></h2>
            <p>若對登入、授權或畫面狀態有疑問，請聯繫客服協助確認；不要提供密碼。</p>
          </div>
          <a class="text-link" href="/contact">聯繫客服 {arrow()}</a>
        </div>
      </section>
    </div>'''

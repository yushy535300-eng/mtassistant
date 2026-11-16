from html import escape

from .common import (
    AUTO,
    DATA,
    LINE,
    MATRIX,
    ambient,
    arrow,
    button,
    chapter,
    dealer,
    eyebrow,
    image_note,
    logo,
    screen,
)


def _text_link(label, url):
    """Render a compact editorial link without introducing a second icon system."""
    return (
        f'<a class="text-link mx-text-link" href="{escape(url, quote=True)}">'
        f'<span>{escape(label)}</span>{arrow()}</a>'
    )


def _dealer_with_caption():
    """Keep the shared dealer helper while retaining the required provenance caption."""
    markup = dealer(
        "live6",
        label="Game+ 公開 MT 人物展示素材，非御策官方荷官名單",
        cls="mx-dealer-image",
        eager=False,
    )
    caption = (
        "來源：Game+ 公開 MT 人物展示素材；非御策官方荷官名單。"
        "商業授權尚未核實，正式部署前需確認。"
    )
    return markup.replace("</figure>", f"<figcaption>{caption}</figcaption></figure>")


def _related_questions():
    """Select the existing FAQ entries relevant to MATRIX without inventing claims."""
    selected = {
        "使用方式": {"電腦和手機都能使用嗎？"},
        "介面展示": {"官網展示的是即時資料嗎？"},
        "分析與結果": {"AI 分析或配注策略可以保證獲利嗎？"},
    }
    items = []
    for category, question, answer in DATA.get("questions", []):
        if question in selected.get(category, set()):
            items.append(
                f'<details class="mx-faq-item">'
                f'<summary><span><small>{escape(category)}</small>{escape(question)}</span>'
                f'<b aria-hidden="true">＋</b></summary>'
                f'<p>{escape(answer)}</p></details>'
            )
    return "".join(items)


def render():
    """Return the feature page main content; the parent builder supplies head/header/footer."""
    live6 = _dealer_with_caption()
    related_questions = _related_questions()

    return f'''
<div class="features-page">
  <section class="mx-hero" aria-labelledby="matrix-page-title">
    {ambient("matrix")}
    <div class="wrap mx-hero-grid">
      <div class="mx-hero-copy">
        <div class="mx-product-signature">
          {logo(cls="mx-hero-logo")}
          <span><b>MT MATRIX</b><small>多桌百家輔助</small></span>
        </div>
        {eyebrow("桌台・牌路・多角度分析")}
        <h1 id="matrix-page-title">掌握多桌。<br><em>看清細節。</em></h1>
        <p class="mx-hero-lede">把桌台、牌路、模型與操作入口放在同一個觀察流程裡。<br>先讀取畫面，再依你的判斷決定下一步。</p>
        <div class="mx-hero-actions">
          {button("進入 MATRIX 多桌輔助", MATRIX, "primary")}
          {button("閱讀多桌輔助教學", "/guide?system=matrix", "outline")}
        </div>
        <p class="mx-hero-caution">分析方向與介面欄位僅供資訊輔助，不保證預測下一局或獲利。</p>
      </div>
      <div class="mx-hero-visual">
        <div class="mx-visual-kicker"><span>MT MATRIX / 主面板</span><span>真實介面截圖</span></div>
        <div class="mx-hero-frame">
          {screen("matrix-assist", "MATRIX ASSIST 多桌輔助主面板", "mx-main-screen", eager=True)}
        </div>
        <div class="mx-visual-footer"><span>桌台資訊・牌路分析・模型入口</span><span>點圖放大檢視</span></div>
      </div>
    </div>
  </section>

  <section class="section paper mx-intro" aria-labelledby="matrix-overview-title">
    <div class="wrap mx-intro-grid">
      <div class="mx-intro-lead">
        {chapter("00", "一個介面，<br>多種觀察角度。", "先確認平台與連線，再從桌台、牌路與模型欄位建立自己的閱讀順序。")}
        <p class="mx-intro-statement" id="matrix-overview-title">MT MATRIX 是多桌資訊整理工具，不代替你的判斷。畫面將不同來源放回同一個工作面，讓你知道目前看見的是什麼、還需要核對什麼。</p>
        <div class="mx-intro-links">
          {_text_link("查看五步操作教學", "/guide?system=matrix")}
          {_text_link("先讀常見問題", "/faq")}
        </div>
      </div>
      <div class="mx-field-sheet">
        <div class="mx-sheet-top"><span>主面板可讀欄位</span><b>5 個資訊層</b></div>
        <ol>
          <li><span>01</span><b>桌台</b><em>目前觀察的桌台與狀態</em></li>
          <li><span>02</span><b>牌路</b><em>大路及下三路的呈現資訊</em></li>
          <li><span>03</span><b>模型</b><em>AI 綜合與牌路策略來源</em></li>
          <li><span>04</span><b>算牌</b><em>V38 四式的牌面與公式結果</em></li>
          <li><span>05</span><b>奇偶</b><em>牌值、計算過程與終值</em></li>
        </ol>
        <p>欄位名稱與狀態以登入後的實際程式介面為準。</p>
      </div>
    </div>
  </section>

  <nav class="mx-index" aria-label="MATRIX 功能導覽">
    <div class="wrap mx-index-inner">
      <span>頁內導覽</span>
      <a href="#radar"><b>01</b>多桌雷達</a>
      <a href="#analysis"><b>02</b>AI 綜合</a>
      <a href="#formulas"><b>03</b>四式算牌</a>
      <a href="#parity"><b>04</b>終值奇偶</a>
    </div>
  </nav>

  <section class="section paper mx-feature mx-radar" id="radar" aria-labelledby="matrix-radar-title">
    <div class="wrap">
      <div class="mx-section-heading">
        <div>{chapter("01", "多桌節奏，<br>同時掌握。", "把多桌資訊先攤開，再選擇要深入查看的桌台。", "matrix-radar-title")}</div>
        <div class="mx-heading-aside"><span>橫向完整畫面</span><p>雷達畫面寬於一般手機視窗，請在下方區域左右滑動；點圖可開啟原尺寸檢視。</p></div>
      </div>
      <div class="mx-radar-stage">
        <div class="mx-stage-bar"><span>多桌雷達</span><span>左右滑動查看完整桌台 →</span></div>
        <div class="mx-radar-viewport" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">
          {screen("multitable-radar", "多桌雷達完整介面", "mx-radar-screen")}
        </div>
        {image_note()}
      </div>
      <div class="mx-connection">
        <div class="mx-connection-copy">
          {eyebrow("平台連線")}
          <h3>先確認平台，<br>再進入觀察。</h3>
          <p>平台區顯示目前選擇與連線狀態。進入對應平台前，先核對帳號授權及程式內提示；狀態以登入後畫面為準。</p>
          <ul class="mx-check-list"><li>平台選擇與目前連線狀態</li><li>對應入口與操作前核對</li></ul>
        </div>
        <div class="mx-connection-shot">
          {screen("platform-connection", "平台切換與連線狀態", "mx-small-screen")}
          {image_note()}
        </div>
      </div>
    </div>
  </section>

  <section class="mx-human-interlude" aria-label="MT 人物展示素材說明">
    <div class="wrap mx-human-grid">
      <div class="mx-human-photo">{live6}</div>
      <div class="mx-human-copy">
        {eyebrow("閱讀介面之前")}
        <h2>把真人情境，<br><em>留在產品之外。</em></h2>
        <p>MT MATRIX 整理的是桌台與分析欄位；人物影像只是公開展示情境，不代表御策官方荷官、合作或代言關係。</p>
        <p class="mx-human-note">正式部署前，請確認此素材的商業使用授權。</p>
      </div>
    </div>
  </section>

  <section class="section mx-feature mx-analysis" id="analysis" aria-labelledby="matrix-analysis-title">
    <div class="wrap mx-analysis-grid">
      <div class="mx-analysis-copy">
        {chapter("02", "不同角度，<br>同頁檢視。", "模型選單提供分析來源與牌路策略入口；它整理資訊，不替你做結果承諾。")}
        <p id="matrix-analysis-title">開啟模型選單後，可辨認目前採用的分析來源，再回到主面板查看當局牌型、推薦資訊與分析內容。AI 綜合不是可靠預測器，畫面中的方向仍需由使用者自行評估。</p>
        <div class="mx-analysis-points"><div><b>01</b><span>模型來源與綜合觀察</span></div><div><b>02</b><span>大路及下三路分析資訊</span></div><div><b>03</b><span>主面板欄位與當局資料</span></div></div>
      </div>
      <div class="mx-analysis-shot">
        <div class="mx-stage-bar"><span>AI 綜合模型選單</span><span>欄位檢視</span></div>
        {screen("analysis-models", "AI 綜合模型選單", "mx-models-screen")}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="section paper mx-feature mx-formulas" id="formulas" aria-labelledby="matrix-formulas-title">
    <div class="wrap mx-split-grid">
      <div class="mx-formulas-shot">
        {screen("four-formulas", "V38 四式算牌完整面板", "mx-formulas-screen")}
        {image_note()}
      </div>
      <div class="mx-split-copy">
        {chapter("03", "牌值與公式，<br>清楚並列。", "從當局牌面開始，依序核對四式結果與下一局投票欄位。")}
        <p id="matrix-formulas-title">V38 四式算牌面板顯示 Shoe、Round、閒莊牌面與點數，以及 A 公式、B 公式、MUL 與 ADD 的觀察結果。</p>
        <ul class="mx-rule-list"><li><b>牌面</b><span>查看當局閒、莊牌面與點數</span></li><li><b>四式</b><span>核對 A、B、MUL、ADD 的顯示結果</span></li><li><b>投票</b><span>查看面板提供的下一局方向欄位</span></li></ul>
        <p class="mx-disclaimer">公式與方向僅供資訊輔助，不代表下一局必然結果。</p>
      </div>
    </div>
  </section>

  <section class="section mx-feature mx-parity" id="parity" aria-labelledby="matrix-parity-title">
    <div class="wrap mx-split-grid mx-split-grid-reverse">
      <div class="mx-split-copy">
        {chapter("04", "計算過程，<br><em>完整呈現。</em>", "把牌面、牌值、計算過程與終值放在同一個模型裡，方便回看每個欄位。")}
        <p id="matrix-parity-title">終值奇偶模型是另一個可供檢視的觀察角度。依序閱讀牌面、牌值、計算過程、終值與顯示方向，不把介面方向解讀成結果保證。</p>
        <div class="mx-parity-callout"><span>使用提醒</span><strong>先看計算，再作判斷。</strong><small>畫面中的數值為介面展示內容，非即時資料。</small></div>
      </div>
      <div class="mx-parity-shot">
        {screen("parity-model", "終值奇偶模型完整面板", "mx-parity-screen")}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="section paper mx-support" aria-labelledby="matrix-support-title">
    <div class="wrap mx-support-grid">
      <div class="mx-support-intro">
        {eyebrow("開始之前")}
        <h2 id="matrix-support-title">相容性、教學，<br><em>先說清楚。</em></h2>
        <p>不用另行下載安裝檔，直接用瀏覽器開啟系統。實際平台及遊戲操作方式，以登入後的程式介面為準。</p>
        <div class="mx-device-line"><span>電腦</span><i></i><span>Android 手機</span><i></i><span>iPhone</span></div>
        <p class="mx-support-note">以瀏覽器開啟系統，可使用電腦、Android 手機與 iPhone；相容性說明依既有常見問題內容整理。</p>
        <div class="mx-support-actions">
          {button("閱讀多桌輔助教學", "/guide?system=matrix", "primary")}
          {_text_link("前往常見問題", "/faq")}
        </div>
      </div>
      <div class="mx-faq-list">
        <div class="mx-faq-heading"><span>相關常見問題</span><b>03</b></div>
        {related_questions}
      </div>
    </div>
  </section>

  <section class="mx-next" aria-label="MATRIX 行動入口">
    <div class="wrap mx-next-grid">
      <div>{eyebrow("你的下一步")}
        <h2>先讀懂畫面。<br><em>再進入 MATRIX。</em></h2>
      </div>
      <div class="mx-next-actions">
        {button("進入 MATRIX 多桌輔助", MATRIX, "primary")}
        {_text_link("需要操作協助？聯繫客服", LINE)}
      </div>
    </div>
  </section>
</div>
'''

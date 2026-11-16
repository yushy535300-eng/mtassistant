from html import escape

from ..common import DATA, MATRIX, AUTO, LINE, logo, screen, button, eyebrow, dealer, arrow, image_note


FAQ_CATEGORIES = ('兩套系統', '使用方式', '帳號授權', '自動下注', '分析與結果', '介面展示')


def _faq_item(index, category, question, answer):
    return f'''<details class="faq-item" data-faq-category="{escape(category, quote=True)}">
  <summary><span class="faq-item__heading"><span class="faq-item__number">{index:02d}</span><span><small>{escape(category)}</small><b>{escape(question)}</b></span></span></summary>
  <p>{escape(answer)}</p>
</details>'''


def _filter_links(total):
    links = [('<a class="faq-filter" href="#faqSearch" data-faq-filter="" aria-current="true"><strong>全部問題</strong><small>顯示完整 %d 題</small></a>' % total)]
    links.extend(
        f'<a class="faq-filter" href="#faqSearch" data-faq-filter="{escape(category, quote=True)}"><strong>{escape(category)}</strong><small>依使用情境篩選</small></a>'
        for category in FAQ_CATEGORIES
    )
    return ''.join(links)


def render():
    questions = DATA['questions']
    total = len(questions)
    faq_items = ''.join(_faq_item(i, category, question, answer) for i, (category, question, answer) in enumerate(questions, 1))

    return f'''<div class="page page-faq">
  <section class="page-hero" aria-labelledby="faq-title">
    <div class="wrap hero-layout">
      <div class="hero-copy">
        {eyebrow('常見問題 / 支援')}
        <h1 id="faq-title">常見問題，<br><span>快速找到答案。</span></h1>
        <p>登入、授權、工具使用與風險說明集中在這裡。用分類或關鍵字查找，仍不確定時再交由官方客服確認。</p>
        <div class="hero-actions">{button('進入 MT MATRIX', MATRIX)}{button('進入 MT AUTO', AUTO, 'outline')}</div>
        <div class="facts"><span><b>{total:02d}</b> 個常見情境</span><span>兩套系統分開說明</span><span>不保存密碼</span></div>
      </div>
      <div class="hero-media">
        <p class="product-caption">MT MATRIX · 多桌百家輔助主面板</p>
        {screen('matrix-assist', 'MT MATRIX 多桌百家輔助主面板', 'hero-screen', True)}
        {image_note()}
      </div>
    </div>
  </section>

  <section class="content-section surface-section" id="faq" aria-labelledby="faq-heading">
    <div class="wrap">
      <div class="section-intro">
        {eyebrow('搜尋 / 分類')}
        <h2 id="faq-heading">用一句話，找到需要的說明。</h2>
        <p>以關鍵字搜尋，或依主題篩選，查看工具的操作說明與使用限制。</p>
      </div>
      <div class="faq-layout">
        <aside class="faq-filters" aria-label="FAQ 問題分類">
          <p class="faq-filters__label">問題分類</p>
          {_filter_links(total)}
          <p class="note">登入或授權問題請提供會員帳號、問題描述與錯誤畫面；請勿提供密碼。</p>
          {button('聯繫 LINE 官方客服', LINE, 'outline')}
        </aside>
        <div class="faq-content">
          <label class="faq-toolbar" for="faqSearch"><span>搜尋常見問題</span><input id="faqSearch" type="search" placeholder="例如：登入、停止、手機" aria-label="搜尋常見問題" autocomplete="off"><span id="faqCount" role="status" aria-live="polite">共 {total} 題</span></label>
          <p id="faqEmpty" class="faq-empty" hidden role="status">沒有符合的問題，請嘗試其他關鍵字。<a href="#faqSearch" data-faq-filter="">清除篩選</a></p>
          <div class="faq-list">{faq_items}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="content-section" aria-labelledby="systems-heading">
    <div class="wrap">
      <div class="section-intro">
        {eyebrow('產品差異 / 入口')}
        <h2 id="systems-heading">先分清楚工具，再開始操作。</h2>
        <p>MT MATRIX 著重觀察與分析；MT AUTO 著重設定、執行與紀錄。兩者都是外部系統入口，官網不登入、不送單。</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card">
          <div class="feature-copy">
            <div class="product-lockup">{logo()}<span><b>MT MATRIX</b><small>多桌百家輔助</small></span></div>
            <h3>把桌台、牌路與分析放在同一個視線裡。</h3>
            <p>主要整理桌台、牌路、AI 分析與算牌資訊。想先理解觀察流程，可從多桌輔助教學開始。</p>
            <a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>
          </div>
          <div class="feature-media"><p class="product-caption">多桌雷達 · 原尺寸可水平查看</p><div class="radar-scroll">{screen('multitable-radar', 'MT MATRIX 多桌雷達完整介面')}</div>{image_note()}</div>
        </article>
        <article class="feature-card">
          <div class="feature-copy">
            <div class="product-lockup">{logo(True)}<span><b>MT AUTO</b><small>百家自動下注</small></span></div>
            <h3>設定完成，再確認停止條件與執行紀錄。</h3>
            <p>著重配注策略、下注金額、停止條件及執行紀錄。開始前請逐項核對設定，再閱讀自動下注教學。</p>
            <a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>
          </div>
          <div class="feature-media"><p class="product-caption">MT AUTO · 自動下注執行面板</p>{screen('auto-running', 'MT AUTO 自動下注執行面板')}{image_note()}</div>
        </article>
      </div>
    </div>
  </section>

  <section class="cta-section" aria-labelledby="faq-cta-heading">
    <div class="wrap cta-layout">
      <div><p class="eyebrow">需要進一步確認？</p><h2 id="faq-cta-heading">看清產品差異，<br><span>再決定下一步。</span></h2><p class="note">FAQ 只整理常見使用情境；實際平台、帳號授權與程式內限制，以登入後畫面及官方客服回覆為準。分析與配注策略不保證預測下一局或獲利。</p></div>
      <div class="cta-actions">{button('進入 MT MATRIX', MATRIX)}{button('進入 MT AUTO', AUTO, 'outline')}<a class="text-link" href="/contact">前往客服中心 {arrow()}</a></div>
    </div>
  </section>
</div>'''

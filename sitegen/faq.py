from html import escape

from .common import AUTO, DATA, LINE, MATRIX, ambient, arrow, button, chapter, eyebrow, image_note, logo, screen


def _icon_plus():
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'


def _faq_item(index, category, question, answer):
    number = f'{index:02d}'
    return f'''<details class="faq-item" data-faq-category="{escape(category, quote=True)}">
  <summary>
    <span class="faq-page__question-copy"><span class="faq-page__question-number">{number}</span><span class="faq-page__question-text"><small>{escape(category)}</small><b>{escape(question)}</b></span></span>
    {_icon_plus()}
  </summary>
  <p>{escape(answer)}</p>
</details>'''


def render():
    questions = DATA['questions']
    faq_items = ''.join(_faq_item(i, category, question, answer) for i, (category, question, answer) in enumerate(questions, 1))
    total = len(questions)

    return f'''<div class="faq-page">
  <section class="faq-page__hero" aria-labelledby="faq-page-title">
    <div class="faq-page__hero-ambient" aria-hidden="true">{ambient('faq')}</div>
    <div class="wrap faq-page__hero-inner">
      <div class="faq-page__hero-copy">
        {eyebrow('常見問題 / 支援')}
        <p class="faq-page__hero-index"><span>FAQ</span><span>{total} 個常見情境</span></p>
        <h1 id="faq-page-title" class="faq-page__hero-title">常見問題<em>。</em><br/><span>快速找到答案。</span></h1>
        <p class="faq-page__hero-lede">登入、授權與工具使用，先用關鍵字定位。需要協助時，請準備對應畫面、問題描述與目前狀態。</p>
        <div class="faq-page__hero-foot"><span>從使用情境開始</span><a href="#faqSearch">開始搜尋 <span aria-hidden="true">↓</span></a></div>
      </div>
      <nav class="faq-page__index" aria-label="FAQ 快速分類">
        <div class="faq-page__index-heading"><span>問題分類</span><b>快速定位</b></div>
        <a class="faq-page__index-link" href="#faqSearch" data-faq-filter="" aria-current="page"><span>01</span><strong>全部問題</strong><small>顯示完整 {total} 題</small><span aria-hidden="true">↗</span></a>
        <a class="faq-page__index-link" href="#faqSearch" data-faq-filter="使用方式"><span>02</span><strong>使用方式</strong><small>裝置與進入方法</small><span aria-hidden="true">↗</span></a>
        <a class="faq-page__index-link" href="#faqSearch" data-faq-filter="帳號授權"><span>03</span><strong>帳號與登入</strong><small>授權與客服協助</small><span aria-hidden="true">↗</span></a>
        <a class="faq-page__index-link" href="#faqSearch" data-faq-filter="自動下注"><span>04</span><strong>自動下注</strong><small>設定、停止與紀錄</small><span aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </section>

  <section class="faq-page__question-section paper" id="faq" aria-labelledby="faq-page-question-heading">
    <div class="wrap faq-page__question-layout">
      <aside class="faq-page__support">
        {chapter('01', '先找答案。<br/>再開始操作。', '把問題與畫面整理好，客服就能更快確認使用情境。')}
        <div class="faq-page__support-rule" aria-hidden="true"></div>
        <p class="faq-page__support-note">如果是登入或授權問題，請提供會員帳號、問題描述與錯誤畫面；請勿提供密碼。</p>
        {button('聯繫 LINE 客服', LINE, 'dark')}
        <div class="faq-page__support-meta"><span>官方客服</span><span>僅提供必要資訊</span></div>
      </aside>

      <div class="faq-page__faq-main">
        <div class="faq-page__faq-heading">
          <div>
            {eyebrow('搜尋 / 常見問題')}
            <h2 id="faq-page-question-heading">你正在找哪一個答案？</h2>
          </div>
          <p>用關鍵字縮小範圍，或從上方索引切換分類。每題都保留對應的使用情境與限制說明。</p>
        </div>
        <div class="faq-page__search-line">
          <label class="faq-search" for="faqSearch">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="m21 21-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z"/></svg>
            <input id="faqSearch" type="search" placeholder="搜尋問題，例如：登入、停止、手機" aria-label="搜尋常見問題" autocomplete="off" />
          </label>
          <p id="faqCount" role="status" aria-live="polite" data-faq-total="{total}">共 {total} 題</p>
        </div>
        <p id="faqEmpty" hidden role="status">沒有符合的問題，請嘗試其他關鍵字或聯繫客服。</p>
        <div class="faq-page__question-list">
          {faq_items}
        </div>
      </div>
    </div>
  </section>

  <section class="faq-page__systems" aria-labelledby="faq-page-systems-heading">
    <div class="wrap faq-page__systems-head">
      {chapter('02', '兩套系統，<br/>兩種操作節奏。', '先分清楚你要觀察的是多桌資訊，還是要管理策略執行。', 'faq-page-systems-heading')}
    </div>
    <div class="wrap faq-page__system-list">
      <article class="faq-page__system faq-page__system--matrix">
        <div class="faq-page__system-copy">
          <div class="faq-page__product-mark">{logo()}<span><b>MT MATRIX</b><small>多桌百家輔助</small></span></div>
          {eyebrow('01 / 多桌觀察')}
          <h3>把桌台、牌路與分析，放在同一個視線裡。</h3>
          <p>MT MATRIX 主要整理桌台、牌路、AI 分析與算牌資訊。若你想先理解介面與觀察流程，可從多桌輔助教學開始。</p>
          <div class="faq-page__system-actions"><a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>{button('進入 MT MATRIX', MATRIX)}</div>
        </div>
        <div class="faq-page__system-visual">
          {screen('matrix-assist', 'MT MATRIX 百家輔助主面板')}
          {image_note()}
        </div>
      </article>
      <article class="faq-page__system faq-page__system--auto">
        <div class="faq-page__system-copy">
          <div class="faq-page__product-mark">{logo(True)}<span><b>MT AUTO</b><small>百家自動下注</small></span></div>
          {eyebrow('02 / 策略執行')}
          <h3>設定完成，再確認停止條件與執行紀錄。</h3>
          <p>MT AUTO 著重配注策略、下注金額、停止條件及執行紀錄。開始前請逐項核對設定，再閱讀自動下注教學。</p>
          <div class="faq-page__system-actions"><a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>{button('進入 MT AUTO', AUTO)}</div>
        </div>
        <div class="faq-page__system-visual faq-page__system-visual--portrait">
          {screen('auto-running', 'MT AUTO 自動下注執行面板')}
          {image_note()}
        </div>
      </article>
    </div>
  </section>

  <section class="faq-page__closing paper" aria-label="客服與風險提醒">
    <div class="wrap faq-page__closing-inner">
      <p class="faq-page__closing-label">需要進一步確認？</p>
      <p>FAQ 只整理常見使用情境；實際平台、帳號授權與程式內限制，請以登入後畫面及官方客服回覆為準。分析與配注策略不保證預測下一局或獲利。</p>
      <a class="text-link" href="/contact">前往客服中心 {arrow()}</a>
    </div>
  </section>
</div>'''

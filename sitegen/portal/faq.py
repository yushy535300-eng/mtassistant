from html import escape

from ..common import DATA, MATRIX, AUTO, LINE, button, arrow


def _categories(questions):
    return list(dict.fromkeys(category for category, _, _ in questions))


def _filter_links(categories, total):
    links = [
        f'<a class="faq-filter" href="#faqSearch" data-faq-filter="" aria-current="true"><span>全部</span><small>{total} 題</small></a>'
    ]
    links.extend(
        f'<a class="faq-filter" href="#faqSearch" data-faq-filter="{escape(category, quote=True)}" aria-current="false"><span>{escape(category)}</span></a>'
        for category in categories
    )
    return ''.join(links)


def _faq_item(index, category, question, answer):
    return f'''<details class="faq-item" data-faq-category="{escape(category, quote=True)}">
  <summary><span class="faq-number">{index:02d}</span><span class="faq-question"><small>{escape(category)}</small><b>{escape(question)}</b></span></summary>
  <div><p>{escape(answer)}</p></div>
</details>'''


def render():
    questions = DATA['questions']
    categories = _categories(questions)
    total = len(questions)
    faq_items = ''.join(
        _faq_item(index, category, question, answer)
        for index, (category, question, answer) in enumerate(questions, 1)
    )

    return f'''<section class="portal-pagehead" aria-labelledby="faq-title">
  <div>
    <p class="kicker">支援 / 常見問題</p>
    <h1 id="faq-title">常見問題</h1>
    <p>查詢兩套工具的使用方式、登入授權與操作限制；用關鍵字或分類快速找到對應說明。</p>
  </div>
  <div class="pagehead-actions">
    {button('進入 MT MATRIX', MATRIX)}
    {button('進入 MT AUTO', AUTO, 'outline')}
  </div>
</section>

<section class="portal-section" id="faq" aria-labelledby="faq-heading">
  <div class="section-top">
    <div>
      <h2 id="faq-heading">搜尋問題</h2>
      <p>輸入登入、手機、停止等關鍵字，或按分類查看八題常見問答。</p>
    </div>
  </div>
  <div class="portal-panel">
    <div class="faq-toolbar">
      <label for="faqSearch">搜尋常見問題</label>
      <input id="faqSearch" type="search" placeholder="例如：登入、停止、手機" aria-label="搜尋常見問題" autocomplete="off">
      <p id="faqCount" role="status" aria-live="polite">共 {total} 題</p>
    </div>
    <nav class="inline-actions faq-filters" aria-label="FAQ 問題分類">
      {_filter_links(categories, total)}
    </nav>
    <p id="faqEmpty" class="portal-notice" hidden role="status">沒有符合的問題。<a class="text-link" href="#faqSearch" data-faq-filter="">清除搜尋與分類 {arrow()}</a></p>
    <div class="faq-list">
      {faq_items}
    </div>
  </div>
</section>

<section class="portal-section" aria-labelledby="support-heading">
  <div class="section-top">
    <div>
      <h2 id="support-heading">需要登入或授權協助？</h2>
      <p>請讓客服知道系統與問題畫面，方便確認目前狀態。</p>
    </div>
  </div>
  <div class="portal-panel two-column">
    <ul class="feature-list">
      <li><strong>聯繫前準備</strong><p>提供會員帳號、問題描述與錯誤畫面。</p></li>
      <li><strong>請勿提供密碼</strong><p>客服不需要你的登入密碼。</p></li>
    </ul>
    <div class="inline-actions">
      {button('聯繫 LINE 客服', LINE)}
      <a class="text-link" href="/contact">查看客服中心 {arrow()}</a>
    </div>
  </div>
</section>

<div class="action-strip" aria-label="下一步">
  <p>想先了解操作流程？</p>
  <div class="inline-actions">
    <a class="text-link" href="/guide?system=matrix">閱讀多桌輔助教學 {arrow()}</a>
    <a class="text-link" href="/guide?system=auto">閱讀自動下注教學 {arrow()}</a>
  </div>
</div>'''

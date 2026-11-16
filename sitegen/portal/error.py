from ..common import button


def render():
    return f'''<section class="portal-pagehead"><div><p class="kicker">404 / 找不到頁面</p><h1>這個網址暫時找不到。</h1><p>請確認網址，或從導航繼續查看工具與操作教學。</p></div><div class="pagehead-actions">{button('返回首頁', '/')}{button('聯繫客服', '/contact', 'outline')}</div></section>'''

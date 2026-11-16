from ..common import button, eyebrow


def render():
    return f'''<section class="page-hero"><div class="wrap hero-layout"><div class="hero-copy">{eyebrow('404 · 找不到頁面')}<h1>這個頁面，<br><span>暫時找不到。</span></h1><p>請確認網址，或返回首頁選擇產品、操作教學與客服入口。</p><div class="hero-actions">{button('返回首頁', '/', 'light')}{button('聯繫客服', '/contact', 'outline-light')}</div></div></div></section>'''

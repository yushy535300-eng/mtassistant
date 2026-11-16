from .common import button, eyebrow


def render():
    return f'''<section class="error-page section paper"><div class="wrap error-layout"><div>{eyebrow('PAGE NOT FOUND / 404')}<h1>這一頁，<br>暫時不在這裡。</h1><p>請確認網址，或回到首頁選擇你要了解的工具。<br>如果原連結無法開啟，可以把網址提供給客服協助。</p><div class="hero-actions">{button('返回首頁', '/')}{button('聯繫客服', '/contact', 'text')}</div></div><span class="error-number" aria-hidden="true">404</span></div></section>'''

"""Check incremental changes on the approved visual base; never call external games or LINE."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:3000'
LINE = 'https://line.me/ti/p/k2pkYGXGL3'
results = []

def check(name, condition, evidence=None):
    results.append({'name': name, 'passed': bool(condition), 'evidence': evidence})

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = browser.new_context()
    context.add_init_script("sessionStorage.setItem('yuceEntrySeen:premium-v3','true')")
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    routes = ['/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact']
    for width, height in [(360,740),(390,844),(440,956),(768,1024),(1440,900)]:
        page.set_viewport_size({'width':width,'height':height})
        for route in routes:
            page.goto(BASE + route, wait_until='networkidle')
            page.wait_for_timeout(100)
            values = page.evaluate("""() => ({overflow:document.documentElement.scrollWidth > innerWidth+1,
              accent:getComputedStyle(document.documentElement).getPropertyValue('--accent').trim(),
              rail:!!document.querySelector('.portal-rail'),
              links:[...document.querySelectorAll('[data-line-link]')].map(a=>({href:a.href,target:a.target,rel:a.rel})),
              buttons:[...document.querySelectorAll('.button,.menu-toggle,.header-motion,.faq-filter,.launch-menu>summary')]
                .filter(e=>e.getClientRects().length && getComputedStyle(e).visibility!=='hidden')
                .map(e=>({text:e.textContent.trim()||e.getAttribute('aria-label'),height:e.getBoundingClientRect().height}))})""")
            check(f'{route}@{width}: no horizontal overflow', not values['overflow'])
            check(f'{route}@{width}: original rose theme and sidebar', values['accent']=='#d52369' and values['rail'])
            check(f'{route}@{width}: LINE correct/safe', len(values['links']) >= 4 and all(a['href']==LINE and a['target']=='_blank' and 'noopener' in a['rel'] for a in values['links']))
            small = [b for b in values['buttons'] if b['height'] < 43.5 or not b['text']]
            check(f'{route}@{width}: visible buttons named and >=44px', not small, small)
            if width <= 640:
                line = page.locator('.portal-bottom [data-line-link]')
                check(f'{route}@{width}: persistent mobile LINE visible', line.is_visible())
        page.goto(BASE + '/', wait_until='networkidle')
        check(f'home@{width}: original table art', '5IpvgHPwOi5uABZyAx9lXZ' in (page.locator('.banner-art img').get_attribute('src') or ''))
        if width <= 640:
            entries = page.locator('.portal-direct-tools a')
            boxes = [a.bounding_box() for a in entries.all()]
            check(f'home@{width}: both tool links first screen', entries.count()==2 and all(box is not None and box['y'] + box['height'] < height-65 for box in boxes))
    page.set_viewport_size({'width':390,'height':844})
    page.goto(BASE + '/guide?system=matrix', wait_until='networkidle')
    check('matrix all five original steps visible', page.locator('article.guide-step-panel:visible').count()==5)
    page.locator('#matrix-step1 .refine-next').click()
    page.wait_for_function("document.querySelector('[data-guide-panel=matrix]').dataset.currentStep === '2'", timeout=4000)
    check('matrix next/hash/progress', page.url.endswith('#matrix-step2') and page.locator('[data-guide-panel="matrix"]').get_attribute('data-current-step')=='2')
    page.goto(BASE + '/guide?system=auto', wait_until='networkidle')
    check('auto all six original steps visible', page.locator('article.guide-step-panel:visible').count()==6)
    page.goto(BASE + '/contact', wait_until='networkidle')
    check('mobile QR collapsed, direct LINE first', not page.locator('.refine-qr').evaluate('e=>e.open') and page.locator('.pagehead-actions [data-line-link]').is_visible())
    page.goto(BASE + '/faq', wait_until='networkidle')
    page.locator('#faqSearch').fill('xxxxx-no-result')
    page.wait_for_timeout(120)
    check('FAQ empty search still works', page.locator('#faqEmpty').is_visible())
    page.locator('#faqSearch').fill('')
    check('FAQ all eight answers retained', page.locator('.faq-item[data-faq-category]').count()==8)
    check('no JS exceptions on base layouts', not errors, errors)
    context.close()
    for width,height in [(360,740),(390,844),(1440,900),(844,390)]:
        ctx=browser.new_context(viewport={'width':width,'height':height})
        pg=ctx.new_page()
        pg.goto(BASE+'/',wait_until='networkidle');pg.wait_for_timeout(650)
        modal=pg.locator('#welcomeDialog')
        check(f'entry@{width}x{height}: automatically opens',modal.evaluate('e=>e.open'))
        box=modal.bounding_box()
        check(f'entry@{width}x{height}: within viewport', bool(box) and box['x'] >= 0 and box['y'] >= 0 and box['x']+box['width'] <= width+1 and box['y']+box['height'] <= height+1)
        check(f'entry@{width}x{height}: green LINE CTA clear', pg.locator('.welcome-line').evaluate("e=>e.getBoundingClientRect().height>=49 && getComputedStyle(e).backgroundColor==='rgb(8, 124, 60)'"))
        pg.keyboard.press('Escape')
        pg.wait_for_function("!document.getElementById('welcomeDialog').open && !document.body.classList.contains('welcome-open')", timeout=2000)
        check(f'entry@{width}x{height}: ESC dismisses and unlocks',not modal.evaluate('e=>e.open') and not pg.locator('body').evaluate("e=>e.classList.contains('welcome-open')"))
        pg.goto(BASE+'/features',wait_until='networkidle');pg.wait_for_timeout(650)
        check(f'entry@{width}x{height}: not repeated per internal page',not pg.locator('#welcomeDialog').evaluate('e=>e.open'))
        pg.goto(BASE+'/?welcome=1',wait_until='networkidle');pg.wait_for_timeout(650)
        pg.locator('.welcome-browse').click()
        check(f'entry@{width}x{height}: browse dismisses', not pg.locator('#welcomeDialog').evaluate('e=>e.open'))
        ctx.close()
    browser.close()
output=ROOT/'docs/preserve-audit.json'
output.write_text(json.dumps({'checks':results,'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results)},ensure_ascii=False,indent=2)+'\n')
failures=[r for r in results if not r['passed']]
print(json.dumps({'total':len(results),'failures':failures},ensure_ascii=False,indent=2))
if failures:raise SystemExit(1)

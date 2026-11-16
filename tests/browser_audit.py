"""Read-only Playwright checks against the isolated site, never product accounts."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get('TEST_ORIGIN', 'http://127.0.0.1:3000').rstrip('/')
ROUTES = ['/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact']
SIZES = [(360,800),(390,844),(393,852),(430,932),(440,956),(768,1024),(1280,800),(1440,900),(1920,1080),(2560,1440)]
results = {'origin':BASE,'layouts':[],'interactions':[],'errors':[], 'webkit':{}}

def check(name, condition, detail=''):
    results['interactions'].append({'name':name, 'passed':bool(condition), 'detail':detail})
    if not condition: results['errors'].append(name + ': ' + detail)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width,height in SIZES:
        context = browser.new_context(viewport={'width':width,'height':height}, device_scale_factor=1)
        page = context.new_page()
        console = []
        page.on('pageerror', lambda error: console.append(str(error)))
        for route in ROUTES:
            response = page.goto(BASE + route, wait_until='networkidle')
            page.wait_for_timeout(250)
            metrics = page.evaluate('''() => ({ width:innerWidth, documentWidth:document.documentElement.scrollWidth, bodyWidth:document.body.scrollWidth, h1:document.querySelectorAll('h1').length, badImages:[...document.images].filter(i=>i.getAttribute('src')&&i.loading!=='lazy'&&(!i.complete||!i.naturalWidth)).map(i=>i.getAttribute('src')), horizontal:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.left<innerWidth&&(r.right>innerWidth+2||r.left<-2)&&!e.closest('.radar-scroll, .mx-radar-scroll, .mx-radar-panorama, .guide-radar-scroll, .guide-screen-scroll, .guide-screen-multitable-radar')}).slice(0,8).map(e=>({tag:e.tagName,cls:e.className,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right})) })''')
            passed = response is not None and response.status == 200 and metrics['documentWidth'] <= width + 2 and metrics['bodyWidth'] <= width + 2 and metrics['h1'] == 1 and not metrics['badImages']
            results['layouts'].append({'route':route,'viewport':[width,height],'passed':passed,'metrics':metrics})
            if not passed: results['errors'].append(f'Layout {width} {route}: {metrics}')
        if console: results['errors'] += [f'JS {width}: ' + e for e in console]
        context.close()
    context = browser.new_context(viewport={'width':390,'height':844})
    page = context.new_page()
    page.goto(BASE, wait_until='networkidle')
    page.locator('#menuToggle').click()
    check('Mobile menu opens', page.locator('#mobileNav').is_visible() and page.locator('#menuToggle').get_attribute('aria-expanded') == 'true')
    page.keyboard.press('Escape')
    check('Mobile menu Escape closes', not page.locator('#mobileNav').is_visible())
    page.locator('[data-tab=parity]').click()
    check('Home actual product screen switches', page.locator('#focus-parity').is_visible() and not page.locator('#focus-cards').is_visible())
    page.keyboard.press('Home')
    check('Product tabs support keyboard Home', page.locator('#focus-cards').is_visible())
    page.locator('#focus-cards [data-image]').click()
    check('Full-size product dialog opens', page.locator('#imageViewer').is_visible() and (page.locator('#viewerImage').get_attribute('src') or '').endswith('four-formulas.png'))
    page.keyboard.press('Escape')
    check('Dialog Escape restores focus', not page.locator('#imageViewer').is_visible() and page.evaluate("document.activeElement.matches('#focus-cards [data-image]')"))
    page.goto(BASE + '/guide?system=auto', wait_until='networkidle')
    check('AUTO query selects AUTO tutorial', page.locator('#guide-panel-auto').is_visible() and not page.locator('#guide-panel-matrix').is_visible())
    page.locator('#guide-tab-matrix').click()
    check('Tutorial tab updates query and content', 'system=matrix' in page.url and page.locator('#guide-panel-matrix').is_visible())
    page.keyboard.press('ArrowRight')
    check('Tutorial keyboard switching', 'system=auto' in page.url and page.locator('#guide-panel-auto').is_visible())
    page.goto(BASE + '/guide?system=matrix#auto-step6', wait_until='networkidle')
    check('Cross-system tutorial hash selects correct panel', page.locator('#guide-panel-auto').is_visible() and page.locator('#auto-step6').is_visible())
    page.goto(BASE + '/faq', wait_until='networkidle')
    check('FAQ initially retains eight questions', page.locator('details.faq-item:visible').count() == 8)
    page.locator('[data-faq-filter="帳號授權"]').first.click()
    matches = page.locator('details.faq-item:visible').all_text_contents()
    check('FAQ account authorization filter', len(matches) == 1 and all('登入' in text for text in matches), 'Original DATA contains one account-authorization question')
    page.locator('#faqSearch').fill('不存在的測試詞abcxyz')
    check('FAQ empty state', page.locator('#faqEmpty').is_visible() and page.locator('details.faq-item:visible').count() == 0)
    page.locator('[data-faq-filter=""]').first.click()
    check('FAQ clear returns all questions', page.locator('details.faq-item:visible').count() == 8)
    if page.locator('details.faq-item').first.get_attribute('open') is not None:
        page.locator('details.faq-item').first.locator('summary').click()
    page.locator('details.faq-item').first.locator('summary').click()
    check('FAQ native details expands', page.locator('details.faq-item').first.get_attribute('open') is not None)
    context.close()
    context = browser.new_context(viewport={'width':390,'height':844}, java_script_enabled=False)
    page = context.new_page()
    page.goto(BASE + '/guide?system=auto', wait_until='networkidle')
    check('No-JS both complete tutorials readable', page.locator('#guide-panel-matrix').is_visible() and page.locator('#guide-panel-auto').is_visible() and page.locator('details[id^="matrix-step"]').count() == 5 and page.locator('details[id^="auto-step"]').count() == 6)
    page.goto(BASE, wait_until='networkidle')
    check('No-JS original full-size image link', (page.locator('[data-image]').first.get_attribute('href') or '').endswith('.png'))
    context.close()
    context = browser.new_context(viewport={'width':390,'height':844}, reduced_motion='reduce')
    page = context.new_page(); page.goto(BASE, wait_until='networkidle')
    check('Reduced motion content not hidden', not page.locator('body').evaluate("e=>e.classList.contains('motion-ready')") and page.locator('.banner-copy').is_visible())
    context.close()
    context = browser.new_context(viewport={'width':393,'height':852}, is_mobile=True, has_touch=True)
    page = context.new_page(); page.goto(BASE, wait_until='networkidle')
    page.locator('#menuToggle').tap()
    check('Touch menu opens', page.locator('#mobileNav').is_visible())
    page.set_viewport_size({'width':852,'height':393})
    check('Landscape orientation has no page overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'))
    page.set_viewport_size({'width':393,'height':852})
    check('Portrait orientation restores without overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'))
    context.close(); browser.close()
    try:
        webkit = p.webkit.launch(headless=True)
        context = webkit.new_context(viewport={'width':390,'height':844})
        page = context.new_page(); checked = []
        for route in ROUTES:
            response = page.goto(BASE + route, wait_until='networkidle')
            ok = response is not None and response.status == 200 and page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2')
            checked.append({'route':route,'passed':ok})
        results['webkit'] = {'available':True,'pages':checked,'note':'Headless WebKit simulation, not iOS Safari physical hardware.'}
        context.close(); webkit.close()
    except Exception as error:
        results['webkit'] = {'available':False,'note':'Headless WebKit unavailable: ' + str(error).splitlines()[0]}
results['passed'] = not results['errors']
(ROOT / 'docs/browser-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2) + '\n')
print(json.dumps({'layouts':len(results['layouts']),'interactions':results['interactions'],'errors':results['errors'],'webkit':results['webkit'],'passed':results['passed']},ensure_ascii=False,indent=2))
raise SystemExit(0 if results['passed'] else 1)

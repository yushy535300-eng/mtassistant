"""Current-version checks, read-only; never enter external product accounts."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = 'http://127.0.0.1:3000'
rows = []
errors = []


def check(name, passed, detail=None):
    rows.append({'name': name, 'passed': bool(passed), 'detail': detail})
    if not passed:
        errors.append(name)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width, height in [(360,800),(390,844),(393,852),(430,932),(440,956),(768,1024),(1440,900)]:
        context = browser.new_context(viewport={'width':width,'height':height})
        page = context.new_page()
        page.goto(BASE, wait_until='networkidle')
        geometry = page.locator('.choice-actions .button').evaluate_all('els=>els.map(e=>({bottom:e.getBoundingClientRect().bottom,height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width}))')
        bottom = page.locator('.portal-bottom').evaluate('e=>getComputedStyle(e).display==="none"?innerHeight:e.getBoundingClientRect().top')
        check(f'{width}: both primary tool entries above fold', len(geometry) == 2 and all(e['bottom'] <= bottom and e['height'] >= 44 for e in geometry), geometry)
        check(f'{width}: no old sidebar or category navigation', page.locator('.portal-rail,.portal-category,.portal-shortcuts').count() == 0)
        check(f'{width}: one visible primary navigation', page.locator('.desktop-nav:visible,.portal-bottom:visible').count() == 1)
        check(f'{width}: no horizontal overflow', page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'))
        context.close()

    context = browser.new_context(viewport={'width':390,'height':844})
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE, wait_until='networkidle')
    page.locator('[data-tab="auto-limits"]').click()
    check('AUTO panel switches independently', page.locator('#focus-auto-limits').is_visible() and page.locator('#focus-cards').is_visible())
    page.locator('[data-tab="parity"]').click()
    check('MATRIX panel switches without changing AUTO', page.locator('#focus-parity').is_visible() and page.locator('#focus-auto-limits').is_visible())
    page.keyboard.press('Home')
    check('Keyboard Home stays within the current tab group', page.locator('#focus-cards').is_visible() and page.locator('#focus-auto-limits').is_visible())
    page.goto(BASE + '/guide?system=matrix#auto-step6', wait_until='networkidle')
    check('Cross-system deep link opens target details', page.locator('#guide-panel-auto').is_visible() and page.locator('#auto-step6').get_attribute('open') is not None)
    check('Deep link synchronizes progress', page.locator('#guide-panel-auto').get_attribute('data-current-step') == '6')
    page.goto(BASE + '/guide?system=matrix', wait_until='networkidle')
    page.locator('#matrix-step1 [data-next-step]').click()
    check('Next step opens target and closes previous on phone', page.locator('#matrix-step2').get_attribute('open') is not None and page.locator('#matrix-step1').get_attribute('open') is None)
    check('Next step updates progress', page.locator('#guide-panel-matrix').get_attribute('data-current-step') == '2')
    page.goto(BASE + '/contact', wait_until='networkidle')
    check('Phone QR initially collapsed', page.locator('.qr-disclosure').get_attribute('open') is None)
    page.locator('.qr-disclosure > summary').click()
    check('Phone can request QR when needed', page.locator('.qr-disclosure img').is_visible())
    check('Direct LINE remains available before QR', page.locator('.pagehead-actions a[href^="https://line.me/"]').count() == 1)
    page.goto(BASE + '/contact#contact-prep', wait_until='networkidle')
    check('Contact preparation deep link opens disclosure', page.locator('#contact-prep').get_attribute('open') is not None)
    page.goto(BASE, wait_until='networkidle')
    page.locator('#menuToggle').click()
    check('Menu moves keyboard focus into visible navigation', page.evaluate('document.getElementById("mobileNav").contains(document.activeElement)'))
    page.keyboard.press('Escape')
    check('Menu Escape restores toggle focus', page.evaluate('document.activeElement.id==="menuToggle"'))
    before = int(page.locator('.portal-banner').get_attribute('data-motion-frames') or '0')
    page.wait_for_timeout(600)
    after = int(page.locator('.portal-banner').get_attribute('data-motion-frames') or '0')
    check('Visible depth stars actually animate', after > before)
    page.locator('#motionToggle').click()
    before = page.locator('.portal-banner').get_attribute('data-motion-frames')
    page.wait_for_timeout(400)
    check('Manual pause stops renderer', before == page.locator('.portal-banner').get_attribute('data-motion-frames'))
    page.locator('#motionToggle').click()
    page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
    page.wait_for_timeout(200)
    before = page.locator('.portal-banner').get_attribute('data-motion-frames')
    page.wait_for_timeout(400)
    check('Offscreen stage stops renderer and CSS light', before == page.locator('.portal-banner').get_attribute('data-motion-frames') and page.locator('.portal-banner').evaluate('e=>e.classList.contains("stage-offscreen")'))
    context.close()
    context = browser.new_context(viewport={'width':390,'height':844}, reduced_motion='reduce')
    page = context.new_page(); page.goto(BASE, wait_until='networkidle')
    before = page.locator('.portal-banner').get_attribute('data-motion-frames')
    page.wait_for_timeout(400)
    check('Reduced motion stops decorative animation', before == page.locator('.portal-banner').get_attribute('data-motion-frames') and page.locator('body').evaluate('e=>e.classList.contains("motion-paused")'))
    context.close()
    context = browser.new_context(viewport={'width':390,'height':844}, java_script_enabled=False)
    page = context.new_page(); page.goto(BASE + '/guide?system=auto', wait_until='networkidle')
    check('No JS keeps all original expandable steps', page.locator('details[data-guide-step]').count() == 11)
    page.locator('#auto-step2 > summary').click()
    check('No JS native tutorial expansion remains usable', page.locator('#auto-step2').get_attribute('open') is not None)
    context.close(); browser.close()
result = {'checks':rows,'errors':errors,'passed':not errors,'note':'Headless browser evidence, not physical iOS/Android certification or a design score.'}
(ROOT/'docs/polish-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['passed'] else 1)

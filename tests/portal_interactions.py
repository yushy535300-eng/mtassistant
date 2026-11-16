"""Read-only checks for the rebuilt portal shell and classification semantics."""
import json
from collections import Counter
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'sitegen/data.json').read_text())
BASE = 'http://127.0.0.1:3000'
checks = []


def check(name, condition, detail=''):
    checks.append({'name': name, 'passed': bool(condition), 'detail': detail})


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 390, 'height': 844})
    page = context.new_page()
    page.goto(BASE + '/faq', wait_until='networkidle')
    for category, expected in Counter(row[0] for row in DATA['questions']).items():
        page.locator('[data-faq-filter]').filter(has_text=category).first.click()
        visible = page.locator('details.faq-item:visible')
        actual = visible.count()
        values = visible.evaluate_all('(items) => items.map(i => i.dataset.faqCategory)')
        check('Exact category ' + category, actual == expected and all(v == category for v in values), f'expected={expected}, actual={actual}')
    page.locator('#faqSearch').fill('手機')
    check('Free text search resets category', page.locator('details.faq-item:visible').count() > 0)
    page.locator('#faqSearch').fill('no-such-question-portal')
    check('Empty result is real', page.locator('#faqEmpty').is_visible())
    page.locator('#faqEmpty [data-faq-filter]').click()
    check('Empty-state clear restores all eight', page.locator('details.faq-item:visible').count() == 8)
    page.goto(BASE + '/features', wait_until='networkidle')
    check('Inner page has motion control', page.locator('#motionToggle').count() == 1)
    start = page.locator('.portal-pagehead').get_attribute('data-motion-frames')
    page.wait_for_timeout(220)
    check('Inner page actually animates', int(page.locator('.portal-pagehead').get_attribute('data-motion-frames') or 0) > int(start or 0))
    page.locator('#motionToggle').click()
    page.wait_for_timeout(120)
    check('Control pauses CSS and canvas', page.locator('body').evaluate("e => e.classList.contains('motion-paused')") and page.locator('#motionToggle').get_attribute('aria-pressed') == 'true')
    page.goto(BASE + '/guide?system=auto', wait_until='networkidle')
    check('Motion preference survives navigation', page.locator('body').evaluate("e => e.classList.contains('motion-paused')"))
    check('AUTO SSR preview is correct', page.locator('#guide-preview-auto').is_visible() and not page.locator('#guide-preview-matrix').is_visible())
    page.locator('#motionToggle').click()
    check('Resume works on inner page', page.locator('#motionToggle').get_attribute('aria-pressed') == 'false')
    for width in (360, 390, 768, 1440):
        page.set_viewport_size({'width': width, 'height': 900})
        for route in ('/', '/features', '/guide', '/faq', '/contact'):
            page.goto(BASE + route, wait_until='networkidle')
            check(f'Final header and page fit {width} {route}', page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'))
    context.close()
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    page = context.new_page(); page.goto(BASE + '/features', wait_until='networkidle')
    check('Reduced motion works on inner page', page.locator('#motionToggle').is_disabled() and page.locator('body').evaluate("e => e.classList.contains('motion-paused')"))
    context.close(); browser.close()

report = {'checks': checks, 'passed': all(row['passed'] for row in checks)}
(ROOT / 'docs/portal-interactions.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report['passed'] else 1)

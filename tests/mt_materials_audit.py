"""Focused current-source checks; never opens external game or messaging URLs."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'http://127.0.0.1:3000'
THREADS = 'https://www.threads.com/@hacklook__?igshid=NTc4MTIwNjQ2YQ=='
RESULTS = []


def check(name, value):
    RESULTS.append({'check': name, 'passed': bool(value)})
    if not value:
        print('FAIL:', name)


def bounds(locator):
    value = locator.bounding_box()
    if value is None:
        raise AssertionError('Expected a visible element')
    return value


def main():
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.add_init_script("sessionStorage.setItem('portalMotionPaused','true')")
        for route in ('/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact'):
            suffix = '&' if '?' in route else '?'
            page.goto(ORIGIN + route + suffix + 'welcome=0', wait_until='networkidle')
            check(f'{route}: header motion control removed', page.locator('#motionToggle').count() == 0)
            links = page.locator('a[data-threads-link]')
            check(f'{route}: current Threads link present', links.count() >= 1)
            check(f'{route}: Threads safe new tab', all(link.get_attribute('href') == THREADS and link.get_attribute('target') == '_blank' and 'noopener' in (link.get_attribute('rel') or '') for link in links.all()))
            check(f'{route}: old account absent', 'uss0857' not in page.content())
        for width, height in ((360,780),(390,844),(440,896),(768,1024),(1440,900)):
            page.set_viewport_size({'width': width, 'height': height})
            for route in ('/', '/features', '/auto'):
                page.goto(ORIGIN + route + '?welcome=0', wait_until='networkidle')
                check(f'{route} {width}px: no page overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'))
                check(f'{route} {width}px: no pause control', page.locator('#motionToggle').count() == 0)
                if route == '/':
                    cards = page.locator('.tool-tile')
                    check(f'{width}px: two independent product cards', cards.count() == 2)
                    for index, key in enumerate(('MATRIX','AUTO')):
                        primary = cards.nth(index).locator('.inline-actions a').nth(0)
                        secondary = cards.nth(index).locator('.inline-actions a').nth(1)
                        check(f'{width}px {key}: enter is main button', primary.inner_text().strip() == '進入系統' and 'button' in (primary.get_attribute('class') or ''))
                        check(f'{width}px {key}: learn is secondary', 'text-link' in (secondary.get_attribute('class') or '') and primary.get_attribute('href') != secondary.get_attribute('href'))
                        check(f'{width}px {key}: primary touch size', bounds(primary)['height'] >= 44)
                    check(f'{width}px: six different portraits', page.locator('.mt-gallery-item').count() == 6)
                    track = page.locator('#mt-gallery-track')
                    track.scroll_into_view_if_needed()
                    controls = page.locator('[data-gallery-direction]')
                    check(f'{width}px: gallery control touch size', all(bounds(item)['height'] >= 44 and bounds(item)['width'] >= 44 for item in controls.all()))
                    before = track.evaluate('(element) => element.scrollLeft')
                    page.locator('[data-gallery-direction="1"]').click()
                    page.wait_for_function('document.querySelector("#mt-gallery-track").scrollLeft > 2')
                    check(f'{width}px: next moves portraits', track.evaluate('(element) => element.scrollLeft') > before)
                    picture = page.locator('.mt-gallery-item .mt-portrait').nth(3)
                    picture.scroll_into_view_if_needed()
                    picture.click()
                    check(f'{width}px: portrait opens original viewer', page.locator('#imageViewer').evaluate('(element)=>element.open'))
                    page.locator('#viewerClose').click()
                else:
                    image = page.locator('.mt-spotlight img')
                    image.scroll_into_view_if_needed()
                    page.wait_for_function('document.querySelector(".mt-spotlight img").complete')
                    check(f'{route} {width}px: portrait available', image.evaluate('(image) => image.naturalWidth > 0 && image.naturalWidth <= 626'))
                    box = bounds(image)
                    check(f'{route} {width}px: complete square ratio', abs(box['width'] - box['height']) <= 1)
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(ORIGIN + '/?welcome=0', wait_until='networkidle')
        stage = page.locator('.portal-banner')
        first = stage.get_attribute('data-motion-frames') or '0'
        page.wait_for_timeout(500)
        check('stale paused session does not stop current background', int(stage.get_attribute('data-motion-frames') or '0') > int(first))
        page.emulate_media(reduced_motion='reduce')
        page.wait_for_timeout(150)
        stopped = stage.get_attribute('data-motion-frames') or '0'
        page.wait_for_timeout(350)
        check('system reduced motion retained', page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches') and (stage.get_attribute('data-motion-frames') or '0') == stopped)
        page.emulate_media(reduced_motion='no-preference')
        page.goto(ORIGIN + '/?welcome=1', wait_until='networkidle')
        page.wait_for_selector('#welcomeDialog[open]')
        check('premium welcome still works', page.locator('#welcomeDialog[open]').count() == 1)
        page.keyboard.press('Escape')
        check('welcome closes normally', page.locator('#welcomeDialog[open]').count() == 0)
        check('no runtime JS errors', len(errors) == 0)
        browser.close()
    result = {'checks': RESULTS, 'passed': sum(item['passed'] for item in RESULTS), 'total': len(RESULTS)}
    (ROOT / 'docs/mt-materials-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"{result['passed']}/{result['total']} focused checks passed")
    if result['passed'] != result['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

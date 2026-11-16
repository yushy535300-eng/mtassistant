"""Current V3 reading, natural-star, pause and reduced-motion evidence."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--enable-unsafe-swiftshader'])
    for width, height in [(390, 844), (1440, 900)]:
        context = browser.new_context(viewport={'width': width, 'height': height})
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for route in ['/', '/features', '/auto', '/guide?system=auto', '/faq', '/contact']:
            page.goto('http://127.0.0.1:3000' + route, wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            result = page.evaluate('''() => ({
              h1: getComputedStyle(document.querySelector('h1')).color,
              font: getComputedStyle(document.body).fontFamily,
              bodyWidth: document.documentElement.scrollWidth,
              bodyText:[...document.querySelectorAll('main p')].filter(e=>e.offsetParent&&e.textContent.trim()&&!e.matches('.eyebrow,.note,.image-note,.asset-caption,.small-note,.hero-devices,.hero-kicker,.product-caption')).map(e=>({text:e.textContent.trim().slice(0,36),size:parseFloat(getComputedStyle(e).fontSize),opacity:getComputedStyle(e).opacity})),
              scene:document.getElementById('skyStage').dataset.renderer,
              naturalFonts:document.fonts.check('17px YuceTC')
            })''')
            assert result['bodyWidth'] <= width + 2
            assert result['naturalFonts'] and 'YuceTC' in result['font']
            assert result['h1'] == 'rgb(245, 248, 252)'
            assert all(r['opacity'] == '1' for r in result['bodyText'])
            rows.append({'route': route, 'viewport': [width, height], **result})
        page.goto('http://127.0.0.1:3000/', wait_until='networkidle')
        page.wait_for_function('document.getElementById("skyStage").classList.contains("sky-ready")')
        first = int(page.locator('#skyStage').get_attribute('data-frames') or '0')
        page.wait_for_timeout(1300)
        second = int(page.locator('#skyStage').get_attribute('data-frames') or '0')
        assert second > first
        page.locator('#motionToggle').click()
        paused = page.locator('#skyStage').get_attribute('data-frames')
        page.wait_for_timeout(400)
        assert paused == page.locator('#skyStage').get_attribute('data-frames')
        page.locator('#motionToggle').click()
        assert page.locator('#skyStage').get_attribute('data-motion') == 'running'
        assert not errors
        context.close()
    context = browser.new_context(viewport={'width':390, 'height':844}, reduced_motion='reduce')
    page = context.new_page(); page.goto('http://127.0.0.1:3000/', wait_until='networkidle')
    assert page.locator('#skyStage').get_attribute('data-motion') == 'static'
    assert page.locator('#motionToggle').is_hidden()
    context.close(); browser.close()
code = (ROOT / 'public/sky.js').read_text()
assert 'createRadialGradient' not in code and 'strokeStyle' not in code and 'star.depth' not in code
assert "[.7,3.6,10.5]" in code
report = {'reading':rows, 'three_natural_star_layers':True, 'no_crosses_halos_or_radius_pulsing':True, 'pause_resume':True, 'reduced_motion':True, 'passed':True}
(ROOT / 'docs/v3-reading.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('V3: 12 reading states, self-hosted Chinese font, natural-star layers, motion/pause/reduce passed.')

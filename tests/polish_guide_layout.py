"""Only the two tutorial routes affected by the final mobile summary layout."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
rows = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width,height in [(360,800),(390,844),(393,852),(430,932),(440,956),(768,1024),(1280,800),(1440,900),(1920,1080),(2560,1440)]:
        page = browser.new_page(viewport={'width':width,'height':height})
        for system,count in [('matrix',5),('auto',6)]:
            page.goto(f'http://127.0.0.1:3000/guide?system={system}',wait_until='networkidle')
            panel = page.locator('#guide-panel-' + system)
            metrics = page.evaluate('({width:innerWidth,documentWidth:document.documentElement.scrollWidth})')
            passed = metrics['documentWidth'] <= width + 2 and panel.is_visible() and panel.locator('details[data-guide-step]').count() == count
            rows.append({'system':system,'viewport':[width,height],'passed':passed,'metrics':metrics})
        page.close()
    browser.close()
result = {'layouts':rows,'passed':all(r['passed'] for r in rows),'note':'Final summary grid only; unchanged home/product/FAQ/contact checks remain in polish-browser.json.'}
(ROOT/'docs/polish-guide-layout.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['passed'] else 1)

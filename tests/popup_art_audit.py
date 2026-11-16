"""Focused checks for the art-led entry dialog; previous site stays unchanged."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:3000'
checks=[]
def check(name,passed,evidence=None):
    checks.append({'name':name,'passed':bool(passed),'evidence':evidence})
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for w,h in [(360,740),(390,844),(440,956),(1440,900),(844,390)]:
        ctx=b.new_context(viewport={'width':w,'height':h})
        pg=ctx.new_page();errors=[]
        pg.on('pageerror',lambda e: errors.append(str(e)))
        pg.goto(BASE+'/',wait_until='networkidle')
        dialog=pg.locator('#welcomeDialog')
        pg.wait_for_selector('#welcomeDialog[open]');pg.wait_for_timeout(350)
        prefix=f'{w}x{h}: '
        check(prefix+'initial artwork loaded without crop',pg.locator('.welcome-art>picture>img').evaluate("e=>e.naturalWidth>0 && getComputedStyle(e).objectFit==='contain'"))
        check(prefix+'dark CTA with green identity >=50px and 16px text',pg.locator('.welcome-line').evaluate("e=>e.getBoundingClientRect().height>=50 && parseFloat(getComputedStyle(e).fontSize)>=16 && getComputedStyle(e).backgroundColor==='rgb(24, 39, 31)' && getComputedStyle(e.querySelector('.welcome-line-icon')).backgroundColor==='rgb(6, 199, 85)'"))
        check(prefix+'LINE correct and new tab',pg.locator('.welcome-line').get_attribute('href')=='https://line.me/ti/p/k2pkYGXGL3' and pg.locator('.welcome-line').get_attribute('target')=='_blank')
        check(prefix+'inside viewport',dialog.evaluate("e=>{const r=e.getBoundingClientRect();return r.x>=0&&r.y>=0&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1}"))
        for _ in range(4):pg.keyboard.press('Tab')
        check(prefix+'native keyboard focus stays in dialog',dialog.evaluate('e=>e.contains(document.activeElement)'))
        dialog.evaluate('e=>e.scrollTop=e.scrollHeight')
        check(prefix+'close remains reachable after scroll',pg.locator('.welcome-close').evaluate("e=>{const r=e.getBoundingClientRect();return r.y>=0&&r.bottom<=innerHeight&&document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('.welcome-close')===e}"))
        pg.keyboard.press('Escape')
        pg.wait_for_function("!document.getElementById('welcomeDialog').open && !document.body.classList.contains('welcome-open')")
        check(prefix+'Escape closes and unlocks',not dialog.evaluate('e=>e.open'))
        pg.goto(BASE+'/contact',wait_until='networkidle');pg.wait_for_timeout(650)
        check(prefix+'session not repeated',not pg.locator('#welcomeDialog').evaluate('e=>e.open'))
        pg.goto(BASE+'/?welcome=1',wait_until='networkidle');pg.wait_for_timeout(750)
        pg.locator('.welcome-browse').click()
        check(prefix+'secondary action closes',not pg.locator('#welcomeDialog').evaluate('e=>e.open'))
        check(prefix+'no JS exceptions',not errors,errors)
        ctx.close()
    ctx=b.new_context(java_script_enabled=False)
    pg=ctx.new_page();pg.goto(BASE+'/',wait_until='networkidle')
    check('No JS: popup absent and main remains',not pg.locator('#welcomeDialog').is_visible() and pg.locator('h1').is_visible())
    ctx.close();b.close()
result={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(ROOT/'docs/popup-art-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'total':len(checks),'failed':[c for c in checks if not c['passed']]},ensure_ascii=False,indent=2))
if result['failed']:raise SystemExit(1)

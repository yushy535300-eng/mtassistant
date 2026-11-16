"""Check real-person scenes, not a dealer carousel, at five relevant viewports."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/dealer-scenes-audit.json'
ROUTES = ['/', '/features', '/auto', '/guide?system=matrix', '/guide?system=auto', '/faq', '/contact']
SIZES = [(1440, 900), (768, 1024), (360, 800), (390, 844), (440, 900)]
checks = []


def record(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in SIZES:
        context = browser.new_context(viewport={'width': width, 'height': height})
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        for route in ROUTES:
            page.goto('http://127.0.0.1:3000' + route, wait_until='networkidle')
            page.evaluate("""() => {const d=document.querySelector('.welcome-dialog');if(d?.open){d.querySelector('[data-welcome-close]')?.click();}}""")
            page.wait_for_timeout(80)
            prefix = f'{width} {route}'
            record(prefix + ' no page overflow', page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'))
            record(prefix + ' no roster or motion control', page.locator('.mt-gallery,.mt-spotlight,#motionToggle,[data-gallery-direction]').count() == 0)
            record(prefix + ' scene foreground inside existing hero', page.locator('.has-scene-person .scene-person').count() == 1)
            record(prefix + ' true transparent foreground loaded and undistorted', page.evaluate("""() => {
                const img=document.querySelector('.has-scene-person .scene-person img');
                const r=img?.getBoundingClientRect();
                return !!img && img.complete && img.naturalWidth > 0 && img.src.includes('-cutout') && r.width > 90 && Math.abs(r.width-r.height)<2;
            }"""))
            record(prefix + ' scene is decorative not fake agent or livestream', page.locator('.scene-person[aria-hidden="true"] img[alt=""][aria-hidden="true"]').count() == 1)
            record(prefix + ' hero text and actions do not overlap foreground', page.evaluate("""() => {
                const hero=document.querySelector('.has-scene-person'),pic=hero.querySelector('.scene-person').getBoundingClientRect();
                const touches=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>2 && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>2;
                return [...hero.querySelectorAll('h1,p:not(.banner-label),a')].every(el=>!touches(el.getBoundingClientRect(),pic));
            }"""))
            record(prefix + ' safe CTA touch size', page.evaluate("""() => [...document.querySelectorAll('.has-scene-person a.button')].every(el=>el.getBoundingClientRect().height>=44)"""))
            record(prefix + ' Threads correct and safe', page.evaluate("""() => [...document.querySelectorAll('a[data-threads-link]')].every(a=>a.href==='https://www.threads.com/@hacklook__?igshid=NTc4MTIwNjQ2YQ==' && a.target==='_blank' && a.rel.includes('noopener'))"""))
            if route == '/':
                record(prefix + ' two correct main entry buttons', page.evaluate("""() => {
                    const tiles=[...document.querySelectorAll('.tool-tile')];
                    return tiles.length===2 && tiles.every((t,i)=>{
                        const btn=t.querySelector('.inline-actions a.button'),links=[...t.querySelectorAll('.inline-actions a')];
                        return btn.textContent.trim()==='進入系統' && btn.href===(i===0?'https://mt-assistant-web-v3.onrender.com/':'https://autotable-o6a2.onrender.com/') && links[0]===btn && links[1].classList.contains('text-link');
                    });
                }"""))
            if route.startswith('/guide'):
                record(prefix + ' five/six complete original steps', page.locator('#guide-panel-matrix article.guide-step-panel').count()==5 and page.locator('#guide-panel-auto article.guide-step-panel').count()==6)
            if route == '/faq':
                search=page.locator('#faqSearch');search.fill('授權');page.wait_for_timeout(80)
                record(prefix + ' FAQ search remains usable', page.locator('details.faq-item:visible').count()>0)
        record(str(width) + ' no JS errors', not errors)
        context.close()
    browser.close()

OUT.write_text(json.dumps({'checks': checks, 'passed': sum(x['passed'] for x in checks), 'total': len(checks)}, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'passed':sum(x['passed'] for x in checks),'total':len(checks),'failed':[x['check'] for x in checks if not x['passed']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)

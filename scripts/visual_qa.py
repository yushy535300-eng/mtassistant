"""Visual QA snapshots for official YUCE service. Fails on broken images or layout overflow."""
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = os.environ.get("QA_SITE_URL","https://mtassistant-oozm.onrender.com").rstrip("/")
ROUTES = ["/","/features","/auto","/guide","/download","/articles","/faq","/contact"]
WIDTHS = {"desktop":(1440,900),"mobile":(390,844)}
OUT=Path("qa-screenshots"); OUT.mkdir(exist_ok=True)
REPORT={"site":BASE,"screenshots":[],"errors":[]}

async def check():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        for label,(width,height) in WIDTHS.items():
            ctx=await browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,locale="zh-TW",is_mobile=label=="mobile",has_touch=label=="mobile")
            for route in ROUTES:
                page=await ctx.new_page()
                path="home" if route=="/" else route.strip("/")
                try:
                    res=await page.goto(BASE+route,wait_until="domcontentloaded",timeout=45000)
                    if not res or res.status>=400: REPORT["errors"].append(f"{label} {route}: HTTP {res.status if res else 'no response'}")
                    await page.wait_for_timeout(1600)
                    await page.evaluate("() => { const d=document.getElementById('welcomeDialog'); if(d?.open) d.close(); }")
                    await page.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading='eager')")
                    await page.wait_for_timeout(2600)
                    await page.evaluate("document.fonts.ready")
                    overflow=await page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 3")
                    if overflow:REPORT["errors"].append(f"{label} {route}: horizontal overflow")
                    imgs=await page.locator("main img").evaluate_all("(nodes)=>nodes.filter(i=>i.getClientRects().length>0 && getComputedStyle(i).visibility!=='hidden' && (!i.complete || i.naturalWidth===0)).map(i=>i.currentSrc)")
                    for src in imgs:REPORT["errors"].append(f"{label} {route}: broken image {src}")
                    if route=="/":
                        videonum=await page.locator("video.mt-full-video").count()
                        if videonum!=3:REPORT["errors"].append(f"{label} home: expected 3 original videos, got {videonum}")
                        adnum=await page.locator("[data-ad-carousel='billboard']").count()
                        if adnum!=1:REPORT["errors"].append(f"{label} home: expected exactly one billboard, got {adnum}")
                        if label=="mobile":
                            visible=await page.locator("#mt-video-track .mt-video-card").count()
                            if visible!=3:REPORT["errors"].append(f"Mobile video carousel card count {visible}")
                    file=OUT/f"{label}-{path}.png"
                    await page.screenshot(path=str(file),full_page=True,animations="disabled")
                    REPORT["screenshots"].append(str(file))
                except Exception as exc:
                    REPORT["errors"].append(f"{label} {route}: {type(exc).__name__} {str(exc)[:150]}")
                finally:await page.close()
            await ctx.close()
        await browser.close()
    (OUT/"report.json").write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(REPORT,ensure_ascii=False,indent=2))
    if REPORT["errors"]:raise SystemExit(1)

asyncio.run(check())

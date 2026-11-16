const fs=require('fs');const path=require('path');
const {chromium,webkit}=require(path.join(process.env.QA_NODE_MODULES||'/tmp/yuce-qa/node_modules','playwright'));
const BASE=process.env.TEST_ORIGIN||'http://127.0.0.1:3100';
const OUT=path.join(process.cwd(),'artifacts');fs.mkdirSync(OUT,{recursive:true});
const routes=['/','/features','/auto','/guide','/download','/faq','/contact','/articles','/articles/matrix-workflow','/articles/auto-checklist','/articles/model-panels','/articles/mobile-home-screen','/articles/execution-status','/articles/connection-troubleshooting'];
const result={layouts:[],interactions:[],errors:[],browsers:[]};
const check=(name,ok,details)=>{result.interactions.push({name,passed:!!ok,details});if(!ok)result.errors.push(name+': '+JSON.stringify(details||''));};
const filename=r=>r==='/'?'home':r.slice(1).replaceAll('/','-');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 for(const width of [360,430,768,1440,1920]){
  const context=await browser.newContext({viewport:{width,height:width<641?932:1000},deviceScaleFactor:1,isMobile:width<641,hasTouch:width<641});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  const list=[430,768,1440].includes(width)?routes:['/','/features','/auto','/articles/matrix-workflow'];
  for(const route of list){
   const response=await page.goto(BASE+route+(route.includes('?')?'&':'?')+'welcome=0',{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
   const info=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,badImages:[...document.images].filter(i=>{const r=i.getBoundingClientRect();return r.width&&r.height&&r.top<innerHeight&&r.bottom>0&&(!i.complete||!i.naturalWidth)}).map(i=>i.getAttribute('src'))}));
   const ok=response.status()===200&&info.documentWidth<=width+1&&info.h1===1&&!info.badImages.length;
   result.layouts.push({route,width,passed:ok,...info});if(!ok)result.errors.push('Layout '+width+' '+route+': '+JSON.stringify(info));
   if([430,1440].includes(width))await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>{i.loading='eager';});await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
   if([430,1440].includes(width))await page.screenshot({path:path.join(OUT,filename(route)+'-'+width+'.jpg'),type:'jpeg',quality:78,fullPage:true});
   if(route==='/'&&width===1440){await page.locator('#toolbox').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(OUT,'product-showcase-desktop.jpg'),type:'jpeg',quality:85});}
  }
  if(errors.length)result.errors.push(...errors.map(e=>width+' '+e));await context.close();
 }
 const context=await browser.newContext({viewport:{width:430,height:932},isMobile:true,hasTouch:true});const page=await context.newPage();
 await page.goto(BASE+'/?welcome=0',{waitUntil:'networkidle'});
 await page.locator('#menuToggle').click();check('Mobile navigation opens',await page.locator('#mobileNav').isVisible());await page.keyboard.press('Escape');check('Mobile navigation closes',!(await page.locator('#mobileNav').isVisible()));
 await page.locator('#tab-parity').click();check('Real model switch',await page.locator('#focus-parity').isVisible()&&!(await page.locator('#focus-cards').isVisible()));
 await page.locator('#focus-parity [data-image]').click();check('Original full-resolution viewer',await page.locator('#imageViewer').isVisible()&&(await page.locator('#viewerImage').getAttribute('src')).includes('parity-model.png'));await page.locator('#viewerClose').click();
 await page.goto(BASE+'/guide?system=auto&welcome=0',{waitUntil:'networkidle'});check('Direct AUTO guide',await page.locator('#guide-panel-auto').isVisible());await page.locator('#guide-tab-matrix').click();check('Guide switch',await page.locator('#guide-panel-matrix').isVisible());
 await page.goto(BASE+'/download?welcome=0',{waitUntil:'networkidle'});await page.locator('#install-matrix-android-tab').click();check('Android installation tab',await page.locator('#install-matrix-android-panel').isVisible());
 await page.goto(BASE+'/faq?welcome=0',{waitUntil:'networkidle'});await page.locator('#faqSearch').fill('手機');check('FAQ filters actual content',await page.locator('.faq-item:visible').count()===1);await page.locator('#faqSearch').fill('不存在xyz');check('FAQ empty state',await page.locator('#faqEmpty').isVisible());
 await page.goto(BASE+'/contact?welcome=0',{waitUntil:'networkidle'});await page.locator('#v2-issue').fill('介面驗收測試，不傳送任何訊息。');await page.locator('#v2-support-form button[type=submit]').click();check('Local support summary',((await page.locator('#v2-summary').inputValue())||'').includes('介面驗收測試'));
 await context.close();
 const reduced=await browser.newContext({viewport:{width:430,height:932},reducedMotion:'reduce'});const reducedPage=await reduced.newPage();await reducedPage.goto(BASE+'/?welcome=0',{waitUntil:'networkidle'});const motion=await reducedPage.evaluate(()=>({orbit:getComputedStyle(document.querySelector('.atelier-orbit')).animationName,beam:getComputedStyle(document.querySelector('.banner-light')).animationName,title:getComputedStyle(document.querySelector('.yc-art-title'),'::before').display}));check('Reduced motion and no site sweep',motion.orbit==='none'&&motion.beam==='none'&&motion.title==='none',motion);await reduced.close();
 result.browsers.push('Chromium');await browser.close();
 const safari=await webkit.launch({headless:true});const safariContext=await safari.newContext({viewport:{width:430,height:932},isMobile:true,hasTouch:true});const safariPage=await safariContext.newPage();
 for(const route of ['/','/features','/auto','/guide','/download','/articles/matrix-workflow']){await safariPage.goto(BASE+route+'?welcome=0',{waitUntil:'networkidle'});const w=await safariPage.evaluate(()=>({width:innerWidth,doc:document.documentElement.scrollWidth}));check('WebKit '+route,w.doc<=w.width+1,w);}
 await safariPage.goto(BASE+'/?welcome=0',{waitUntil:'networkidle'});await safariPage.screenshot({path:path.join(OUT,'home-webkit-phone.jpg'),type:'jpeg',quality:82,fullPage:true});result.browsers.push('WebKit');await safari.close();
 fs.writeFileSync(path.join(OUT,'browser-audit.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({layouts:result.layouts.length,interactions:result.interactions.length,errors:result.errors,browsers:result.browsers},null,2));if(result.errors.length)process.exitCode=1;
})().catch(e=>{result.errors.push(String(e.stack||e));fs.writeFileSync(path.join(OUT,'browser-audit.json'),JSON.stringify(result,null,2));console.error(e);process.exitCode=1});

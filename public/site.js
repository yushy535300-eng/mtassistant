(()=>{'use strict';
 const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
 const menu=$('#mobileNav'),toggle=$('#menuToggle');
 function setMenu(open){if(!menu||!toggle)return;menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'關閉選單':'開啟選單');}
 toggle?.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
 window.addEventListener('resize',()=>{if(innerWidth>980)setMenu(false);},{passive:true});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false);});
 const viewer=$('#imageViewer'),image=$('#viewerImage');
 $$('[data-image]').forEach(button=>button.addEventListener('click',()=>{
  if(!viewer||!image)return;
  image.src=button.dataset.image;image.alt=button.dataset.title;
  $('#viewerTitle').textContent=button.dataset.title;
  viewer.showModal();document.body.classList.add('viewer-open');
  $('.viewer-scroll').scrollTo(0,0);
 }));
 $('#viewerClose')?.addEventListener('click',()=>viewer.close());
 viewer?.addEventListener('click',event=>{if(event.target===viewer)viewer.close();});
 viewer?.addEventListener('close',()=>document.body.classList.remove('viewer-open'));
 const tabs=$$('[data-tab]');
 function activateTab(tab){for(const t of tabs){const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;const panel=$('#focus-'+t.dataset.tab);if(panel)panel.hidden=!active;}}
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>activateTab(t));t.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const index=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;tabs[index].focus();activateTab(tabs[index]);});});
 if(tabs.length)activateTab(tabs[0]);
 const search=$('#faqSearch');search?.addEventListener('input',()=>{const q=search.value.trim().toLowerCase();let count=0;$$('.faq-item').forEach(item=>{const show=item.textContent.toLowerCase().includes(q);item.hidden=!show;if(show)count++;});$('#faqEmpty').hidden=count>0;});
 const guideTabs=$$('[data-guide]');
 function selectGuide(name,updateUrl=false,scroll=false){
  if(!['matrix','auto'].includes(name)||!guideTabs.length)return;
  for(const t of guideTabs){const active=t.dataset.guide===name;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;$('#guide-panel-'+t.dataset.guide).hidden=!active;}
  for(const system of ['matrix','auto']){const preview=$('#guide-preview-'+system);if(preview)preview.hidden=system!==name;}
  document.body.dataset.guideSystem=name;
  if(updateUrl){const url=new URL(location.href);url.searchParams.set('system',name);url.hash='';history.replaceState(null,'',url.pathname+url.search);}
  if(scroll)$('#guide-panel-'+name).scrollIntoView({block:'start',behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
 }
 guideTabs.forEach((t,i)=>{t.addEventListener('click',()=>selectGuide(t.dataset.guide,true,false));t.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const next=guideTabs[e.key==='Home'?0:e.key==='End'?1:1-i];next.focus();selectGuide(next.dataset.guide,true,false);});});
 if(guideTabs.length){const requested=new URLSearchParams(location.search).get('system');selectGuide(requested==='auto'||location.hash.startsWith('#auto-step')?'auto':'matrix');}
})();

(() => {
  'use strict';
  const $ = (selector, root=document) => root.querySelector(selector);
  const $$ = (selector, root=document) => [...root.querySelectorAll(selector)];
  const nav = $('#nav');
  const menuButton = $('#mobileMenu');
  if (nav && menuButton) {
    const setOpen = open => {
      nav.classList.toggle('is-open', open);
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? '關閉選單' : '展開選單');
    };
    menuButton.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
    $$('a', nav).forEach(link => link.addEventListener('click', () => setOpen(false)));
    window.addEventListener('keydown', event => { if (event.key === 'Escape') setOpen(false); });
    window.addEventListener('resize', () => { if (window.innerWidth > 1090) setOpen(false); }, { passive:true });
  }
  const examples = [
    ['BAV01', '閒', '高可信'],['BAV01_LIVE', '閒', '高可信'],['BAV02', '莊', '低可信'],
    ['BAV02_LIVE', '莊', '低可信'],['BAV03', '莊', '低可信'],
    ['BAV03A', '閒', '高可信'],['BAV05', '莊', '中可信'],['BAV06', '莊', '中可信'],
    ['BAV07', '閒', '低可信'],['BAV08', '閒', '中可信']
  ];
  const tableParent = $('#previewTables');
  if (tableParent) {
    const fragment = document.createDocumentFragment();
    for (const [index, table] of examples.entries()) {
      const tile = document.createElement('div');
      if (index===0) tile.className='chosen';
      const direction = document.createElement('span');
      direction.className = table[1] === '莊' ? 'bet-bank' : 'bet-player';
      direction.textContent = '● ' + table[1];
      const name = document.createElement('b');
      name.textContent = table[0];
      const confidence = document.createElement('small');
      confidence.textContent = table[2];
      tile.append(name, direction, confidence);
      fragment.appendChild(tile);
    }
    tableParent.replaceChildren(fragment);
  }
  const tabButtons=$$('[data-preview]');
  const titles={radar:'多桌雷達',analysis:'AI 綜合輔助',cards:'V38 四式算牌',parity:'終值奇偶模型'};
  const activate=name=>{
    if(!titles[name])return;
    for(const tab of tabButtons){
      const selected=tab.dataset.preview===name;
      tab.classList.toggle('selected',selected);
      tab.setAttribute('aria-selected',String(selected));
      tab.tabIndex=selected?0:-1;
    }
    for(const [key] of Object.entries(titles)){
      const panel=$('#panel-'+key);
      if(panel){
        const visible=key===name;
        panel.hidden=!visible;
        panel.classList.toggle('visible',visible);
      }
    }
    const title=$('#stageTitle');
    if(title)title.textContent=titles[name];
  };
  tabButtons.forEach((tab,index)=>{
    tab.addEventListener('click',()=>activate(tab.dataset.preview));
    tab.addEventListener('keydown',e=>{
      if(e.key!=='ArrowDown'&&e.key!=='ArrowUp'&&e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
      e.preventDefault();
      const step=(e.key==='ArrowDown'||e.key==='ArrowRight')?1:-1;
      const next=tabButtons[(index+step+tabButtons.length)%tabButtons.length];
      next?.focus();if(next)activate(next.dataset.preview);
    });
  });
  activate('radar');

  // Refined interaction layer; all motion is optional and GPU-friendly.
  const reduceMotion=window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
  const meter=$('#scrollMeter');
  let pendingScroll=false;
  function updateScrollMeter(){
    pendingScroll=false;
    if(!meter)return;
    const height=Math.max(1,document.documentElement.scrollHeight-window.innerHeight);
    const ratio=Math.max(0,Math.min(1,window.scrollY/height));
    meter.style.width=(ratio*100).toFixed(2)+'%';
  }
  window.addEventListener('scroll',()=>{
    if(pendingScroll)return;
    pendingScroll=true;
    window.requestAnimationFrame(updateScrollMeter);
  },{passive:true});
  window.addEventListener('resize',updateScrollMeter,{passive:true});
  updateScrollMeter();

  // Reveal informational sections gently; show all immediately for reduced
  // motion, older browsers, and without JavaScript.
  const revealNodes=$$('.section-head,.feature-large,.feature-compact,.showcase-copy,.showcase-stage,.auto-console,.auto-feature-copy,.auto-subfeatures,.how-grid>div,.faqs,.bottom-cta-inner,.identity-transition-inner');
  if(!reduceMotion && 'IntersectionObserver' in window){
    const revealObserver=new IntersectionObserver(entries=>{
      for(const entry of entries){
        if(!entry.isIntersecting)continue;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    },{rootMargin:'0px 0px -35px 0px',threshold:.08});
    revealNodes.forEach((node,i)=>{
      node.classList.add('reveal-up');
      if(i%3)node.dataset.delay=String(i%3);
      revealObserver.observe(node);
    });
  }
  const finePointer=window.matchMedia?.('(pointer:fine)').matches ?? false;
  if(finePointer&&!reduceMotion){
    document.body.classList.add('has-fine-pointer');
    const halo=$('#ambientHalo');
    let x=0,y=0,requestPending=false;
    document.addEventListener('pointermove',e=>{
      if(e.pointerType&&e.pointerType!=='mouse')return;
      x=e.clientX;y=e.clientY;
      if(requestPending)return;
      requestPending=true;
      window.requestAnimationFrame(()=>{
        requestPending=false;
        if(halo){
          halo.style.setProperty('--cursor-x',x+'px');
          halo.style.setProperty('--cursor-y',y+'px');
        }
      });
    },{passive:true});
  }
  const showcase=$('#showcase');
  if(showcase&&finePointer&&!reduceMotion){
    showcase.addEventListener('pointermove',e=>{
      const bounds=showcase.getBoundingClientRect();
      const px=((e.clientX-bounds.left)/Math.max(bounds.width,1)*100).toFixed(1);
      const py=((e.clientY-bounds.top)/Math.max(bounds.height,1)*100).toFixed(1);
      showcase.style.setProperty('--show-x',px+'%');
      showcase.style.setProperty('--show-y',py+'%');
    },{passive:true});
  }
  // Press feedback is limited to real navigation controls; it does not
  // interfere with links or simulate the actual betting product.
  $$('a.primary-btn,a.outline-btn,a.head-entry').forEach(control=>{
    control.addEventListener('pointerdown',()=>control.classList.add('is-pressed'),{passive:true});
    for(const e of ['pointerup','pointerleave','pointercancel'])control.addEventListener(e,()=>control.classList.remove('is-pressed'),{passive:true});
  });

  const sections=$$('main section[id]');
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      const first=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
      if(!first)return;
      $$('.navigation a').forEach(link=>link.classList.toggle('active',link.hash==='#'+first.target.id));
    },{rootMargin:'-15% 0px -65% 0px',threshold:[0,.2,.5]});
    sections.forEach(section=>observer.observe(section));
  }
})();
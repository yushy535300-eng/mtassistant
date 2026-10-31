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
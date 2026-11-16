(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const capture = new URLSearchParams(location.search).get('capture') === '1';
  const toggle = document.getElementById('motionToggle');
  let paused = false;
  // The user removed the header control; stale preferences must not freeze the scene.
  if (toggle) {
    try { paused = sessionStorage.getItem('portalMotionPaused') === 'true'; } catch (_) {}
  }
  let request = 0, previous = 0, elapsed = 0;
  const stages = [];
  const ranges = [[4, 6], [2.4, 4], [1.2, 2.4]];
  const drift = [2, 6, 17];

  document.querySelectorAll('.portal-banner, .portal-pagehead').forEach((parent, index) => {
    if (parent.closest('.page-faq, .page-contact')) return;
    let canvas = parent.querySelector('canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'head-sparks';
      canvas.setAttribute('aria-hidden', 'true');
      parent.append(canvas);
    }
    if (getComputedStyle(canvas).display === 'none') return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    let seed = 72 + index;
    const random = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const count = innerWidth < 641 ? 25 : 48;
    const points = Array.from({length:count}, (_, i) => ({
      x:random() * 1.7 - .85, y:random() * 1.1 - .55,
      depth:i % 3, phase:random(), radius:.65 + random() * .55,
      brightness:.38 + random() * .38, tint:random() > .35,
    }));
    const bounds = parent.getBoundingClientRect();
    const stage = {parent, canvas, ctx, points, width:0, height:0,
      visible:bounds.bottom > 0 && bounds.top < innerHeight};
    stages.push(stage);
    parent.dataset.motionLayers = '3';
    parent.dataset.motionMode = 'perspective-depth';
  });

  function size() {
    const dpr = Math.min(devicePixelRatio || 1, innerWidth < 641 ? 1.25 : 1.5);
    stages.forEach((stage) => {
      stage.width = stage.parent.clientWidth;
      stage.height = stage.parent.clientHeight;
      stage.canvas.width = Math.round(stage.width * dpr);
      stage.canvas.height = Math.round(stage.height * dpr);
      stage.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    });
  }

  function paint(time, all = false) {
    stages.forEach((stage) => {
      if (!all && !stage.visible) return;
      const {ctx, width, height} = stage;
      ctx.clearRect(0, 0, width, height);
      stage.points.forEach((point) => {
        const cycle = (point.phase + time * (.007 + point.depth * .008)) % 1;
        const [near, far] = ranges[point.depth];
        const z = far - (far - near) * cycle;
        const perspective = 2.8 / z;
        const wrap = width * 1.2;
        const x = ((width * .78 + point.x * width * perspective + time * drift[point.depth]) % wrap + wrap) % wrap - width * .05;
        const y = height * .46 + point.y * height * perspective + Math.sin(time * .12 + point.phase * 7) * 3;
        const edge = Math.max(0, Math.min(1, x / 32, (width - x) / 32, y / 22, (height - y) / 22));
        const depthFade = Math.pow(Math.sin(cycle * Math.PI), .7);
        const protectedText = Math.max(0, Math.min(1, (x / width - .45) * 5));
        const alpha = point.brightness * edge * depthFade * protectedText;
        if (alpha <= .01) return;
        ctx.fillStyle = point.tint ? `rgba(214,246,239,${alpha})` : `rgba(255,218,198,${alpha})`;
        ctx.beginPath();
        ctx.arc(x, y, point.radius * perspective, 0, Math.PI * 2);
        ctx.fill();
      });
      stage.parent.dataset.motionFrames = String((Number(stage.parent.dataset.motionFrames) || 0) + 1);
    });
  }

  function frame(now) {
    if (paused || reduced.matches || document.hidden || capture || !stages.some(stage => stage.visible)) {
      previous = 0; request = 0; return;
    }
    if (!previous || now - previous >= 32) {
      const delta = previous ? Math.min((now - previous) / 1000, .08) : 0;
      elapsed += delta; previous = now; paint(elapsed);
    }
    request = requestAnimationFrame(frame);
  }

  function sync() {
    const stop = paused || reduced.matches || document.hidden || capture;
    document.body.classList.toggle('motion-paused', stop);
    if (request) cancelAnimationFrame(request);
    request = 0; previous = 0;
    if (!stop && stages.some(stage => stage.visible)) request = requestAnimationFrame(frame);
    if (!toggle) return;
    const label = reduced.matches ? '減少動態' : paused ? '開啟動態' : '暫停動態';
    const text = toggle.querySelector('.motion-label');
    if (text) text.textContent = label;
    const symbol = toggle.querySelector('svg');
    if (symbol) symbol.innerHTML = paused || reduced.matches ? '<path d="m9 5 10 7-10 7z"/>' : '<path d="M8 5v14M16 5v14"/>';
    toggle.title = label;
    toggle.setAttribute('aria-pressed', String(paused || reduced.matches));
    toggle.setAttribute('aria-label', reduced.matches ? '已依裝置設定減少動態' : paused ? '開啟背景動態' : '暫停背景動態');
    toggle.disabled = reduced.matches;
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const stage = stages.find(item => item.parent === entry.target);
        if (stage) stage.visible = entry.isIntersecting;
        entry.target.classList.toggle('stage-offscreen', !entry.isIntersecting);
      });
      sync();
    }, {rootMargin:'0px', threshold:0});
    stages.forEach(stage => observer.observe(stage.parent));
  }
  toggle?.addEventListener('click', () => {
    paused = !paused;
    try { sessionStorage.setItem('portalMotionPaused', String(paused)); } catch (_) {}
    sync();
  });
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  let resizePending = false;
  window.addEventListener('resize', () => {
    if (resizePending) return;
    resizePending = true;
    requestAnimationFrame(() => { resizePending = false; size(); paint(elapsed, true); sync(); });
  }, {passive:true});
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') document.querySelector('.launch-menu')?.removeAttribute('open');
  });
  document.addEventListener('click', (event) => {
    const launcher = document.querySelector('.launch-menu');
    if (launcher && !launcher.contains(event.target)) launcher.removeAttribute('open');
  });
  size(); paint(0, true); sync();
})();

/* Real recordings: native audio controls; avoid overlapping sound. */
document.addEventListener('DOMContentLoaded', () => {
  const videos=Array.from(document.querySelectorAll('video.mt-full-video'));
  videos.forEach(video=>video.addEventListener('play',()=>videos.forEach(other=>{if(other!==video&&!other.paused)other.pause();})));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)videos.forEach(video=>video.pause());});
});

/* Home hero: a stable, visibility-aware five-second crossfade. */
(() => {
  const rot = document.querySelector('[data-dealer-rotation]');
  if (!rot) return;
  const slides = Array.from(rot.querySelectorAll('picture'));
  if (slides.length < 2) return;
  const DEALER_INTERVAL_MS = 5000;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const capture = new URLSearchParams(location.search).get('capture') === '1';
  let available = [], current = slides[0], timer = 0, visible = true;
  function show(slide) {
    if (!slide) return;
    current = slide;
    slides.forEach(item => item.classList.toggle('is-active', item === slide));
    rot.dataset.activeDealer = slide.dataset.dealerId || '';
  }
  function sync() {
    clearInterval(timer);
    timer = 0;
    if (available.length > 1 && visible && !document.hidden && !reduced.matches && !capture) {
      timer = setInterval(() => {
        const next = (available.indexOf(current) + 1) % available.length;
        show(available[next]);
      }, DEALER_INTERVAL_MS);
    }
  }
  function imageReady(slide) {
    const img = slide.querySelector('img');
    if (!img) return Promise.resolve(false);
    if (img.complete) return Promise.resolve(img.naturalWidth > 0);
    return new Promise(resolve => {
      img.addEventListener('load', () => resolve(true), {once:true});
      img.addEventListener('error', () => resolve(false), {once:true});
    });
  }
  show(slides[0]);
  rot.classList.add('is-ready');
  Promise.all(slides.map(imageReady)).then(results => {
    available = slides.filter((_, i) => results[i]);
    if (available.length && !available.includes(current)) show(available[0]);
    sync();
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(rot);
  }
  document.addEventListener('visibilitychange', sync);
  reduced.addEventListener('change', () => { if (reduced.matches) show(available[0] || slides[0]); sync(); });
})();

/* Independent, accessible brand campaigns. No runtime external asset requests. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const capture=new URLSearchParams(location.search).get('capture')==='1';
 document.querySelectorAll('[data-ad-carousel]').forEach(slot=>{
   const slides=[...slot.querySelectorAll('[data-ad-slide]')],dots=[...slot.querySelectorAll('[data-ad-index]')];
   if(!slides.length)return;
   let current=0,timer=0,visible=false,touch=null;
   const show=index=>{current=(index+slides.length)%slides.length;slides.forEach((item,i)=>{item.hidden=i!==current;item.toggleAttribute('data-active',i===current)});dots.forEach((dot,i)=>dot.setAttribute('aria-pressed',String(i===current)));};
   const sync=()=>{clearInterval(timer);timer=0;if(!visible||slot.hidden||document.hidden||reduced.matches||capture)return;timer=setInterval(()=>{if(!slot.matches(':hover')&&!slot.contains(document.activeElement))show(current+1)},10000);};
   const select=index=>{show(index);sync()};
   dots.forEach((dot,i)=>dot.addEventListener('click',()=>select(i)));
   slot.querySelector('[data-ad-prev]').addEventListener('click',()=>select(current-1));
   slot.querySelector('[data-ad-next]').addEventListener('click',()=>select(current+1));
   const stage=slot.querySelector('.yc-ad-stage');let swiped=false;
   stage.addEventListener('touchstart',e=>{touch=[e.changedTouches[0].clientX,e.changedTouches[0].clientY];swiped=false},{passive:true});
   stage.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch[0],dy=e.changedTouches[0].clientY-touch[1];if(Math.abs(dx)>42&&Math.abs(dx)>Math.abs(dy)*1.3){swiped=true;select(current+(dx<0?1:-1));}touch=null;},{passive:true});
   stage.addEventListener('click',e=>{if(swiped){e.preventDefault();swiped=false;}},true);
   if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync()}).observe(slot);else{visible=true;sync()}
   document.addEventListener('visibilitychange',sync);reduced.addEventListener('change',sync);
   if(slot.dataset.adCarousel!=='float')return;
   const open=document.getElementById('ycAdOpen');let state='ready',forced=false;try{state=sessionStorage.getItem('yuceScarabAdState')||'ready'}catch(_){}
   const setState=value=>{state=value;if(value!=='ready')forced=false;try{sessionStorage.setItem('yuceScarabAdState',value)}catch(_){}update()};
   const update=()=>{const display=!capture&&state==='ready'&&(forced||scrollY>360);slot.hidden=!display;open.hidden=capture||state!=='collapsed';document.body.classList.toggle('yc-ad-opened',display);sync()};
   slot.querySelector('[data-ad-collapse]').addEventListener('click',()=>setState('collapsed'));
   slot.querySelector('[data-ad-close]').addEventListener('click',()=>setState('closed'));
   open.addEventListener('click',()=>{forced=true;setState('ready')});
   window.addEventListener('scroll',update,{passive:true});update();
 });
})();

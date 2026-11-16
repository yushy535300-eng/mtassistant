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
    const count = innerWidth < 641 ? 36 : 76;
    const points = Array.from({length:count}, (_, i) => ({
      x:random() * 1.7 - .85, y:random() * 1.1 - .55,
      depth:i % 3, phase:random(), radius:.75 + random() * .75,
      brightness:.46 + random() * .40, tint:random() > .35,
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


/* V3: motion surfaces, viewport-aware video, and responsive real MT exhibits. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const capture = new URLSearchParams(location.search).get('capture') === '1';
  const body = document.body;
  body.classList.add('motion-js');

  document.querySelectorAll('.portal-banner,.portal-pagehead').forEach((head) => {
    if (head.querySelector('.motion-head-lines')) return;
    const layer = document.createElement('span');
    layer.className = 'motion-head-lines';
    layer.setAttribute('aria-hidden','true');
    head.append(layer);
  });
  document.querySelectorAll('#main .portal-panel,#main .tool-tile,#main .guide-entry,#main .portal-shortcuts>a,#main .contact-link,#main .mt-pair-card').forEach(card => card.classList.add('motion-card'));

  const reveal = Array.from(document.querySelectorAll('#main .portal-section,#main .portal-direct-tools,#main .portal-shortcuts,#main .action-strip'));
  let revealObserver = null;
  function revealAll() {
    reveal.forEach(el => { el.classList.remove('motion-pending'); el.classList.add('motion-entered'); });
  }
  if (!reduced.matches && !capture && 'IntersectionObserver' in window) {
    revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.remove('motion-pending');
        entry.target.classList.add('motion-entered');
        revealObserver.unobserve(entry.target);
      });
    }, {threshold:.06,rootMargin:'0px 0px 40px 0px'});
    reveal.forEach(el => {
      const box=el.getBoundingClientRect();
      if (box.top > innerHeight * .90) {
        el.classList.add('motion-pending');
        revealObserver.observe(el);
      } else el.classList.add('motion-entered');
    });
  } else revealAll();

  const stages = Array.from(document.querySelectorAll('[data-mt-stage]'));
  let stageVisible = true;
  const video = document.querySelector('[data-mt-video]');
  const toggle = document.querySelector('[data-mt-video-toggle]');
  const fullscreen = document.querySelector('[data-mt-video-fullscreen]');
  let userPaused = false;
  let userStarted = false;

  function labelVideo() {
    if (!video || !toggle) return;
    const playing = !video.paused && !video.ended;
    toggle.textContent = playing ? '暫停影片' : '播放影片';
    toggle.setAttribute('aria-pressed', String(playing));
    toggle.setAttribute('aria-label', playing ? '暫停 MT 動態展示影片' : '播放 MT 動態展示影片');
  }
  function playVideo() {
    if (!video) return;
    const task=video.play();
    if (task && typeof task.catch==='function') task.catch(labelVideo);
  }
  function syncVideo() {
    if (!video) return;
    if (document.hidden || !stageVisible || capture || userPaused || (reduced.matches && !userStarted)) video.pause();
    else playVideo();
    labelVideo();
  }
  if (video) {
    video.muted = true;
    video.controls = false;
    const container=video.closest('[data-mt-stage]');
    const box=container?.getBoundingClientRect();
    stageVisible=!!box && box.bottom>0 && box.top<innerHeight;
    video.addEventListener('play',labelVideo);
    video.addEventListener('pause',labelVideo);
    video.addEventListener('ended',labelVideo);
    video.addEventListener('error',() => { video.controls=true; labelVideo(); });
    toggle?.addEventListener('click',() => {
      if (video.paused || video.ended) { userPaused=false; userStarted=true; playVideo(); }
      else { userPaused=true; video.pause(); }
      labelVideo();
    });
    fullscreen?.addEventListener('click',() => {
      if (video.requestFullscreen) {
        const task=video.requestFullscreen(); if(task?.catch) task.catch(()=>{video.controls=true;});
      } else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
      else video.controls=true;
    });
  }
  if ('IntersectionObserver' in window) {
    const stageObserver=new IntersectionObserver(entries => {
      entries.forEach(entry => {
        entry.target.classList.toggle('mt-stage-offscreen', !entry.isIntersecting);
        if (video && entry.target.contains(video)) {
          stageVisible=entry.isIntersecting;
          syncVideo();
        }
      });
    }, {threshold:.12,rootMargin:'0px'});
    stages.forEach(stage=>stageObserver.observe(stage));
  }
  if (matchMedia('(pointer:fine)').matches && !reduced.matches && !capture) {
    document.querySelectorAll('.mt-cinema').forEach(card => {
      let pending=0,x=50,y=38;
      card.addEventListener('pointermove',event=>{
        const b=card.getBoundingClientRect();
        x=Math.max(0,Math.min(100,(event.clientX-b.left)/b.width*100));
        y=Math.max(0,Math.min(100,(event.clientY-b.top)/b.height*100));
        if(!pending) pending=requestAnimationFrame(()=>{
          card.style.setProperty('--mt-pointer-x',x+'%');
          card.style.setProperty('--mt-pointer-y',y+'%');
          pending=0;
        });
      },{passive:true});
      card.addEventListener('pointerleave',()=>{
        card.style.setProperty('--mt-pointer-x','50%');
        card.style.setProperty('--mt-pointer-y','38%');
      });
    });
  }
  reduced.addEventListener('change',()=>{
    if(reduced.matches){revealObserver?.disconnect();revealAll();userStarted=false;}
    syncVideo();
  });
  document.addEventListener('visibilitychange',syncVideo);
  syncVideo();
})();

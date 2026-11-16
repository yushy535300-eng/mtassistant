/* A single ambient renderer. Content, focus and controls never depend on it. */
(() => {
  'use strict';
  const stage = document.getElementById('skyStage');
  if (!stage) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const capture = new URLSearchParams(location.search).get('capture') === '1';
  const canvas = document.getElementById('auroraCanvas');
  const starCanvas = document.getElementById('starCanvas');
  const context = starCanvas.getContext('2d', { alpha: true });
  const toggle = document.getElementById('motionToggle');
  let width = innerWidth, height = innerHeight, mobile = width <= 640;
  let gl = null, program = null, timeLocation = null, sizeLocation = null, texture = null;
  let ready = false, textureMobile = null, request = 0, animation = 0;
  let frames = 0, last = 0, clock = 2.4, stars = [], averageCost = 0, lowQuality = false;
  let userPaused = false;
  try { userPaused = sessionStorage.getItem('yuce-motion-paused') === 'true'; } catch (_) { /* Optional preference. */ }
  const vertex = 'attribute vec2 p;varying vec2 uv;void main(){uv=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
  const fragment = `precision mediump float;
    varying vec2 uv; uniform float time; uniform vec2 resolution;
    uniform sampler2D art; uniform float portrait;
    void main(){
      vec2 q=vec2(uv.x,1.-uv.y);
      float rhythm=time*.43+.17*sin(time*.57);
      float region=mix(smoothstep(.3,.78,q.x),smoothstep(.30,.72,q.y),portrait);
      vec2 sampleUV=q;
      sampleUV.x+=region*(.038*sin(q.y*8.+rhythm)+.016*sin(q.y*14.-time*.49));
      sampleUV.y+=region*(.041*sin(q.x*6.-rhythm)+.018*cos(q.x*11.+time*.38));
      float screenRatio=resolution.x/resolution.y;
      float imageRatio=mix(2.333333,.5625,portrait);
      if(screenRatio>imageRatio)sampleUV.y=(sampleUV.y-.5)*imageRatio/screenRatio+.5;
      else sampleUV.x=(sampleUV.x-.5)*screenRatio/imageRatio+.5;
      vec3 colour=texture2D(art,clamp(sampleUV,.001,.999)).rgb;
      float flow=.9+.1*sin(time*.8+q.x*5.+q.y*4.);
      colour*=flow;
      gl_FragColor=vec4(colour,1.);
    }`;
  function shader(type, source) {
    const result = gl.createShader(type);
    gl.shaderSource(result, source); gl.compileShader(result);
    if (!gl.getShaderParameter(result, gl.COMPILE_STATUS)) {
      gl.deleteShader(result); throw new Error('Scene shader unavailable');
    }
    return result;
  }
  function initialise() {
    try {
      gl = canvas.getContext('webgl', { alpha:false, antialias:false, depth:false, stencil:false, powerPreference:'low-power' });
      if (!gl) { stage.dataset.renderer = 'css-fallback'; return; }
      program = gl.createProgram();
      gl.attachShader(program, shader(gl.VERTEX_SHADER, vertex));
      gl.attachShader(program, shader(gl.FRAGMENT_SHADER, fragment));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error('Scene unavailable');
      gl.useProgram(program);
      const buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,buffer);
      gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
      const position = gl.getAttribLocation(program,'p');
      gl.enableVertexAttribArray(position); gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
      timeLocation = gl.getUniformLocation(program,'time');
      sizeLocation = gl.getUniformLocation(program,'resolution');
      texture = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,texture);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
      gl.uniform1i(gl.getUniformLocation(program,'art'),0);
      stage.dataset.renderer = 'webgl';
    } catch (_) { gl = null; stage.dataset.renderer = 'css-fallback'; }
  }
  function loadArt() {
    if (!gl || textureMobile === mobile) return;
    textureMobile = mobile;
    const id = ++request, image = new Image();
    image.onload = () => {
      if (!gl || id !== request) return;
      gl.bindTexture(gl.TEXTURE_2D,texture);
      gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,image);
      gl.uniform1f(gl.getUniformLocation(program,'portrait'),mobile ? 1 : 0);
      ready = true; stage.classList.add('sky-ready'); draw();
    };
    image.onerror = () => { ready = false; textureMobile = null; stage.classList.remove('sky-ready'); };
    image.src = mobile ? stage.dataset.mobile : stage.dataset.desktop;
  }
  let seed = 7321;
  function random() { seed = seed * 16807 % 2147483647; return (seed - 1) / 2147483646; }
  function makeStars() {
    seed = 7321; stars = [];
    const counts = mobile ? [48,14,5] : [115,30,8];
    counts.forEach((count,layer) => {
      for (let i=0;i<count;i++) {
        stars.push({ x:random()*(width+32)-16, y:random()*(height+32)-16,
          layer, radius:[.35,.62,.96][layer]+random()*.28,
          vx:-[.7,3.6,10.5][layer]*(.86+random()*.28),
          vy:[.25,1.2,3.4][layer]*(.86+random()*.28),
          alpha:.20+random()*.55, phase:random()*Math.PI*2 });
      }
    });
  }
  function resize() {
    width = innerWidth; height = innerHeight; mobile = width <= 640;
    const ratio = lowQuality ? .42 : mobile ? .65 : .75;
    canvas.width = Math.round(width*ratio); canvas.height = Math.round(height*ratio);
    const dpr = Math.min(devicePixelRatio,1.5);
    starCanvas.width = Math.round(width*dpr); starCanvas.height = Math.round(height*dpr);
    context?.setTransform(dpr,0,0,dpr,0,0);
    if (gl) gl.viewport(0,0,canvas.width,canvas.height);
    makeStars(); loadArt(); draw();
  }
  function drawStars(dt) {
    if (!context) return;
    context.clearRect(0,0,width,height);
    for (const star of stars) {
      star.x += star.vx*dt; star.y += star.vy*dt;
      if(star.x < -16) star.x = width+16;
      if(star.y > height+16) star.y = -16;
      // Stable points, not crosses, halos, confetti or breathing bubbles.
      context.globalAlpha = star.alpha * (.92+.08*Math.sin(clock*.26+star.phase));
      context.fillStyle = star.layer === 2 ? '#eff3f8' : '#cedce9';
      context.beginPath(); context.arc(star.x,star.y,star.radius,0,Math.PI*2); context.fill();
    }
    context.globalAlpha = 1;
  }
  function draw(dt=0) {
    if(gl && ready) {
      gl.uniform1f(timeLocation,clock); gl.uniform2f(sizeLocation,width,height);
      gl.drawArrays(gl.TRIANGLES,0,6);
    }
    drawStars(dt); stage.dataset.frames = String(++frames);
  }
  function tick(now) {
    animation = 0;
    if(document.hidden || userPaused || reduced.matches || capture) return;
    if(now-last >= 1000/(mobile ? 30 : 40)) {
      const dt = Math.min((now-last)/1000,.08); last = now; clock += dt;
      const start = performance.now(); draw(dt);
      averageCost = averageCost*.95+(performance.now()-start)*.05;
      if(!lowQuality && averageCost>22 && frames>80) { lowQuality=true; resize(); }
    }
    animation = requestAnimationFrame(tick);
  }
  function syncMotion() {
    cancelAnimationFrame(animation); animation = 0; last = performance.now();
    const still = userPaused || reduced.matches || capture;
    stage.classList.toggle('sky-static',still);
    stage.classList.toggle('sky-paused',document.hidden || still);
    stage.dataset.motion = still ? 'static' : document.hidden ? 'paused' : 'running';
    if (toggle) {
      toggle.hidden = reduced.matches;
      toggle.setAttribute('aria-pressed',String(userPaused));
      toggle.textContent = userPaused ? '開啟背景動態' : '暫停背景動態';
    }
    if(!still && !document.hidden) animation = requestAnimationFrame(tick); else draw();
  }
  toggle?.addEventListener('click',() => {
    userPaused = !userPaused;
    try { sessionStorage.setItem('yuce-motion-paused',String(userPaused)); } catch (_) { /* Continue without persistence. */ }
    syncMotion();
  });
  initialise(); resize(); syncMotion();
  let resizeTimer;
  addEventListener('resize',() => { clearTimeout(resizeTimer); resizeTimer=setTimeout(resize,120); },{passive:true});
  document.addEventListener('visibilitychange',syncMotion);
  reduced.addEventListener('change',syncMotion);
  canvas.addEventListener('webglcontextlost',event => {
    event.preventDefault(); gl=null; ready=false; stage.classList.remove('sky-ready'); stage.dataset.renderer='css-fallback';
  });
})();

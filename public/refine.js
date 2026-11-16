(() => {
  'use strict';
  const panels = [...document.querySelectorAll('[data-guide-panel]')];
  if (!panels.length) return;
  let frame = 0;
  function update() {
    frame = 0;
    for (const panel of panels) {
      if (panel.hidden) continue;
      const system = panel.dataset.guidePanel;
      const steps = [...panel.querySelectorAll('article.guide-step-panel')];
      if (!steps.length) continue;
      const offset = (document.getElementById('header')?.getBoundingClientRect().bottom || 70) + 90;
      let index = 0;
      steps.forEach((step, i) => { if (step.getBoundingClientRect().top <= offset) index = i; });
      const label = steps[index].querySelector('.kicker')?.textContent.trim().replace(/^\d+\s*[／/]\s*/, '') || '';
      const next = steps[index + 1]?.querySelector('.kicker')?.textContent.trim().replace(/^\d+\s*[／/]\s*/, '');
      const progress = panel.querySelector('[data-refine-progress]');
      const text = `目前：第 ${index + 1}／${steps.length} 步 · ${label}${next ? `　下一步：${next}` : '　已到最後一步，請完成核對。'}`;
      if (progress && progress.textContent !== text) {
        progress.textContent = text;
        progress.dataset.currentStep = String(index + 1);
      }
      panel.querySelectorAll('.guide-sidebar a[href^="#"]').forEach((a, i) => {
        if (i === index) a.setAttribute('aria-current', 'step');
        else a.removeAttribute('aria-current');
      });
      panel.dataset.currentStep = String(index + 1);
    }
  }
  function schedule() { if (!frame) frame = requestAnimationFrame(update); }
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  addEventListener('hashchange', schedule);
  document.querySelectorAll('[data-guide]').forEach(tab => tab.addEventListener('click', schedule));
  const observer = new MutationObserver(schedule);
  panels.forEach(panel => observer.observe(panel, {attributes:true,attributeFilter:['hidden']}));
  update();
})();

(() => {
  'use strict';
  const dialog = document.getElementById('welcomeDialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const params = new URLSearchParams(location.search);
  const force = params.get('welcome') === '1';
  if (!force && (params.get('capture') === '1' || params.get('welcome') === '0')) return;
  let seen = false;
  try { seen = sessionStorage.getItem('yuceEntrySeen:premium-v3') === 'true'; } catch (_) { /* Optional storage. */ }
  if (seen && !force) return;
  let previousFocus = null;
  function close() {
    document.body.classList.remove('welcome-open');
    if (dialog.open) dialog.close();
  }
  dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab' || !dialog.open) return;
    const controls = Array.from(dialog.querySelectorAll('button,a[href]')).filter(element => element instanceof HTMLElement && element.getBoundingClientRect().height > 0);
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  });
  dialog.querySelectorAll('[data-welcome-close]').forEach(button => button.addEventListener('click', close));
  dialog.querySelector('[data-line-link]')?.addEventListener('click', close);
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('welcome-open');
    if (previousFocus?.isConnected && typeof previousFocus.focus === 'function') previousFocus.focus({preventScroll:true});
  });
  setTimeout(() => {
    if (dialog.open) return;
    previousFocus = document.activeElement;
    try {
      dialog.showModal();
      document.body.classList.add('welcome-open');
      try { sessionStorage.setItem('yuceEntrySeen:premium-v3', 'true'); } catch (_) { /* Site stays usable. */ }
    } catch (_) { /* Native dialog failure must not prevent reading the website. */ }
  }, 500);
})();

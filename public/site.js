(() => {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const capture = new URLSearchParams(location.search).get('capture') === '1';
  if (capture) {
    $$('img').forEach((image) => { image.loading = 'eager'; image.decoding = 'sync'; });
    document.body.classList.add('capture-mode');
  }
  const menu = $('#mobileNav'), toggle = $('#menuToggle');
  function setMenu(open) {
    if (!menu || !toggle) return;
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '關閉選單' : '開啟選單');
    if (open) menu.querySelector('a')?.focus({preventScroll:true});
    else if (menu.contains(document.activeElement)) toggle.focus({preventScroll:true});
  }
  toggle?.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  menu?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
  window.addEventListener('resize', () => { if (innerWidth > 980) setMenu(false); }, {passive:true});
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  let scheduled = false;
  const updateHeader = () => { $('#header')?.classList.toggle('is-scrolled', scrollY > 20); scheduled = false; };
  window.addEventListener('scroll', () => { if (!scheduled) { requestAnimationFrame(updateHeader); scheduled = true; } }, {passive:true});
  updateHeader();

  const viewer = $('#imageViewer'), image = $('#viewerImage');
  let opener = null;
  function imageState(loading, failed = false) {
    if ($('#viewerLoading')) $('#viewerLoading').hidden = !loading;
    if ($('#viewerError')) $('#viewerError').hidden = !failed;
    image?.setAttribute('aria-busy', String(loading));
  }
  image?.addEventListener('load', () => imageState(false));
  image?.addEventListener('error', () => imageState(false, true));
  $$('[data-image]').forEach((link) => link.addEventListener('click', (e) => {
    if (!viewer || !image || typeof viewer.showModal !== 'function') return;
    e.preventDefault(); opener = link;
    imageState(true);
    if ($('#viewerOriginal')) $('#viewerOriginal').href = link.dataset.image;
    image.src = link.dataset.image; image.alt = link.dataset.title || '真實產品介面';
    $('#viewerTitle').textContent = image.alt;
    viewer.showModal(); document.body.classList.add('viewer-open');
    $('.viewer-scroll')?.scrollTo(0, 0); $('#viewerClose')?.focus();
  }));
  $('#viewerClose')?.addEventListener('click', () => viewer?.close());
  viewer?.addEventListener('click', (e) => { if (e.target === viewer) viewer.close(); });
  viewer?.addEventListener('close', () => { imageState(false); document.body.classList.remove('viewer-open'); opener?.focus(); });

  const tabs = $$('[data-tab]');
  function activateTab(tab) {
    const group = tab.closest('[role=tablist]');
    Array.from(group?.querySelectorAll('[data-tab]') || []).forEach((t) => {
      const active = t === tab; t.setAttribute('aria-selected', String(active)); t.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(t.getAttribute('aria-controls') || 'focus-' + t.dataset.tab);
      if (panel) panel.hidden = !active;
    });
  }
  function keyboardTab(e, list, index, activate) {
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(e.key)) return;
    e.preventDefault();
    const next = e.key === 'Home' ? 0 : e.key === 'End' ? list.length - 1 : (index + (e.key === 'ArrowRight' ? 1 : -1) + list.length) % list.length;
    list[next].focus(); activate(list[next]);
  }
  tabs.forEach((t) => {
    const group = Array.from(t.closest('[role=tablist]')?.querySelectorAll('[data-tab]') || []);
    t.addEventListener('click', () => activateTab(t));
    t.addEventListener('keydown', (e) => keyboardTab(e, group, group.indexOf(t), activateTab));
  });
  $$('[role=tablist]').forEach((group) => {
    const initial = group.querySelector('[data-tab][aria-selected=true]') || group.querySelector('[data-tab]');
    if (initial) activateTab(initial);
  });

  const guides = $$('[data-guide]');
  function selectGuide(name, updateUrl = false) {
    if (!['matrix','auto'].includes(name) || !guides.length) return;
    guides.forEach((tab) => {
      const active = tab.dataset.guide === name;
      tab.setAttribute('aria-selected', String(active)); tab.tabIndex = active ? 0 : -1;
      const panel = $('#guide-panel-' + tab.dataset.guide), preview = $('#guide-preview-' + tab.dataset.guide);
      if (panel) panel.hidden = !active; if (preview) preview.hidden = !active;
    });
    document.body.dataset.guideSystem = name;
    const currentPanel = document.getElementById('guide-panel-' + name);
    if (currentPanel) updateGuideProgress(currentPanel, currentPanel.querySelector('[data-guide-step][open]'));
    if (updateUrl) { const url = new URL(location.href); url.searchParams.set('system', name); url.hash = ''; history.replaceState(null, '', url.pathname + url.search); }
  }
  function updateGuideProgress(panel, step) {
    if (!step) return;
    const steps = Array.from(panel.querySelectorAll('[data-guide-step]'));
    const index = steps.indexOf(step), status = panel.querySelector('[data-guide-progress]');
    if (index < 0 || !status) return;
    const shortTitle = (item) => item?.querySelector('summary .kicker')?.textContent.trim().replace(/^\d+\s*[／/]/, '') || '';
    status.textContent = `目前：第 ${index + 1}／${steps.length} 步 · ${shortTitle(step)}。` +
      (steps[index + 1] ? ` 下一步：${shortTitle(steps[index + 1])}。` : ' 已到最後一步，請核對設定與風險再進入系統。');
    panel.dataset.currentStep = String(index + 1);
    panel.querySelectorAll('.guide-sidebar a[href^="#"]').forEach((link) => {
      if (link.getAttribute('href') === '#' + step.id) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
  }
  function openHashTarget(scroll = true) {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let detail = target.closest('details');
    while (detail) { detail.open = true; detail = detail.parentElement?.closest('details'); }
    const panel = target.closest('[data-guide-panel]');
    if (panel) updateGuideProgress(panel, target.closest('[data-guide-step]'));
    if (scroll) requestAnimationFrame(() => target.scrollIntoView({behavior:'auto', block:'start'}));
  }
  function syncGuide() {
    selectGuide(location.hash.startsWith('#auto-step') ? 'auto' : location.hash.startsWith('#matrix-step') ? 'matrix' : new URLSearchParams(location.search).get('system') === 'auto' ? 'auto' : 'matrix');
    openHashTarget();
  }
  guides.forEach((tab, i) => {
    tab.addEventListener('click', () => selectGuide(tab.dataset.guide, true));
    tab.addEventListener('keydown', (e) => keyboardTab(e, guides, i, (next) => selectGuide(next.dataset.guide, true)));
  });
  if (guides.length) {
    syncGuide(); window.addEventListener('hashchange', syncGuide); window.addEventListener('popstate', syncGuide);
    if (location.hash) requestAnimationFrame(() => document.getElementById(location.hash.slice(1))?.scrollIntoView({behavior:'auto',block:'start'}));
  }
  else {
    openHashTarget();
    window.addEventListener('hashchange', () => openHashTarget());
  }
  $$('details[data-guide-step]').forEach((step) => step.addEventListener('toggle', () => {
    const panel = step.closest('[data-guide-panel]');
    if (step.open && panel) updateGuideProgress(panel, step);
  }));
  $$('[data-next-step]').forEach((link) => link.addEventListener('click', (event) => {
    const target = document.getElementById(link.dataset.nextStep || link.hash.slice(1));
    if (!target) return;
    event.preventDefault();
    const current = link.closest('details[data-guide-step]');
    if (current && innerWidth <= 640) current.open = false;
    location.hash = target.id;
    openHashTarget();
    target.querySelector('summary')?.focus({preventScroll:true});
  }));
  const responsiveDetails = $$('.qr-disclosure,[data-phone-collapse]');
  if (responsiveDetails.length) {
    const phone = matchMedia('(max-width:640px)');
    const syncQr = () => { responsiveDetails.forEach(detail => { detail.open = !phone.matches; }); };
    syncQr(); phone.addEventListener('change', syncQr);
  }
  const search = $('#faqSearch');
  let faqCategory = '';
  function filterFaq() {
    if (!search) return;
    const q = search.value.trim().toLocaleLowerCase(); let count = 0;
    $$('.faq-item').forEach((item) => { const visible = (!faqCategory || item.dataset.faqCategory === faqCategory) && item.textContent.toLocaleLowerCase().includes(q); item.hidden = !visible; if (visible) count++; });
    const empty = $('#faqEmpty'), status = $('#faqCount');
    if (empty) empty.hidden = count > 0; if (status) status.textContent = `顯示 ${count} 個問題`;
    $$('[data-faq-filter]').forEach((a) => a.setAttribute('aria-current', (a.dataset.faqFilter || '') === faqCategory ? 'true' : 'false'));
  }
  search?.addEventListener('input', () => { faqCategory = ''; filterFaq(); });
  $$('[data-faq-filter]').forEach((a) => a.addEventListener('click', () => { if (!search) return; faqCategory = a.dataset.faqFilter || ''; search.value = ''; filterFaq(); requestAnimationFrame(() => search.focus({preventScroll:true})); }));
  filterFaq();
  $$('.section-nav a[href^="#"], .guide-sidebar a[href^="#"], .guide-layout aside a[href^="#"]').forEach((a) => a.addEventListener('click', () => { a.parentElement?.querySelectorAll('a').forEach((item) => item.removeAttribute('aria-current')); a.setAttribute('aria-current','location'); }));
  // Reading content is immediately visible, regardless of observer/GPU availability.
  $$('[data-reveal]').forEach((element) => { element.classList.add('is-visible'); });
})();

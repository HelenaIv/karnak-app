// Registers the offline service worker and shows the guide's offline status in the header.
(function () {
  if (!('serviceWorker' in navigator)) return;
  const L = window.KARNAK_LANG;
  const T = L === 'nb'
    ? { saving: p => `↓ ${p}%`, ready: '✓ Offline', fail: '! Offline', savingL: 'Lagrer guiden for bruk uten nett', readyL: 'Hele guiden er lagret på denne enheten og virker uten internett', failL: 'Offline-kopien er ikke ferdig – åpne guiden igjen med internett' }
    : L === 'uk'
    ? { saving: p => `↓ ${p}%`, ready: '✓ Офлайн', fail: '! Офлайн', savingL: 'Завантаження для офлайн-доступу', readyL: 'Увесь путівник збережено на пристрої й доступний без інтернету', failL: 'Офлайн-копія не завершена — відкрийте путівник з інтернетом' }
    : { saving: p => `↓ ${p}%`, ready: '✓ Offline', fail: '! Offline', savingL: 'Saving the guide for offline use', readyL: 'The whole guide is saved on this device and works without internet', failL: 'Offline copy not finished — open the guide again with internet' };

  const badge = document.createElement('span');
  badge.id = 'offline-status';
  badge.setAttribute('role', 'status');
  badge.style.cssText = 'font:11px/1.2 Arial,sans-serif;padding:3px 7px;border-radius:10px;white-space:nowrap;background:#e9e3d3;color:#273a30';
  const place = () => {
    const tools = document.querySelector('.header-tools');
    if (tools && !badge.isConnected) tools.prepend(badge);
  };
  const show = (text, ok, label) => {
    badge.textContent = text;
    badge.title = label; badge.setAttribute('aria-label', label);
    badge.style.background = ok ? '#dbe8dc' : '#e9e3d3';
    place();
  };

  navigator.serviceWorker.addEventListener('message', e => {
    const m = e.data || {};
    if (m.type === 'progress') show(T.saving(Math.floor(100 * m.done / m.total)), false, T.savingL);
    if (m.type === 'ready') show(T.ready, true, T.readyL);
    if (m.type === 'pending' && !navigator.onLine) show(T.fail, false, T.failL);
  });

  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').then(reg => {
      if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
      const ask = () => navigator.serviceWorker.controller && navigator.serviceWorker.controller.postMessage('status');
      ask();
      navigator.serviceWorker.addEventListener('controllerchange', ask);
      reg.addEventListener('updatefound', () => show(T.saving(0), false, T.savingL));
    }).catch(() => show(T.fail, false, T.failL));
  });
})();

/* Piyush Kumar Soni portfolio: mobile menu + privacy-friendly click hooks. No third-party code. */
(function () {
  var d = document;
  d.documentElement.classList.remove('no-js');
  d.documentElement.classList.add('js');

  var btn = d.querySelector('.menu-btn');
  var nav = d.querySelector('.nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('.label').textContent = open ? 'Close' : 'Menu';
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.querySelector('.label').textContent = 'Menu';
        btn.focus();
      }
    });
  }

  /* Click tracking hooks. Nothing is sent unless an analytics tool is added later.
     Supported if present: Plausible, GoatCounter, GA4 (gtag) or any dataLayer. */
  d.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-track]') : null;
    if (!el) return;
    var name = el.getAttribute('data-track');
    var label = el.getAttribute('href') || '';
    try {
      if (window.plausible) window.plausible(name, { props: { target: label } });
      if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: 'click-' + name, title: label, event: true });
      if (window.gtag) window.gtag('event', name, { link_url: label });
      if (window.dataLayer && window.dataLayer.push) window.dataLayer.push({ event: name, link_url: label });
    } catch (err) { /* never block navigation */ }
  });

  var y = d.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

/* Scroll fade-in, as on the original site */
(function () {
  var els = document.querySelectorAll('.fade-in');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  els.forEach(function (el) { io.observe(el); });
})();

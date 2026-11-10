// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');

  function setOpen(open) {
    if (!links || !toggle) return;
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  if (toggle && links) {
    if (!toggle.hasAttribute('aria-controls')) {
      toggle.setAttribute('aria-controls', 'primary-navigation');
    }
    setOpen(false);
    toggle.addEventListener('click', function () {
      setOpen(!links.classList.contains('open'));
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  // Accordion (only used if a page includes .accordion-item markup)
  document.querySelectorAll('.accordion-trigger').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.accordion-item');
      var panel = item.querySelector('.accordion-panel');
      var isOpen = item.classList.contains('open');

      document.querySelectorAll('.accordion-item.open').forEach(function (other) {
        if (other !== item) {
          other.classList.remove('open');
          other.querySelector('.accordion-panel').style.maxHeight = null;
          other.querySelector('.accordion-trigger').setAttribute('aria-expanded', 'false');
        }
      });

      if (isOpen) {
        item.classList.remove('open');
        panel.style.maxHeight = null;
        btn.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Open an accordion item from the URL hash (guarded: an invalid hash must not throw)
  if (window.location.hash) {
    try {
      var target = document.querySelector(window.location.hash);
      if (target && target.classList.contains('accordion-item')) {
        target.querySelector('.accordion-trigger').click();
        setTimeout(function () { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 120);
      }
    } catch (err) { /* ignore invalid selectors */ }
  }

  // Theme toggle (light/dark). The actual theme is set before paint by a
  // small inline script in <head> (reads localStorage, falls back to the
  // OS preference) so there's no flash of the wrong theme on load — this
  // just wires up the button to flip it afterwards.
  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    var root = document.documentElement;
    function describeTheme(theme) {
      themeBtn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      themeBtn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    }
    describeTheme(root.getAttribute('data-theme') || 'light');
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      describeTheme(next);
      try { localStorage.setItem('jil-theme', next); } catch (err) { /* private browsing etc. */ }
    });
  }

  // Animated stat counters (home page "Jopetnah at a glance" band).
  // Falls back to the real static numbers already in the HTML if JS
  // doesn't run, and skips the animation outright for reduced-motion.
  var counters = document.querySelectorAll('.stats-band .counter');
  if (counters.length) {
    var prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var band = document.querySelector('.stats-band');

    function runCounters() {
      counters.forEach(function (el) {
        var target = parseInt(el.getAttribute('data-target'), 10);
        if (isNaN(target)) return;
        var duration = 900;
        var startTime = null;
        function step(ts) {
          if (!startTime) startTime = ts;
          var progress = Math.min((ts - startTime) / duration, 1);
          el.textContent = Math.floor(progress * target);
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            el.textContent = target;
          }
        }
        el.textContent = '0';
        requestAnimationFrame(step);
      });
    }

    if (!prefersReducedMotion && band && 'IntersectionObserver' in window) {
      var counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            runCounters();
            counterObserver.disconnect();
          }
        });
      }, { threshold: 0.4 });
      counterObserver.observe(band);
    }
    // If reduced motion is preferred, or there's no IntersectionObserver
    // support, the real numbers already in the HTML are left exactly as
    // they are -- nothing further to do.
  }

  // Contact form: pre-select the service dropdown from ?sector=NN, which is set by
  // the "Discuss this sector" buttons on the Services page. An invalid or unknown
  // value is ignored and the dropdown simply stays on its default.
  (function () {
    try {
      var select = document.getElementById('service');
      if (!select || !window.URLSearchParams) return;
      var id = new URLSearchParams(window.location.search).get('sector');
      if (!id || !/^\d{2}$/.test(id)) return;
      var opt = select.querySelector('option[data-sector="' + id + '"]');
      if (opt) select.value = opt.value;
    } catch (err) { /* leave the default selection */ }
  })();

  // Collapsible groups (About page): one button expands or collapses every section in the group.
  // Added by script, so without JavaScript each section still opens and closes on its own.
  (function () {
    try {
      document.querySelectorAll('.exec-body').forEach(function (group) {
        var items = group.querySelectorAll('details.collapsible');
        if (items.length < 2) return;
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'collapsible-toggle';
        function allOpen() { return Array.prototype.every.call(items, function (d) { return d.open; }); }
        function sync() {
          var open = allOpen();
          btn.textContent = open ? 'Collapse all sections' : 'Expand all sections';
          btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        }
        btn.addEventListener('click', function () {
          var open = !allOpen();
          items.forEach(function (d) { d.open = open; });
          sync();
        });
        items.forEach(function (d) { d.addEventListener('toggle', sync); });
        items[0].parentNode.insertBefore(btn, items[0]);
        sync();
      });
    } catch (err) { /* leave the sections as plain collapsibles */ }
  })();
});

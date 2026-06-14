/* ============================================================
   deck.js — 跨頁進場動效與互動引擎（vanilla，無依賴）
   reveal(stagger) · count-up · 進度條 · 視差 · 複製鈕 · 列印 finalize
   各頁專屬互動（試算器等）留在各檔內嵌 <script>，不在此檔。
   ============================================================ */
(function () {
  "use strict";

  var motionOK = !window.matchMedia ||
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var doc = document;

  /* ---------- 進度條 ---------- */
  var progress = doc.getElementById('progress') || doc.querySelector('.progress');
  if (progress) {
    var onScroll = function () {
      var h = doc.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var p = max > 0 ? (h.scrollTop || doc.body.scrollTop) / max : 0;
      progress.style.width = (p * 100).toFixed(2) + '%';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- reveal（stagger 進場） ---------- */
  var revEls = [].slice.call(doc.querySelectorAll('[data-reveal]'));
  if (motionOK && hasIO && revEls.length) {
    doc.documentElement.classList.add('anim');
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
    revEls.forEach(function (el) { io.observe(el); });
    // 安全網：慢速 / headless 算繪時不留白
    setTimeout(function () { revEls.forEach(function (el) { el.classList.add('in'); }); fillBars(); }, 2800);
  }

  /* ---------- count-up（[data-count]） ---------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    var dec = (target % 1 !== 0) ? 1 : 0;
    if (!motionOK) { el.textContent = prefix + target.toFixed(dec) + suffix; return; }
    var dur = 1300, start = null;
    el.textContent = prefix + '0' + suffix;
    function tick(ts) {
      if (!start) start = ts;
      var t = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = prefix + (target * eased).toFixed(dec) + suffix;
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = prefix + target.toFixed(dec) + suffix;
    }
    requestAnimationFrame(tick);
  }
  var counts = [].slice.call(doc.querySelectorAll('[data-count]'));
  if (counts.length) {
    if (hasIO) {
      var cio = new IntersectionObserver(function (ents) {
        ents.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); } });
      }, { threshold: 0.6 });
      counts.forEach(function (el) { cio.observe(el); });
    } else counts.forEach(countUp);
  }

  /* ---------- 條狀填充（.bf[data-w] 於 #costBars 或 [data-bars]） ---------- */
  function fillBars() {
    [].slice.call(doc.querySelectorAll('.bf[data-w]')).forEach(function (b) {
      b.style.width = b.getAttribute('data-w') + '%';
    });
  }
  var barWrap = doc.getElementById('costBars') || doc.querySelector('[data-bars]');
  if (barWrap) {
    if (hasIO) {
      var bio = new IntersectionObserver(function (ents) {
        ents.forEach(function (e) { if (e.isIntersecting) { fillBars(); bio.disconnect(); } });
      }, { threshold: 0.3 });
      bio.observe(barWrap);
    } else fillBars();
  }

  /* ---------- 視差（[data-parallax]，rAF 節流） ---------- */
  var pxEls = [].slice.call(doc.querySelectorAll('[data-parallax]'));
  if (motionOK && pxEls.length) {
    var ticking = false;
    var apply = function () {
      var vh = window.innerHeight || doc.documentElement.clientHeight;
      pxEls.forEach(function (el) {
        var speed = parseFloat(el.getAttribute('data-parallax')) || 0.12;
        var r = el.getBoundingClientRect();
        var center = r.top + r.height / 2;
        var off = (center - vh / 2) * -speed;
        // 限幅，維持精緻不誇張
        if (off > 90) off = 90; else if (off < -90) off = -90;
        el.style.setProperty('--parallax', off.toFixed(1) + 'px');
      });
      ticking = false;
    };
    var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(apply); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req, { passive: true });
    apply();
  }

  /* ---------- 複製鈕（.copy-button[data-copy] 或就近 <pre>） ---------- */
  [].slice.call(doc.querySelectorAll('.copy-button')).forEach(function (btn) {
    btn.addEventListener('click', function () {
      var sel = btn.getAttribute('data-copy');
      var src = sel ? doc.querySelector(sel) : null;
      if (!src) {
        var card = btn.closest('.code-card') || btn.parentElement;
        src = card ? card.querySelector('pre, code') : null;
      }
      var text = src ? (src.innerText || src.textContent) : '';
      var done = function () {
        var label = btn.getAttribute('data-label') || btn.textContent;
        btn.setAttribute('data-label', label);
        btn.classList.add('copied');
        btn.textContent = '已複製 ✓';
        setTimeout(function () { btn.classList.remove('copied'); btn.textContent = label; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = doc.createElement('textarea');
        ta.value = text; doc.body.appendChild(ta); ta.select();
        try { doc.execCommand('copy'); } catch (e) {}
        doc.body.removeChild(ta); done();
      }
    });
  });

  /* ---------- 列印 finalize（白底黑字 + 展開 details + 全顯） ---------- */
  function setDetailsOpen(open) {
    [].slice.call(doc.querySelectorAll('details.q, details.faq')).forEach(function (d) {
      if (open) {
        if (!d.hasAttribute('data-wasopen')) d.setAttribute('data-wasopen', d.open ? '1' : '0');
        d.open = true;
      } else {
        d.open = d.getAttribute('data-wasopen') === '1';
        d.removeAttribute('data-wasopen');
      }
    });
  }
  function finalizeForPrint() {
    revEls.forEach(function (e) { e.classList.add('in'); });
    fillBars();
    setDetailsOpen(true);
  }
  window.addEventListener('beforeprint', finalizeForPrint);
  window.addEventListener('afterprint', function () { setDetailsOpen(false); });
  if (window.matchMedia) {
    var mqp = window.matchMedia('print');
    var onmq = function (e) { if (e.matches) finalizeForPrint(); else setDetailsOpen(false); };
    if (mqp.addEventListener) mqp.addEventListener('change', onmq);
    else if (mqp.addListener) mqp.addListener(onmq);
  }
})();

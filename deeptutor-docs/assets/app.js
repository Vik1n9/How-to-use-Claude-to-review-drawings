/* DeepTutor 改寫版 · docs shell behavior (vanilla, zero deps) */
(function () {
  "use strict";

  /* ---------- sidebar: keep active item in view ---------- */
  var current = document.querySelector('.side-item[aria-current="page"]');
  if (current && current.scrollIntoView) {
    try { current.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (e) {}
  }

  /* ---------- search ---------- */
  var layer = document.getElementById("searchLayer");
  var input = document.getElementById("searchInput");
  var list = document.getElementById("searchResults");
  var trigger = document.getElementById("searchTrigger");
  if (!layer || !input || !list || !trigger) return;

  var INDEX = null;
  var results = [];
  var selected = -1;
  var ROOTURL = trigger.getAttribute("data-root") || "";

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function ensureIndex() {
    if (INDEX) return Promise.resolve(INDEX);
    var url = trigger.getAttribute("data-index");
    return fetch(url).then(function (r) { return r.json(); }).then(function (j) {
      INDEX = j.pages || [];
      return INDEX;
    });
  }

  function snippet(text, q) {
    var i = text.indexOf(q);
    if (i < 0) i = 0;
    var start = Math.max(0, i - 40);
    var frag = text.slice(start, Math.min(text.length, start + 130));
    return frag;
  }

  function mark(s, q) {
    if (!q) return esc(s);
    var out = "";
    var lower = s.toLowerCase(), ql = q.toLowerCase(), i = 0;
    while (true) {
      var j = lower.indexOf(ql, i);
      if (j < 0) { out += esc(s.slice(i)); break; }
      out += esc(s.slice(i, j)) + "<mark>" + esc(s.slice(j, j + q.length)) + "</mark>";
      i = j + q.length;
    }
    return out;
  }

  function search(q) {
    q = q.trim();
    if (!q) { render([]); return; }
    var ql = q.toLowerCase();
    var scored = [];
    for (var i = 0; i < INDEX.length; i++) {
      var p = INDEX[i];
      var score = 0;
      var hay = null;
      if (p.t.toLowerCase().indexOf(ql) >= 0) score += 50;
      if (p.s.toLowerCase().indexOf(ql) >= 0) score += 10;
      for (var h = 0; h < p.h.length; h++) {
        if (p.h[h].toLowerCase().indexOf(ql) >= 0) { score += 20; break; }
      }
      var pos = p.x.indexOf(q) >= 0 ? p.x.indexOf(q) : p.x.toLowerCase().indexOf(ql);
      if (pos >= 0) { score += 5; hay = p.x.slice(Math.max(0, pos - 40), pos + 90); }
      if (score > 0) scored.push({ p: p, score: score, hay: hay || p.x.slice(0, 90) });
    }
    scored.sort(function (a, b) { return b.score - a.score; });
    render(scored.slice(0, 12), q);
  }

  function render(items, q) {
    results = items;
    selected = items.length ? 0 : -1;
    if (!q) { list.innerHTML = '<li class="search-empty">輸入關鍵字，搜尋全部 50 篇文件。</li>'; return; }
    if (!items.length) { list.innerHTML = '<li class="search-empty">沒有符合「' + esc(q) + '」的結果。</li>'; return; }
    var html = "";
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      html += '<li><a href="' + ROOTURL + it.p.u + '" aria-selected="' + (i === selected) + '" data-i="' + i + '">'
        + '<span class="r-section">' + esc(it.p.s) + '</span>'
        + '<span class="r-title">' + mark(it.p.t, q) + '</span>'
        + '<span class="r-snip">' + mark(it.hay, q) + '</span>'
        + '</a></li>';
    }
    list.innerHTML = html;
  }

  function moveSelection(delta) {
    if (!results.length) return;
    selected = (selected + delta + results.length) % results.length;
    var links = list.querySelectorAll("a");
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute("aria-selected", String(i === selected));
    }
    if (links[selected]) links[selected].scrollIntoView({ block: "nearest" });
  }

  function open() {
    ensureIndex().then(function () {
      layer.hidden = false;
      document.body.style.overflow = "hidden";
      input.value = "";
      search("");
      input.focus();
    });
  }
  function close() {
    layer.hidden = true;
    document.body.style.overflow = "";
  }

  trigger.addEventListener("click", open);
  layer.addEventListener("click", function (e) {
    if (e.target.hasAttribute("data-close")) close();
  });
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault();
      if (layer.hidden) open(); else close();
      return;
    }
    if (layer.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); close(); }
    else if (e.key === "ArrowDown") { e.preventDefault(); moveSelection(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); moveSelection(-1); }
    else if (e.key === "Enter" && selected >= 0 && results[selected]) {
      e.preventDefault();
      location.href = ROOTURL + results[selected].p.u;
      close();
    }
  });
  input.addEventListener("input", function () { search(input.value); });
})();

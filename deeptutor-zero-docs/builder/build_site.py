#!/usr/bin/env python3
"""Build the DeepTutor 零度版 docs site (kami design language) from the
Traditional-Chinese rewrite. Generator + check mode per kami
«Product site system»: fails loudly on unresolved links, missing assets,
leftover source paths, or drift between manifest and output.
"""

import difflib
import html as htmllib
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest  # noqa: E402

import pygments.token as T  # noqa: E402
from pygments.lexers import get_lexer_by_name  # noqa: E402
from pygments.util import ClassNotFound  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent          # DeepTutor 零度版 排版網站
SITE = ROOT / "site"
ASSETS = SITE / "assets"
BUILDER = Path(__file__).resolve().parent
SRC_DIR = ROOT.parent / "DeepTutor 零度版 繁體中文"

SITE_NAME = "DeepTutor 零度版"
ORIGIN = "https://docs.deeptutor.info"
PAGES = manifest.pages_dict()
FLAT = manifest.flat_pages()
ORIG_DIR = ROOT.parent / "DeepTutor 原始文檔"

# anchor slugs on the ORIGINAL site are simplified-Chinese; our headings are
# Traditional. Translate by position: orig heading order -> new heading order.
ORIG_SLUGS = {}   # slug -> [slugified simplified h2/h3 texts, in order]


def slugify(text):
    t = re.sub(r"\s+", "-", text.strip()).lower()
    return re.sub(r"[^\w\u4e00-\u9fff\-]", "", t, flags=re.UNICODE)


def load_orig_slugs():
    for slug in PAGES:
        p = ORIG_DIR / manifest.source_path(slug)
        if not p.exists():
            continue
        heads = []
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
            if m:
                heads.append(slugify(re.sub(r"[*`]", "", m.group(1))))
        ORIG_SLUGS[slug] = heads


def skel(s):
    return re.sub(r"[^a-z0-9-]", "", s.lower())


def pair_ok(a, b):
    ka, kb = skel(a), skel(b)
    if ka and ka == kb:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.35


def align_fmap(orig, new):
    """orig simplified slugs -> new ids. The rewrite renames headings
    (traditional wording, step numbers) and inserts new ones, so align with a
    monotonic LCS over a loose equality (ASCII skeleton or char ratio >= .35)."""
    n, m = len(orig), len(new)
    if not n or not m:
        return {}, None
    eq = [[pair_ok(orig[i], new[j]) for j in range(m)] for i in range(n)]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            best = max(dp[i + 1][j], dp[i][j + 1])
            if eq[i][j]:
                best = max(best, 1 + dp[i + 1][j + 1])
            dp[i][j] = best
    pairs = {}
    i = j = 0
    while i < n and j < m:
        if eq[i][j] and dp[i][j] == 1 + dp[i + 1][j + 1]:
            pairs[i] = j
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1
        else:
            j += 1
    fmap = {orig[a]: new[b] for a, b in pairs.items()}
    miss = n - len(pairs)
    return fmap, (f"{miss}/{n} headings unmatched in alignment" if miss else None)


# ---------------------------------------------------------------- front-matter

def parse_front_matter(md_text):
    m = re.match(r"\A---\n(.*?)\n---\n", md_text, re.S)
    meta = {"title": "", "url": "", "description": ""}
    if not m:
        return meta, md_text
    raw = m.group(1)
    for line in raw.splitlines():
        lm = re.match(r"(title|url|description)\s*:\s*(.*)\s*$", line)
        if lm:
            meta[lm.group(1)] = lm.group(2).strip().strip('"').strip("'")
    return meta, md_text[m.end():]


# ---------------------------------------------------------------- pandoc

def pandoc(md_body):
    p = subprocess.run(
        ["pandoc", "-f", "markdown+raw_html+autolink_bare_uris-smart",
         "-t", "html", "--no-highlight", "--wrap=none"],
        input=md_body, capture_output=True, text=True, check=True,
    )
    return p.stdout


# ---------------------------------------------------------------- code highlight

def tclass(t):
    if t in T.Comment: return "c"
    if t in T.Keyword: return "k"
    if t in T.String: return "s"
    if t in T.Number: return "m"
    if t in T.Name.Function: return "nf"
    if t in T.Name.Class: return "nc"
    if t in T.Name.Builtin: return "nb"
    if t in T.Name.Constant: return "nb"
    if t in T.Name.Decorator: return "nd"
    if t in T.Name.Tag: return "nt"
    if t in T.Generic: return None
    return None


LANG_MAP = {"bash": "bash", "shell": "bash", "sh": "bash", "console": "bash",
            "json": "json", "python": "python", "py": "python",
            "yaml": "yaml", "yml": "yaml", "javascript": "javascript",
            "js": "javascript"}

# pages whose section headers were rewritten as standalone bold paragraphs
BOLD_HEADER_PAGES = {"explore/partners", "explore/reading", "explore/subagents",
                     "explore/space", "explore/settings"}


def highlight_code(code, lang):
    lang = LANG_MAP.get((lang or "").lower())
    if not lang:
        return None
    try:
        lexer = get_lexer_by_name(lang, stripnl=False, ensurenl=False)
    except ClassNotFound:
        return None
    out, cur, buf = [], None, ""
    for ttype, value in lexer.get_tokens(code):
        c = tclass(ttype)
        if c == cur:
            buf += value
            continue
        if buf:
            out.append(f'<span class="{cur}">{htmllib.escape(buf, quote=False)}</span>' if cur
                       else htmllib.escape(buf, quote=False))
        cur, buf = c, value
    if buf:
        out.append(f'<span class="{cur}">{htmllib.escape(buf, quote=False)}</span>' if cur
                   else htmllib.escape(buf, quote=False))
    return "".join(out).rstrip("\n")


CODE_RE = re.compile(r"<pre([^>]*)>\s*<code([^>]*)>(.*?)</code>\s*</pre>", re.S)


def _lang_of(attrs):
    m = re.search(r'class="(?:language-|sourceCode[ \-])?([\w+#.-]+)[^"]*"', attrs or "")
    if not m:
        return None
    return m.group(1).rstrip(".")


def rebuild_codeblocks(body):
    def repl(m):
        pre_attrs, code_attrs, escaped = m.group(1), m.group(2), m.group(3)
        lang = _lang_of(pre_attrs) or _lang_of(code_attrs)
        raw = htmllib.unescape(re.sub(r"<[^>]+>", "", escaped))
        baked = highlight_code(raw, lang)
        attrs = f' data-lang="{htmllib.escape(lang, quote=True)}"' if lang else ""
        if baked is None:
            inner = htmllib.escape(raw, quote=False).rstrip("\n")
        else:
            inner = baked
        return f'<div class="codeblock"{attrs}><pre><code>{inner}</code></pre></div>'
    return CODE_RE.sub(repl, body)


# ---------------------------------------------------------------- post-process

SPACER_RE = re.compile(r"<p>(?:&nbsp;|\u00a0|\s*</p>\s*<p(?: [^>]*)?>)\s*</p>")


def postprocess(body, promote_bold=False):
    # the md repeats the title as an H1 inside the body -> drop the first one
    body = re.sub(r"\s*<h1[^>]*>.*?</h1>\s*", " ", body, count=1)
    body = rebuild_codeblocks(body)
    # 原文連結 blockquote -> source note
    m = re.search(r"<blockquote>\s*<p>原文連結：(.*?)</p>\s*</blockquote>", body, re.S)
    if m:
        body = (body[:m.start()] + '<p class="source-note">原文連結：' + m.group(1) + "</p>"
                + body[m.end():])
    # spacer paragraphs -> structural gap
    body = re.sub(r"<p>(?:&nbsp;|\u00a0)</p>", '<div class="gap" aria-hidden="true"></div>', body)
    body = re.sub(r"<p>\s*</p>", "", body)
    # tables -> overflow wrapper
    body = body.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    if promote_bold:
        body = promote_standalone_bolds(body)
    return body


def promote_standalone_bolds(body):
    """**Section header** on its own line -> <h2 id=...> (run-in bolds stay)."""
    taken = set(re.findall(r'id="([^"]+)"', body))

    def repl(m):
        inner = m.group(1)
        text = strip_tags(inner)
        if not text or len(text) > 60:
            return m.group(0)
        hid = slugify(text) or "section"
        base, k = hid, 2
        while hid in taken:
            hid = f"{base}-{k}"
            k += 1
        taken.add(hid)
        return f'<h2 id="{hid}">{inner}</h2>'

    return re.sub(r"<p><strong>(.*?)</strong></p>", repl, body)


def build_toc(body):
    items = []
    last_h2 = None
    for m in re.finditer(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body, re.S):
        level, hid, inner = int(m.group(1)), m.group(2), m.group(3)
        label = re.sub(r"<[^>]+>", "", inner).strip()
        if level == 2:
            last_h2 = {"id": hid, "label": label, "children": []}
            items.append(last_h2)
        else:
            if last_h2 is None:
                last_h2 = {"id": hid, "label": label, "children": []}
                items.append(last_h2)
            else:
                last_h2["children"].append({"id": hid, "label": label})
    if not items:
        return ""
    lines = ['<nav class="toc" aria-label="本頁內容"><p class="toc-label">本頁內容</p><ul>']
    for it in items:
        lines.append(f'<li class="d2"><a href="#{it["id"]}">{htmllib.escape(it["label"])}</a>')
        if it["children"]:
            lines.append("<ul>")
            for ch in it["children"]:
                lines.append(f'<li class="d3"><a href="#{ch["id"]}">{htmllib.escape(ch["label"])}</a></li>')
            lines.append("</ul>")
        lines.append("</li>")
    lines.append("</ul></nav>")
    return "\n".join(lines)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ---------------------------------------------------------------- link rewriting

class LinkRewriter:
    def __init__(self, current_slug, frag_maps, id_lists):
        self.slug = current_slug
        self.depth = current_slug.count("/")
        self.prefix = "../" * self.depth
        self.assets = self.prefix + "assets"
        self.errors = []
        self.warns = []
        self.frag_maps = frag_maps   # target slug -> {orig simplified slug: new id}
        self.id_lists = id_lists     # target slug -> [new ids in order]

    def page_href(self, target_path):
        cand = target_path
        if cand in PAGES:
            return cand
        if cand + "/index" in PAGES:
            return cand + "/index"
        return None

    def translate_frag(self, target, frag):
        dec = urllib.parse.unquote(frag).rstrip("/")
        fmap = self.frag_maps.get(target, {})
        if dec in fmap:
            return fmap[dec]
        # fuzzy: the rewrite localized some anchor slugs (文档->文件 etc.)
        best, ratio = None, 0.0
        for k in fmap:
            r = difflib.SequenceMatcher(None, dec, k).ratio()
            if r > ratio:
                best, ratio = k, r
        if best is not None and ratio >= 0.65:
            return fmap[best]
        # skeleton fallback straight against the target page's real ids
        k = skel(dec)
        if k:
            for s in self.id_lists.get(target, []):
                if skel(s) == k:
                    return s
        self.warns.append(f"anchor #{dec} -> {target}: no match; kept verbatim")
        return dec

    def rewrite(self, body):
        def href_repl(m):
            url = m.group(1)
            frag = ""
            if url.startswith("/zh-cn") or url == "/zh-cn/":
                path = url[len("/zh-cn"):]
                frag = ""
                if "#" in path:
                    path, frag = path.split("#", 1)
                path = path.strip("/")
                if path == "":
                    target = "index"
                elif path == "explore":
                    target = "explore/chat-workspace"   # no overview page in this set
                else:
                    target = self.page_href(path)
                    if target is None:
                        self.errors.append(f"unresolved internal link /zh-cn/{path}/")
                        return m.group(0)
                href = f"{self.prefix}{target}.html"
                if frag:
                    href += "#" + self.translate_frag(target, frag)
                return f'href="{href}"'
            if url.startswith("#"):
                same = self.translate_frag(self.slug, url[1:])
                return f'href="#{same}"'
            if url.startswith("/"):
                self.errors.append(f"unresolved absolute link {url}")
                return m.group(0)
            if url.startswith(("http://", "https://")):
                return f'href="{url}" target="_blank" rel="noopener"'
            return m.group(0)

        body = re.sub(r'href="([^"]+)"', href_repl, body)
        body = re.sub(r'src="(/[^"]+)"', lambda m: f'src="{self.assets}{m.group(1)}"', body)
        return body


# ---------------------------------------------------------------- shell

def sidebar_html(current_slug, prefix):
    groups = []
    for section, items in manifest.SECTIONS:
        links = []
        for slug, label in items:
            href = prefix + slug + ".html"
            cur = ' aria-current="page"' if slug == current_slug else ""
            links.append(f'<a class="side-item" href="{href}"{cur}>{htmllib.escape(label)}</a>')
        groups.append(
            f'<div class="side-group"><p class="side-group-label">{htmllib.escape(section)}</p>'
            + "\n".join(links) + "</div>"
        )
    return "\n".join(groups)


def pager_html(slug, prefix):
    flat = [p[0] for p in FLAT]
    i = flat.index(slug)
    parts = []
    if i > 0:
        prev = FLAT[i - 1]
        parts.append(
            f'<a class="prev" href="{prefix}{prev[0]}.html">'
            f'<p class="pager-eyebrow">上一頁</p><p class="pager-title">{htmllib.escape(prev[1])}</p></a>'
        )
    else:
        parts.append("<span></span>")
    if i < len(flat) - 1:
        nxt = FLAT[i + 1]
        parts.append(
            f'<a class="next" href="{prefix}{nxt[0]}.html">'
            f'<p class="pager-eyebrow">下一頁</p><p class="pager-title">{htmllib.escape(nxt[1])}</p></a>'
        )
    else:
        parts.append("<span></span>")
    return '<nav class="pager" aria-label="上下頁">' + "\n".join(parts) + "</nav>"


SEARCH_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round">'
               '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')


def page_shell(*, slug, section, title, description, toc, body, pager, prefix,
               search_index_href, home_banner=""):
    label, _ = PAGES[slug]
    head_title = f"{title} · {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{htmllib.escape(head_title)}</title>
<meta name="description" content="{htmllib.escape(description)}">
<meta name="generator" content="Kami">
<meta property="og:title" content="{htmllib.escape(head_title)}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_TW">
<link rel="icon" type="image/png" href="{prefix}assets/brand/logo.png">
<link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
<a class="skip-link" href="#main">跳到主要內容</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{prefix}index.html">
      <img class="brand-logo" src="{prefix}assets/brand/logo.png" alt="">
      <span class="brand-name">DeepTutor <em>零度版</em></span>
      <span class="brand-tag">繁體中文文件</span>
    </a>
    <div class="topbar-actions">
      <button class="search-trigger" id="searchTrigger" type="button"
              data-index="{prefix}assets/search-index.json" data-root="{prefix}"
              aria-label="搜尋文件（Ctrl K）">{SEARCH_ICON}<span class="st-label">搜尋</span><kbd>Ctrl K</kbd></button>
      <a class="topbar-link" href="{ORIGIN}/zh-cn/" target="_blank" rel="noopener">原文站</a>
      <a class="topbar-link" href="https://github.com/HKUDS/DeepTutor" target="_blank" rel="noopener">GitHub</a>
    </div>
  </div>
</header>
<div class="shell">
  <aside class="sidebar" id="sidebar" aria-label="文件導覽">
    <nav class="side-nav">
{sidebar_html(slug, prefix)}
    </nav>
  </aside>
  <main class="main" id="main">
    <article class="doc">
      <p class="eyebrow">{htmllib.escape(section)}<span aria-hidden="true"> · </span>{htmllib.escape(label)}</p>
      <h1 class="doc-title">{htmllib.escape(title)}</h1>
      {f'<p class="doc-lede">{htmllib.escape(description)}</p>' if description else ""}
      {home_banner}
      {toc}
      {body}
    </article>
    {pager}
  </main>
</div>
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <img src="{prefix}assets/brand/logo.png" alt="">
      <div>
        <p class="footer-name">DeepTutor <em>零度版</em></p>
        <p class="footer-tagline">開源、agent-native 的個人化學習助手——四種安裝、十六個管道、三層記憶，一套共享執行環境串起全部。</p>
        <p class="footer-ethos">把同一套對話迴圈，帶到你學習的每個角落。</p>
      </div>
    </div>
    <div class="footer-colophon">
      <div class="footer-links">
        <a href="{prefix}index.html">文件主頁</a>
        <a href="{ORIGIN}/zh-cn/" target="_blank" rel="noopener">原文站</a>
        <a href="https://github.com/HKUDS/DeepTutor" target="_blank" rel="noopener">GitHub</a>
        <a href="https://discord.gg/eRsjPgMU4t" target="_blank" rel="noopener">Discord</a>
      </div>
      <p class="footer-legal">本站依官方中文文件零度版改寫重排（繁體中文．台灣用語），僅供學習交流；上游專案由香港大學數據智能實驗室（HKUDS）以 Apache 2.0 開源。</p>
    </div>
  </div>
</footer>
<div class="search-layer" id="searchLayer" hidden>
  <div class="search-backdrop" data-close></div>
  <div class="search-panel" role="dialog" aria-modal="true" aria-label="搜尋文件">
    <div class="search-box">
      {SEARCH_ICON}
      <input id="searchInput" type="search" placeholder="搜尋 50 篇文件…" autocomplete="off">
      <button class="search-close" type="button" data-close>Esc</button>
    </div>
    <ul class="search-results" id="searchResults"></ul>
    <div class="search-hint">↑↓ 選擇 · Enter 開啟 · Esc 關閉</div>
  </div>
</div>
<script src="{prefix}assets/app.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- build

def build():
    SITE.mkdir(exist_ok=True)
    for p in SITE.glob("**/*.html"):
        p.unlink()                      # generated only; downloaded assets stay
    ASSETS.mkdir(parents=True, exist_ok=True)
    shutil.copy(BUILDER / "styles.css", ASSETS / "styles.css")
    shutil.copy(BUILDER / "app.js", ASSETS / "app.js")
    for src, dst in [("_astro/logo.CHiZ99lN.png", "brand/logo.png"), ("banner.png", "brand/banner.png")]:
        srcp = ASSETS / src
        if srcp.exists():
            shutil.copy(srcp, ASSETS / dst)
        else:
            print(f"WARN brand asset missing: {src}")

    all_errors = []
    all_warns = []
    search_entries = []

    load_orig_slugs()

    # pass 1: convert every body; collect heading ids for anchor translation
    docs = {}
    for slug, label, section in FLAT:
        md_path = SRC_DIR / manifest.source_path(slug)
        meta, md_body = parse_front_matter(md_path.read_text(encoding="utf-8"))
        body = postprocess(pandoc(md_body), promote_bold=slug in BOLD_HEADER_PAGES)
        new_ids = re.findall(r'<h[23][^>]*id="([^"]+)"', body)
        orig = ORIG_SLUGS.get(slug, [])
        fmap, _ = align_fmap(orig, new_ids)
        docs[slug] = {"meta": meta, "label": label, "section": section, "body": body,
                      "fmap": fmap, "ids": new_ids}

    # pass 2: rewrite links, assemble shell, write
    frag_maps = {s: d["fmap"] for s, d in docs.items()}
    id_lists = {s: d["ids"] for s, d in docs.items()}
    for slug, label, section in FLAT:
        d = docs[slug]
        meta = d["meta"]
        title = meta["title"] or label
        description = meta.get("description", "")

        rw = LinkRewriter(slug, frag_maps, id_lists)
        body = rw.rewrite(d["body"])
        all_errors += [f"[{slug}] {e}" for e in rw.errors]
        all_warns += [f"[{slug}] {e}" for e in rw.warns]

        toc = build_toc(body)
        prefix = rw.prefix
        home_banner = ""
        if slug == "index":
            home_banner = (f'<a class="home-banner" href="https://deeptutor.info" target="_blank" rel="noopener">'
                           f'<img src="{prefix}assets/brand/banner.png" alt="DeepTutor banner"></a>')

        flat = [p[0] for p in FLAT]
        i = flat.index(slug)
        pager = ""
        if i > 0 or i < len(flat) - 1:
            pager = pager_html(slug, prefix)

        page = page_shell(
            slug=slug, section=section, title=title, description=description,
            toc=toc, body=body, pager=pager, prefix=prefix,
            search_index_href=prefix + "assets/search-index.json",
            home_banner=home_banner,
        )

        out_path = SITE / (slug + ".html")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")

        text = strip_tags(re.sub(r"<pre.*?</pre>", " ", body, flags=re.S))[:4000]
        headings = [strip_tags(m.group(2)) for m in re.finditer(r'<h([23])[^>]*>(.*?)</h\1>', body, re.S)]
        search_entries.append({
            "u": slug + ".html", "t": title, "s": section, "h": headings, "x": text,
        })

    (ASSETS / "search-index.json").write_text(
        json.dumps({"pages": search_entries}, ensure_ascii=False), encoding="utf-8")

    print(f"built {len(FLAT)} pages -> {SITE}")
    if all_warns:
        print("WARNINGS:")
        for w in all_warns:
            print("  " + w)
    if all_errors:
        print("LINK ERRORS:")
        for e in all_errors:
            print("  " + e)
        return 1
    return 0


# ---------------------------------------------------------------- check

def check():
    errs = []
    html_files = sorted(SITE.glob("**/*.html"))
    if len(html_files) != len(FLAT):
        errs.append(f"page count {len(html_files)} != {len(FLAT)}")
    FORBIDDEN = ['href="/zh-cn', 'src="/screenshots', 'src="/channel-icons',
                 'src="/_astro', 'src="/banner', "{{", "&nbsp;"]
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(SITE)
        for pat in FORBIDDEN:
            if pat in text:
                errs.append(f"{rel}: forbidden pattern {pat!r}")
        ids_by_file = {}
        for attr in ("href", "src"):
            for m in re.finditer(rf'{attr}="([^"]+)"', text):
                url = m.group(1)
                if url.startswith(("http://", "https://", "#", "mailto:", "ws:", "wss:")):
                    continue
                path, _, frag = url.partition("#")
                target = (f.parent / path).resolve()
                if not target.exists():
                    errs.append(f"{rel}: {attr}={url} -> missing {target.name}")
                elif attr == "href" and frag:
                    if target.suffix == ".html":
                        ids = ids_by_file.setdefault(target, set(re.findall(r'id="([^"]+)"', target.read_text(encoding="utf-8"))))
                        if frag not in ids:
                            errs.append(f"{rel}: {url} -> fragment #{frag} not found in {target.name}")
    idx = json.loads((ASSETS / "search-index.json").read_text(encoding="utf-8"))
    if len(idx["pages"]) != len(FLAT):
        errs.append(f"search index pages {len(idx['pages'])} != {len(FLAT)}")
    covered = {p["u"] for p in idx["pages"]}
    for slug, _, _ in FLAT:
        if slug + ".html" not in covered:
            errs.append(f"search index missing {slug}.html")
    if errs:
        print("CHECK FAILED:")
        for e in errs:
            print("  " + e)
        return 1
    print(f"check OK: {len(html_files)} pages, links + assets + search index all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(check() if "--check" in sys.argv else build())

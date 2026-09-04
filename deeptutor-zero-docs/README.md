# DeepTutor 零度版 · 排版網站

依官方文件站（docs.deeptutor.info/zh-cn/）架構重排的**繁體中文靜態 HTML 文件站**，
內文為「DeepTutor 零度版」改寫（繁體中文・台灣用語），kami 設計語言
（暖羊皮紙底、墨藍強調色、襯線字階層；中文字體首選 Iansui／芫荽）。

## 看站

需透過 HTTP 伺服器開啟（側欄搜尋用 fetch 載入索引，`file://` 下會停用）：

```bash
cd site
python3 -m http.server 8000
# 開啟 http://localhost:8000/
```

## 結構

```
site/                  直接可佈署的靜態站（50 頁 + 全量配圖）
  index.html           文件主頁
  get-started/         快速上手（8 頁）
  explore/             探索 DeepTutor（11 頁）
  ecosystem/           DeepTutor 生態（6 頁）
  partners/            夥伴與管道（17 頁）
  cli/                 DeepTutor CLI（6 頁）
  assets/
    screenshots/       自 docs.deeptutor.info 下載的原文截圖（全量收錄）
    channel-icons/     15 個管道圖示（SVG）
    brand/             logo 與 banner
    styles.css         kami docs shell 樣式
    app.js             搜尋（Ctrl+K）與側欄行為
    search-index.json  全站搜尋索引
builder/               產生器（重建用）
  manifest.py          50 頁清單＝原站側欄架構
  build_site.py        md→HTML 產生器＋--check 模式
  styles.css / app.js  樣式與腳本源檔
  image-list.txt       原站圖片清單（90 個路徑）
```

## 內容來源

- 內文：`../DeepTutor 零度版 繁體中文/`（零度版改寫・繁體中文）
- 對照稿：`../DeepTutor 原始文檔/`（官方 zh-cn 原文，供錨點 slug 對位）
- 配圖：從 `https://docs.deeptutor.info` 對應文章下載

## 重建

```bash
python3 builder/build_site.py          # 重建 50 頁 + 搜尋索引
python3 builder/build_site.py --check  # 內鏈/圖片/錨點/殘留路徑檢查
```

`--check` 會驗證：50 頁齊、所有本地 href/src 可解析、跨頁錨點 id 存在於目標頁、
無殘留 `/zh-cn` 連結或 `{{PLACEHOLDER}}`。

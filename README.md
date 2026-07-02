# 一頁式網頁指南合集

本倉庫收錄各種主題的「一頁式」互動教學網頁。每份指南都是獨立、可直接在瀏覽器開啟的 HTML 檔案，無需後端伺服器或建置流程。

全站採用統一的 **Mission Manual** 黑白展演式設計系統：固定 overlay 導覽、全屏 cinematic hero、長篇指南章節 rail，以及 GSAP + ScrollTrigger 的捲動動效。後續任何版面、動畫或視覺改版，請先讀：

1. `PRODUCT.md`：產品定位、讀者、品牌語氣、設計原則。
2. `DESIGN.md`：黑白 mission manual 視覺規則、元件、動效規範。

## 指南列表

| # | 指南 | 一句話介紹 | 線上閱讀 |
|---|------|-----------|---------|
| 1 | **從零開始前進美股** | 台灣投資人用複委託買美股的入門手冊 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/us-stocks-guide.html) |
| 2 | **Codex 輔助審圖工作流** | 消防製圖人員用 Codex Windows App 建立案件管理、日誌、版本與 AI 輔助初審流程 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/guide.html) |
| 3 | **製作幕後：用 AI 打造一頁式指南** | 從建倉、發想計畫、調用技能外掛、來回修正到推上 GitHub 的完整流程 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/making-of.html) |
| 4 | **PCShop 專案製作流程** | 電腦組裝估價系統的製作筆記：從痛點、規格、過濾、版面到上線 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/pcshop-ai-build-guide.html) |
| 5 | **美容儀器說明書 AI 協作工作流** | 簡體說明書 PDF 的三段 AI 接力：翻譯、複驗校稿、排版輸出 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/beauty-manual-ai-guide.html) |
| 6 | **USJ 10/6 票券安心選購工具** | 6 位成人從一日通、團體 VIP、Express、私人 VIP 中選出最穩組合，附購票與入園檢查清單 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/usj-vip-guide.html) |
| 7 | **2026 大阪五天自由行指南** | 6 位成人以心齋橋為基地，分成總覽、Day 1/3/4/5 深度頁與既有 Day 2 USJ 指南，整理神社、市場、道頓堀、勝尾寺、箕面瀑布、臨空城 Outlet、分團與餐廳候選 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/osaka-2026-trip-guide.html) |

## 設計與動畫規則

- `assets/tokens.css`：黑白色階、字體、radius、列印與 reduced-motion 基礎規則。
- `assets/style.css`：Mission hero、overlay nav、章節 rail、長文排版、表格、code block、callout、FAQ。
- `assets/deck.js`：GSAP 動效引擎，包含 hero timeline、ScrollTrigger reveal、進度條、章節 rail、copy button 與列印 finalize。
- `assets/media/mission-control-hero.png`：本地生成式 cinematic hero 背景，避免外部圖片依賴與品牌資產風險。

目前使用固定版本 CDN：

```html
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
```

`prefers-reduced-motion: reduce` 時會停用大位移、scrub 與 parallax，內容仍會立即可見。

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `PRODUCT.md` | 本站產品定位與後續改版必讀規則 |
| `DESIGN.md` | 本站 Mission Manual 視覺與動效規格 |
| `us-stocks-guide.html` | 美股複委託入門互動式教學頁面 |
| `guide.html` | 消防審圖 Codex GUI 工作流教學頁面：案件資料夾、AGENTS.md、工作日誌、本機 Git 與人工複核 |
| `making-of.html` | 製作幕後：用 AI 打造一頁式指南並推上 GitHub 的流程教學 |
| `pcshop-ai-build-guide.html` | PCShop 專案製作筆記 |
| `beauty-manual-ai-guide.html` | 美容儀器說明書 AI 協作工作流筆記 |
| `usj-vip-guide.html` | USJ 10/6 票券安心選購工具，整理 6 位成人最該先看的組合、活動查核與購票入園流程；同時作為大阪五天自由行的 Day 2 頁 |
| `osaka-2026-trip-guide.html` | 2026/10/05-10/09 大阪五天自由行總覽入口，連到 Day 1/3/4/5 深度頁與既有 Day 2 USJ 指南 |
| `osaka-2026-day1.html`, `osaka-2026-day3.html`, `osaka-2026-day4.html`, `osaka-2026-day5.html` | 大阪五天自由行每日深度頁，分別整理當天景點介紹、交通、餐廳、分團、注意事項與備案 |
| `osaka-2026-chat-supplement.md` | 大阪五天自由行的聊天補充素材整理，僅作編輯輸入 |
| `assets/` | 共用設計系統、GSAP 動效與本地媒體資產 |

## 部署

本專案維持靜態 GitHub Pages 部署。修改 HTML/CSS/JS 後推送到 `main`，GitHub Pages 會使用同一批靜態檔案更新線上頁面。

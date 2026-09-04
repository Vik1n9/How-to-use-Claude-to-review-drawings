# 一頁式網頁指南合集

本倉庫收錄各種主題的「一頁式」互動教學網頁。每份指南都是獨立、可直接在瀏覽器開啟的 HTML 檔案，無需後端伺服器或建置流程。

全站指南（大阪旅遊系列除外）採用 **Kami** 文件設計系統：暖色 parchment 紙底、單一墨藍強調色、serif 主導的層級，封面 → 目錄 → 章節的長文結構，每頁自包含樣式、可直接列印或存 PDF。後續任何版面或視覺改版，請先讀：

1. `PRODUCT.md`：產品定位、讀者、品牌語氣、設計原則。
2. `DESIGN.md`：Kami 視覺規則、元件與例外頁面說明。

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
| 8 | **AI 家教為何教不會？港大 DeepTutor** | 論文科普改寫：給 AI 一本會長大的病歷本，270 場模擬家教課的實驗結果 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/deeptutor-guide.html) |
| 9 | **蒼天堀夜行（大阪隱藏版私人行程）** | 獨立於主行程之外，以《人中之龍》大阪篇氛圍填補 10/5・10/7・10/8 晚餐後到午夜的空檔，逐站附真實店家、地址與營業時間查核 | [開啟](https://vik1n9.github.io/One-Page-Beginners-Guide/osaka-2026-yakuza-nights.html) |

## 設計系統

Kami 設計系統的規格與模板內建在本倉庫：

- `.claude/skills/kami/references/design.md`：色票、字級、元件與減法視覺規則。
- `.claude/skills/kami/assets/templates/long-doc.html`：長文模板（封面／目錄／章節／callout／表格／圖表）。

採用 Kami 的六份指南（樣式內嵌於各自檔案，不依賴外部 CSS，可單獨分享與列印）：`us-stocks-guide.html`、`guide.html`、`making-of.html`、`pcshop-ai-build-guide.html`、`beauty-manual-ai-guide.html`、`deeptutor-guide.html`。

美股頁的五個互動元件（複利試算、漲跌色對照、交割時間軸、碎股試算、停損模擬）與製作幕後／PCShop 的前後對照切換都保留，改用 Kami 的色票與版面重新設計。

**例外**：大阪旅遊系列（`osaka-2026-*.html` 與 `usj-vip-guide.html`）是自成一格的暖紙質旅遊手冊設計，維持原樣、不套用 Kami 規格。

舊的黑白 Mission Manual 共用檔（`assets/tokens.css`、`assets/style.css`、`assets/deck.js` 與 hero 背景圖）已隨轉換刪除。

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `PRODUCT.md` | 本站產品定位與後續改版必讀規則 |
| `DESIGN.md` | 本站 Mission Manual 視覺與動效規格 |
| `us-stocks-guide.html` | 美股複委託入門互動式教學頁面（Kami 版面，含五個互動試算元件） |
| `guide.html` | 消防審圖 Codex GUI 工作流教學頁面：案件資料夾、AGENTS.md、工作日誌、本機 Git 與人工複核（Kami 版面） |
| `making-of.html` | 製作幕後：用 AI 打造一頁式指南並推上 GitHub 的流程教學（Kami 版面） |
| `pcshop-ai-build-guide.html` | PCShop 專案製作筆記（Kami 版面） |
| `beauty-manual-ai-guide.html` | 美容儀器說明書 AI 協作工作流筆記（Kami 版面） |
| `deeptutor-guide.html` | 港大 DeepTutor 論文科普改寫：AI 家教的個人化記憶架構（Kami 版面） |
| `usj-vip-guide.html` | USJ 10/6 票券安心選購工具，整理 6 位成人最該先看的組合、活動查核與購票入園流程；同時作為大阪五天自由行的 Day 2 頁 |
| `osaka-2026-trip-guide.html` | 2026/10/05-10/09 大阪五天自由行總覽入口，連到 Day 1/3/4/5 深度頁與既有 Day 2 USJ 指南 |
| `osaka-2026-day1.html`, `osaka-2026-day3.html`, `osaka-2026-day4.html`, `osaka-2026-day5.html` | 大阪五天自由行每日深度頁，分別整理當天景點介紹、交通、餐廳、分團、注意事項與備案 |
| `osaka-2026-chat-supplement.md` | 大阪五天自由行的聊天補充素材整理，僅作編輯輸入 |
| `osaka-2026-yakuza-nights.html` | 獨立於主行程之外的夜間私人行程：以《人中之龍》大阪篇氛圍填補三個晚上的空檔，不含任何指向主行程的連結 |
| `assets/` | 共用設計系統、GSAP 動效與本地媒體資產 |

## 部署

本專案維持靜態 GitHub Pages 部署。修改 HTML/CSS/JS 後推送到 `main`，GitHub Pages 會使用同一批靜態檔案更新線上頁面。

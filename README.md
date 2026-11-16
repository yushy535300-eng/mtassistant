# 御策百家輔助｜上一版細節精修・LINE・進站彈窗

以使用者認可的已發布 `4aa7735` 為基底；保留玫紅、炭黑、牌桌背景、側欄、分類列與卡片。不是 `1fa7561` 那個換主視覺/撤側欄的方案。最新交接為 `PRESERVED_HANDOFF.md`、`docs/PRESERVED_TEST_REPORT.md`，原正式GitHub、Render與兩產品均未修改。

## 建置

Python標準庫生成器＋原Rust靜態伺服器，無資料庫、會員、金流或外部API。素材與字體自包含，不需建置時重新生成。

```sh
SITE_ORIGIN=https://your-test-domain.example ALLOW_INDEXING=false python3 build_site.py
cargo build --release --locked
PORT=3000 ALLOW_INDEXING=false ./target/release/mtassistant-official
```

開發 `DEV_FILES=true` 讀public白名單檔案；新增資產需重新生成與編譯。Release嵌入所有資產，不依賴工作目錄有public。預設noindex，正式部署仍需另行明確批准。

## 來源

`sitegen/portal/portal.css` 與 `4aa7735` 完全相同，唯一增量層為 `detail-polish.css`；不載入舊V3、sky、cohesion或1fa的新主視覺。頁面保留原布局，只局部改首頁LINE與手機直達、guide進度/下一步/手機目錄、contact手機QR、shell LINE與welcome。

`public/site.js`為原tabs/FAQ/選單/燈箱修正；`portal.js`為真景深/局部光線/暫停；`refine.js`為原教學進度與native進站彈窗。`build_site.py`統一LINE正確href/新分頁屬性，生成初始HTML/SEO/路由/gzip/Rust資產表。原 `data.json`、Logo、產品/客服/Threads入口不變。

六頁 `/`、`/features`、`/auto`、`/guide`（matrix/auto分開）、`/faq`、`/contact`；所有原301、`/mt`、`/index.html`、尾斜線與兩教學舊網址保留。彈窗session一次，可關閉/先逛/Escape；`?welcome=1`只為重現彈窗，`?capture=1`或`?welcome=0`為不彈窗驗收。無JS不開彈窗，正文仍可用。

## 驗收

```sh
python3 tests/preserve_audit.py
python3 tests/http_audit.py
python3 tests/aria_reference_audit.py
python3 tests/release_smoke.py
```

最新證據為 `docs/preserve-*`，200項目前全部通過，含手機/桌機/橫向彈窗、主按鈕觸控與LINE；104內部網址、ARIA與Release通過。工程結果不是美術100分，原人物商業/肖像授權、實體手機/LINE App、field CWV與效能最佳化仍未完全確認。外部產品登入/下注/結算未操作。

當前精修版只在Preview、未發布，分享URL仍是已發布且使用者認可的原版。發布需新的明確指示；不要把此前發布批准視為本次批准。

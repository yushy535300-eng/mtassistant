# 目前素材來源與權利狀態

本輪以使用者認可的炭黑／玫紅／牌桌版為基底，人物改為原主視覺的裝飾前景；沒有荷官名單、姓名介紹卡、輪播或假直播。原照片不改寫、不覆蓋，透明版本為背景編修衍生檔。

| 目前素材 | 可核對來源 | 實際用途 | 限制與處理 |
|---|---|---|---|
| baccarat-logo.png、auto-logo.png | 使用者指定公開Repository/public/assets | 原品牌、兩產品、導航／迎賓 | 原圖保留，不另換Logo或以文字替代 |
| interfaces/*.png 與響應式WebP | 原Repository的產品截圖 | 首頁、MATRIX/AUTO、分離5/6步教學與FAQ | 真實歷史截圖，原PNG/原生上限保留，不生成假UI或假即時數據 |
| async-images/5IpvgHPwOi5uABZyAx9lXZ/image-1.webp及image-2.webp | 本次原創非人物牌桌藝術 | 已認可桌機／手機首頁、精品迎賓 | 非現場實拍、不冒充真人或產品畫面；兩者獨立構圖 |
| live6.webp → live6-cutout.webp/mobile | https://gameplus3.icu/assets/live6.webp | 首頁牌桌前景 | 第三方來源標註JOJO；先前背景-only編修，不是新人物 |
| live3.webp → live3-cutout.webp/mobile | https://gameplus3.icu/assets/live3.webp | MATRIX主視覺 | 第三方來源標註海苔；23:13只去背景的透明PNG與原照保留 |
| live4.webp → live4-cutout.webp/mobile | https://gameplus3.icu/assets/live4.webp | AUTO主視覺 | 第三方來源標註小泡芙；同上 |
| live5.webp → live5-cutout.webp/mobile | https://gameplus3.icu/assets/live5.webp | 教學主視覺（兩系統狀態） | 第三方來源標註小葵；同上 |
| live1.webp → live1-cutout.webp/mobile | https://gameplus3.icu/assets/live1.webp | FAQ主視覺 | 第三方來源標註米果；先前背景-only編修 |
| live2.webp → live2-cutout.webp/mobile | https://gameplus3.icu/assets/live2.webp | 客服主視覺、原首頁品牌情境段 | 第三方來源標註毛毛；人物不是客服本人或御策代言 |
| LINE QR | 使用者指定LINE原入口 | 客服頁 | 可重製、來源就是相同客服網址，非虛構帳號 |
| 本地繁中字體子集 | Noto CJK TC，開發工具產生子集 | HTML文字 | 字體非點陣文字照片，快取依內容雜湊；可選工具不增加網站執行依賴 |

`design/cutouts/live3/4/5.png`的1920輸出不代表取得更高畫質原照片。`scripts/prepare_scene_people.py`只驗透明、整圖縮小與WebP重編碼；網站上限仍626×626、手機520×520，不程式去背景、不裁臉、不延展新身體，不把AI生成替代人冒充MT。六頁輸出姓名為空，aria-hidden裝飾層不扮演客服、直播或可操作角色。各照片original SHA與目前頁面map見`docs/cutout-assets.json`。

來源HTML的圖片alt、MT介紹標題已實際讀取對照，證據在`docs/MT_NEW_ASSET_CANDIDATES.md`、`docs/MT_SOURCE_OBSERVATION.md`。第三方Game+的MT標示不等於獨立官方身份驗證、御策代言、商用或肖像授權；這些仍未確認，正式商用前需取得許可或替換成使用者已授權素材。不導入其他代理、優惠、登入或遊戲入口。`mt-feature.webp`未使用，因無法確認其真人現場身份或排除合成。

之前QIFZssPyOpL8IvxDiTwerQ的非人物牌桌／策略圖、極光和JZABzlVPZyUJo85Q8Hz3Lx的另套美術，以及旧的六人原圖輪播，均為歷史設計資料，不是本輪正在呈現的主視覺；不能拿舊資產說明或舊截圖當最新。所有用到的圖片都包含在自包含public資產中，正常建置不需要金鑰、下載外網或額外付費服務。


## MT original dealer foregrounds — 2026-11-16

The two user-supplied MT game screenshots were cropped and alpha-matted to retain only the original dealer subjects. Face, pose and clothing pixels are retained from the source; no synthetic replacement was used. The four desktop/mobile WebP files under `public/assets/dealers/mt-real-0*-cutout*.webp` have transparent backgrounds. The full-table screenshot and recording exhibition has been removed from the visible website; the original source media remain archived in `public/assets/mt-real/`.

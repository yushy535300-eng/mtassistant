"""Render a factual handoff report from completed QA artifacts, not invented scores."""
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
http = json.loads((ROOT / 'docs/http-audit.json').read_text())
browser = json.loads((ROOT / 'docs/browser-audit.json').read_text())
webkit = json.loads((ROOT / 'docs/webkit-audit.json').read_text())
release = json.loads((ROOT / 'docs/release-smoke.json').read_text())
manifest = json.loads((ROOT / 'docs/screenshots/manifest.json').read_text())
lines = ['# TEST_REPORT｜御策百家輔助 V2', '', '更新：'+datetime.now(ZoneInfo('Asia/Taipei')).isoformat(timespec='seconds'), '', '本報告是已執行的技術驗收，不代表使用者最終視覺驗收、國際獎項認證、實機測試或正式部署。設計評分另見DESIGN_QUALITY.md。', '', '## 原架構與功能', '', f'- HTTP：passed={http["passed"]}，檢查{http["internal_urls_checked"]}個內部URL，errors={len(http["errors"])}。', f'- Chromium：passed={browser["passed"]}，{len(browser["layouts"])}個真實版位，errors={len(browser["errors"])}。', f'- Headless WebKit：passed={webkit["passed"]}，physical_device={webkit["physical_device"]}。', f'- Embedded Release：passed={release["passed"]}；沒有public目錄的臨時工作目錄，{len(release["checks"])}個頁/核心資產200。純healthz不當作可索引HTML頁。', '- Cargo debug/release build/check、Python py_compile、Node --check、Bash syntax均已執行。主生成與Rust runtime使用標準庫，无DB、會員、管理後台或新業務API。', '', '路由：/、/features、/auto、/guide?system=matrix、/guide?system=auto、/faq、/contact。原/mt、/index.html、尾斜線、guide/matrix/auto 301、healthz與原assets保留；品牌404維持404、未允許method維持405。詳FUNCTION_PRESERVATION.md與tests/http_audit.py。', '', '## 10種尺寸與真實互動', '', '360、390、393、430、440、768、1280、1440、1920、2560px，7種頁面狀態共70版位。包含原1920×1080與1440×900。檢查document overflow、圖片比例、控制可操作性；雷達元件內橫捲是設計功能，不是整頁溢出。', '']
for row in browser['interactions']:
    lines.append(f'- {row["name"]}：{row["passed"]}。'+(row.get('detail') or ''))
lines += ['', 'WebKit另檢查兩種橫直向/觸控、選單/Escape與FAQ空結果；這是引擎模擬，不是iPhone Safari或Android Chrome實機。dynamic URL bar/真實電源限制與跨系統字型仍需實機驗收。', '', '## Lighthouse 12.8.2真實參考結果', '', 'Lighthouse使用本機HTTP3000與真實Chromium，手機模式與首頁桌機；不是正式Render、不是field Core Web Vitals。保留HTML/JSON與fetchTime，改善前另存lighthouse-round1/，沒有改寫舊分數。', '', '| 測試 | Performance | Accessibility | Best practices | SEO | LCP 秒 | TBT ms | CLS |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for path in sorted((ROOT / 'docs/lighthouse').glob('*.report.json')):
    report = json.loads(path.read_text())
    categories = {k:round(v['score']*100) for k,v in report['categories'].items()}
    audits = report['audits']
    name = path.name.replace('.report.json','')
    lines.append('| '+name+' | '+str(categories['performance'])+' | '+str(categories['accessibility'])+' | '+str(categories['best-practices'])+' | '+str(categories['seo'])+' | '+f'{audits["largest-contentful-paint"]["numericValue"]/1000:.2f}'+' | '+str(round(audits['total-blocking-time']['numericValue']))+' | '+str(audits['cumulative-layout-shift']['numericValue'])+' |')
lines += ['', 'SEO69是**刻意禁止索引**导致is-crawlable不通过，不為升分而開放測試索引。每頁title/description/H1/OG/canonical/JSON-LD/ALT/內鏈已在初始HTML检查；分享圖1200×630各頁獨立。測試robots禁止、空sitemap與HTTP/meta noindex。正式模式會生成正式sitemap與index metadata，但尚未在正式服務部署或Search Console驗證；不保證排名或rich results。', '', 'LCP是實驗室值，TBT不是INP；沒有28日真實用戶、CrUX或正式網域field資料，不能聲稱field CWV通過。環境效能有變動，實際正式部署仍需複測。已做gzip、WebP、原生解析度上限、lazy/preload、資產hash/immutable與固定URL no-cache；unused CSS、正式網路延遲與高密度新UI圖仍有改善空間。', '', '## 截圖與實際發現的修正', '', f'{len(manifest)}張全頁長圖（桌機7/手機7）位於docs/screenshots/。manifest保存request viewport、實際PNG像素與來源；長圖7500px上限會等比縮小，不是手機viewport錯誤。', '', '- 修正Hero遮臉、手機章節導航裁切、未載入原圖、教學/產品主標孤字、深淺背景拼接、兩段重複CTA、來源/原Logo可存取名稱與AUTO表格ARIA。', '- WCAG按真實背景亮度與4.5:1計算修正；未為高分移除必要風險文字。', '- 原生寬上限後發現lazy双图Grid可縮到2px；補width100%，不把小圖拉超原生尺寸。', '- capture-only eager/sync修正工具長圖假空白；正常Browser同時有原始首屏交叉證據，不依工具透明度正規化盲改網站。詳docs/CAPTURE_NOTES.md。', '', '## 安全界線與尚未驗證', '', '- 沒有寫入正式GitHub main、Render或兩產品；未使用正式DB、未登入產品、未操作下注、未執行正式部署。原Repo僅讀取，保存是獨立Manus測試main。', '- Game+三張真人的商用/肖像權與MT官方來源證明待確認；不能以網路公開當授權。正式發布前需合法素材或替換。', '- 原UI圖與教學依原網站來源；不是即時或未來結果，不可保證策略收益。需要最新高密度真實UI與登入後行為核對。', '- 沒有iOS/Android實機、正式Lighthouse/field CWV、Docker daemon實建、正式可索引環境驗證；Dockerfile與回復方案已準備。', '- 尚未建立独立GitHub Repository（沒有本次寫入授權）；完整原始碼與Git bundle另交付，不杜撰GitHub網址。', '- 設計90分目標以獨立DESIGN_QUALITY.md為準，不能把功能測試通過等同全站國際級美術完成。', '', '## 證據索引', '', 'docs/http-audit.json、browser-audit.json、webkit-audit.json、release-smoke.json、lighthouse/*.report.{html,json}、lighthouse-round1/、screenshots/manifest.json、REVIEW.md、design-quality.json。測試腳本可重跑，README有可選工具安裝方式。', '']
(ROOT / 'TEST_REPORT.md').write_text('\n'.join(lines))
print('Wrote factual TEST_REPORT from completed artifacts.')

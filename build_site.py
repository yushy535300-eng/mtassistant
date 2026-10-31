from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).parent
PUBLIC=ROOT/'public'
ORIGIN='https://mtassistant-oozm.onrender.com'
VERSION='20261101-guides'
LINE='https://line.me/R/ti/p/%40116cfqfk'
MATRIX='https://scarabheart.onrender.com/'
AUTO='https://scarabheart.onrender.com/mt-auto'

def icon(name):
 paths={'arrow':'M7 17 17 7M7 7h10v10','chevron':'m9 5 7 7-7 7','layers':'m12 3 10 5-10 5L2 8l10-5Zm-10 9 10 5 10-5M2 16l10 5 10-5','grid':'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z','signal':'M3 17v4M9 12v9M15 7v14M21 2v19','shield':'m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Zm-4 9 3 3 5-6','monitor':'M3 3h18v14H3zM8 21h8M12 17v4','play':'m8 5 11 7-11 7V5Z','plus':'M12 5v14M5 12h14','chat':'M21 11.5a8.5 8.5 0 0 1-8.5 8.5H3l2-5a8.5 8.5 0 1 1 16-3.5Z','check':'m5 12 4 4L19 6','close':'m6 6 12 12M6 18 18 6','search':'m21 21-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z'}
 return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{paths[name]}"/></svg>'

def img(name,label,cls='',eager=False):
 w,h=Image.open(PUBLIC/'assets/interfaces'/f'{name}.png').size
 return f'<button class="screen {cls}" type="button" data-image="/assets/interfaces/{name}.png?v={VERSION}" data-title="{label}" aria-label="放大檢視{label}"><img src="/assets/interfaces/{name}.png?v={VERSION}" alt="{label}" width="{w}" height="{h}" loading="{"eager" if eager else "lazy"}" decoding="async"/><span class="zoom">{icon("plus")} 查看完整介面</span></button>'

def logo(auto=False,cls=''):
 return f'<img class="product-logo {cls}" src="/assets/{"auto-logo" if auto else "baccarat-logo"}.png?v={VERSION}" alt="{"MT AUTO 自動下注" if auto else "MT MATRIX 多桌百家"}原版 Logo" width="180" height="180"/>'

def button(text,url,style='gold'):
 return f'<a class="button {style}" href="{url}">{text}{icon("arrow")}</a>'

def tag(text):return f'<span class="eyebrow"><i></i>{text}</span>'

def heading(kicker,title,desc='',cls=''):
 return f'<div class="section-heading {cls}"><div>{tag(kicker)}<h2>{title}</h2></div><p>{desc}</p></div>'

NAV=[('/','首頁'),('/features','百家輔助'),('/auto','自動下注'),('/guide','操作教學'),('/faq','常見問題')]

def header(route):
 links=''.join(f'<a href="{p}" {"aria-current=page" if route==p or (p=="/guide" and route.startswith("/guide/")) else ""}>{t}</a>' for p,t in NAV)
 return f'''<a class="skip" href="#main">跳至主要內容</a><header class="site-header" id="header"><div class="nav-wrap"><a class="brand" href="/" aria-label="御策百家輔助首頁">{logo()}<span><b>御策百家輔助</b><small>YUCE · BACCARAT ASSIST</small></span></a><nav class="desktop-nav" aria-label="主要導覽">{links}</nav><div class="header-actions"><a class="service-link" href="/contact">聯繫客服</a><a class="header-launch" href="{MATRIX}">立即使用{icon('arrow')}</a><button type="button" class="menu-toggle" id="menuToggle" aria-label="開啟選單" aria-expanded="false" aria-controls="mobileNav"><span></span><span></span></button></div></div><nav id="mobileNav" class="mobile-nav" aria-label="手機導覽" hidden>{links}<a href="/contact">聯繫客服</a><div>{button('進入百家輔助',MATRIX)}{button('進入自動下注',AUTO,'outline')}</div></nav></header>'''

def footer():
 return f'''<section class="final-cta"><div class="wrap final-inner"><div>{tag('YOUR NEXT MOVE')}<h2>選擇適合你的<br/><em>百家操作方式。</em></h2></div><div class="final-actions">{button('進入多桌百家輔助',MATRIX)}{button('進入百家自動下注',AUTO,'outline')}<a class="text-link" href="/contact">需要協助？聯繫官方客服 {icon('arrow')}</a></div></div></section><footer><div class="wrap footer-top"><a class="brand" href="/">{logo()}<span><b>御策百家輔助</b><small>YUCE · BACCARAT ASSIST</small></span></a><p>專注百家輔助與策略操作，<br/>讓資訊、設定與紀錄各就其位。</p><div class="footer-links"><div><span>探索產品</span><a href="/features">MT MATRIX 多桌百家</a><a href="/auto">MT AUTO 自動下注</a></div><div><span>支援服務</span><a href="/guide/matrix">百家輔助教學</a><a href="/guide/auto">自動下注教學</a><a href="/faq">常見問題</a><a href="/contact">客服中心</a></div></div></div><div class="wrap footer-bottom"><span>© 2026 御策百家輔助</span><p>分析與策略僅供資訊輔助，不保證預測準確或獲利。請理性評估操作風險。</p><a href="#main">返回頁首 ↑</a></div></footer><a class="floating-service" href="{LINE}" aria-label="LINE 官方客服">{icon('chat')}<span>LINE 客服</span></a>'''

def viewer():
 return f'''<dialog id="imageViewer" class="image-viewer" aria-labelledby="viewerTitle"><div class="viewer-bar"><div><strong id="viewerTitle">功能介面</strong><span>原尺寸顯示，可上下／左右滑動查看</span></div><button type="button" id="viewerClose" aria-label="關閉放大介面">{icon('close')}</button></div><div class="viewer-scroll"><img id="viewerImage" alt=""/></div></dialog>'''

def page(route,title,desc,content,theme=''):
 canonical=ORIGIN+route
 schema={'@context':'https://schema.org','@type':'WebSite','name':'御策百家輔助','url':ORIGIN+'/'}
 return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/><meta name="theme-color" content="#09111d"/><title>{title}</title><meta name="description" content="{desc}"/><meta property="og:site_name" content="御策百家輔助"/><meta property="og:title" content="{title}"/><meta property="og:description" content="{desc}"/><meta property="og:type" content="website"/><meta property="og:url" content="{canonical}"/><link rel="canonical" href="{canonical}"/><link rel="icon" href="/favicon.png?v={VERSION}"/><link rel="apple-touch-icon" href="/assets/baccarat-logo.png?v={VERSION}"/><link rel="stylesheet" href="/site.css?v={VERSION}"/><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="/site.js?v={VERSION}" defer></script></head><body class="{theme}">{header(route)}<main id="main">{content}</main>{footer()}{viewer()}</body></html>'''

home=f'''
<section class="home-hero"><div class="hero-grid-lines" aria-hidden="true"></div><div class="wrap hero-layout"><div class="hero-copy">{tag('MT MATRIX × MT AUTO')}<h1>多桌洞察。<br/><em>策略有序。</em></h1><p>從牌路觀察到策略執行。<br/>你的百家操作，值得一套完整工具。</p><div class="hero-actions">{button('探索百家輔助','/features')}{button('了解自動下注','/auto','outline')}</div><div class="compat">{icon('monitor')} 電腦・手機・平板 <i></i> 瀏覽器直接使用</div><div class="hero-index"><a href="/features"><span>01</span>多桌雷達與分析{icon('arrow')}</a><a href="/auto"><span>02</span>策略與自動下注{icon('arrow')}</a></div></div><div class="hero-visual"><div class="visual-label"><span class="live-dot"></span> MATRIX ASSIST <span>PRODUCT INTERFACE / 01</span></div><div class="hero-screen">{img('matrix-assist','MATRIX ASSIST 主介面',eager=True)}</div><div class="visual-bottom"><span>多桌雷達 · AI 綜合 · 四式算牌</span><a href="/features">探索完整功能 {icon('arrow')}</a></div><span class="visual-coordinate" aria-hidden="true">YUCE / MATRIX</span></div></div><div class="wrap hero-baseline"><span>為專注操作而設計</span><div><b>OBSERVE</b><i></i><b>PLAN</b><i></i><b>EXECUTE</b></div><a href="#products">向下探索 ↓</a></div></section>
<section class="product-section product-entry-section paper" id="products"><div class="wrap">{heading('CHOOSE YOUR SYSTEM','你的百家工具，<br class="mobile-break"/>從這裡開始。','觀察牌路，或管理策略執行。<br/>依照你的操作需求，選擇對應系統。')}<div class="product-choice-grid"><article class="product-choice choice-matrix"><div class="choice-identity">{logo()}<div><span>MT MATRIX</span><h3>多桌百家輔助</h3></div><a class="choice-more" href="/features" aria-label="了解多桌百家輔助">{icon('arrow')}</a></div><p class="choice-description">整合桌台、牌路與分析資訊，<br/>讓多桌觀察保持清楚。</p><ul class="choice-features"><li>{icon('grid')}多桌雷達</li><li>{icon('signal')}AI 綜合</li><li>{icon('layers')}算牌模型</li></ul><div class="choice-actions">{button('進入百家輔助',MATRIX,'dark')}<a class="choice-detail" href="/features">了解完整功能 {icon('arrow')}</a></div></article><article class="product-choice choice-auto"><div class="choice-identity">{logo(True)}<div><span>MT AUTO</span><h3>百家自動下注</h3></div><a class="choice-more" href="/auto" aria-label="了解百家自動下注">{icon('arrow')}</a></div><p class="choice-description">先確認配注與停止條件，<br/>再掌握每次執行與紀錄。</p><ul class="choice-features"><li>{icon('layers')}配注策略</li><li>{icon('shield')}停止條件</li><li>{icon('signal')}執行紀錄</li></ul><div class="choice-actions">{button('進入自動下注',AUTO,'dark')}<a class="choice-detail" href="/auto">了解完整功能 {icon('arrow')}</a></div></article></div></div></section>
<section class="focus-section"><div class="wrap focus-layout"><div class="focus-copy">{tag('A CLOSER LOOK')}<h2>資訊集中，<br/><em>思路更清楚。</em></h2><p>主面板、四式算牌與奇偶模型，<br/>用熟悉的介面查看不同觀察角度。</p><div class="focus-tabs" role="tablist" aria-label="功能介面預覽"><button role="tab" aria-selected="true" aria-controls="focus-assist" id="focus-tab-assist" data-tab="assist"><span>01</span> AI 綜合分析 {icon('arrow')}</button><button role="tab" aria-selected="false" aria-controls="focus-cards" id="focus-tab-cards" data-tab="cards"><span>02</span> V38 四式算牌 {icon('arrow')}</button><button role="tab" aria-selected="false" aria-controls="focus-parity" id="focus-tab-parity" data-tab="parity"><span>03</span> 終值奇偶模型 {icon('arrow')}</button></div></div><div class="focus-stage"><div class="stage-heading"><span>MT MATRIX / INTERFACE</span><span>點圖查看完整介面 {icon('plus')}</span></div><div role="tabpanel" id="focus-assist" aria-labelledby="focus-tab-assist">{img('matrix-assist','AI 綜合分析主面板')}</div><div role="tabpanel" id="focus-cards" aria-labelledby="focus-tab-cards" hidden>{img('four-formulas','V38 四式算牌')}</div><div role="tabpanel" id="focus-parity" aria-labelledby="focus-tab-parity" hidden>{img('parity-model','終值奇偶模型')}</div><p class="image-note">介面截圖，非即時資料。</p></div></div></section>
<section class="start-section paper"><div class="wrap"><div class="start-heading">{tag('GET STARTED')}<h2>開始使用，<br/>不必複雜。</h2><div class="start-guide-links"><a class="text-link" href="/guide/matrix">百家輔助教學 {icon('arrow')}</a><a class="text-link" href="/guide/auto">自動下注教學 {icon('arrow')}</a></div></div><ol class="start-steps"><li><span>01</span><h3>選擇系統</h3><p>依需求進入多桌輔助或自動下注。</p></li><li><span>02</span><h3>登入與連線</h3><p>確認帳號授權及平台連線狀態。</p></li><li><span>03</span><h3>設定與操作</h3><p>觀察牌路，或設定策略與停止條件。</p></li></ol></div></section>'''

def producthero(auto,kicker,title,desc,asset,label):
 return f'<section class="product-hero {"auto-hero" if auto else "matrix-hero"}"><div class="wrap product-hero-layout"><div><div class="product-identity">{logo(auto)}<span>{"MT AUTO" if auto else "MT MATRIX"}<small>{"AUTOMATED BACCARAT" if auto else "MULTI-TABLE ASSISTANT"}</small></span></div>{tag(kicker)}<h1>{title}</h1><p>{desc}</p><div class="hero-actions">{button("進入自動下注" if auto else "進入百家輔助",AUTO if auto else MATRIX)}{button("自動下注教學" if auto else "百家輔助教學","/guide/auto" if auto else "/guide/matrix","outline")}</div></div><div class="product-hero-image">{img(asset,label,eager=True)}<span class="product-image-note">PRODUCT INTERFACE · 點圖放大</span></div></div></section>'

features=producthero(False,'桌台・牌路・多角度分析','掌握多桌。<br/><em>看清每一個細節。</em>','多桌雷達、AI 綜合、四式算牌與終值奇偶，<br/>把不同觀察角度帶回同一套介面。','matrix-assist','MATRIX ASSIST 百家輔助主面板')+f'''
<nav class="section-nav" aria-label="百家功能導覽"><div class="wrap"><a href="#radar">多桌雷達</a><a href="#analysis">AI 綜合</a><a href="#formulas">四式算牌</a><a href="#parity">終值奇偶</a></div></nav>
<section class="radar-section paper" id="radar"><div class="wrap">{heading('01 / MULTI-TABLE RADAR','多桌節奏，<br/>同時掌握。','桌台、方向與可信度並列呈現。<br/>左右滑動查看雷達，再選擇需要觀察的桌台。')}<div class="wide-screen"><div class="stage-heading"><span>MULTI-TABLE RADAR</span><span>左右滑動查看完整桌台 →</span></div><div class="radar-panorama" tabindex="0" role="region" aria-label="左右捲動查看完整多桌雷達">{img('multitable-radar','多桌雷達')}</div></div><div class="connection-row"><div>{tag('PLATFORM CONNECTION')}<h3>平台切換與連線狀態。</h3><p>在平台區確認目前選擇與連線狀態，<br/>再進入對應平台操作。</p></div>{img('platform-connection','平台切換與連線狀態')}</div></div></section>
<section class="story-section" id="analysis"><div class="wrap story-layout"><div class="story-copy">{tag('02 / AI ANALYSIS')}<h2>不同角度，<br/><em>同頁檢視。</em></h2><p>切換模型選單，查看 AI 綜合與牌路策略。主面板同步整理當局牌型、推薦資訊及分析內容。</p><div class="line-features"><div>{icon('layers')}<span>模型來源與綜合觀察</span></div><div>{icon('signal')}<span>大路及下三路分析資訊</span></div></div></div><div class="analysis-composition"><div class="analysis-main">{img('matrix-assist','MATRIX ASSIST AI 綜合分析')}</div><div class="analysis-menu">{img('analysis-models','AI 綜合模型選單')}</div></div></div></section>
<section class="story-section paper" id="formulas"><div class="wrap story-layout reverse"><div class="story-copy">{tag('03 / FOUR FORMULAS')}<h2>牌值與公式，<br/>清楚並列。</h2><p>V38 四式算牌面板顯示 Shoe、Round、當局牌面，以及 A 公式、B 公式、MUL 與 ADD 的觀察結果。</p><ul class="plain-list"><li>查看當局閒、莊牌面與點數</li><li>檢視四式結果及下一局投票</li></ul></div><div class="story-image">{img('four-formulas','V38 四式算牌完整面板')}</div></div></section>
<section class="story-section parity-section" id="parity"><div class="wrap story-layout"><div class="story-copy">{tag('04 / TERMINAL PARITY')}<h2>計算過程，<br/><em>完整呈現。</em></h2><p>終值奇偶模型將牌面、牌值、計算過程與終值集中呈現，提供另一個可供檢視的觀察角度。</p><p class="subtle-note">分析方向不代表下一局必然結果。</p></div><div class="story-image">{img('parity-model','終值奇偶模型完整面板')}</div></div></section>'''

auto=producthero(True,'配注・條件・執行紀錄','設定你的節奏。<br/><em>掌握每次執行。</em>','從策略選擇到下注金額，<br/>把執行條件與紀錄清楚留在眼前。','auto-running','百家自動下注執行面板')+f'''
<div class="auto-traits"><div class="wrap"><span>{icon('layers')}策略與配注</span><span>{icon('shield')}止損與止盈</span><span>{icon('signal')}執行狀態</span><span>{icon('grid')}事件紀錄</span></div></div>
<section class="story-section paper"><div class="wrap story-layout"><div class="story-copy">{tag('01 / STRATEGY')}<h2>先選策略，<br/>再開始執行。</h2><p>從推薦與配注設定出發，確認配注方式、開始方式與推薦來源。</p><div class="numbered-notes"><div><b>01</b><span>選擇配注方式</span></div><div><b>02</b><span>確認開始方式與基本額</span></div><div><b>03</b><span>選擇推薦來源</span></div></div></div><div class="story-image portrait-setting">{img('auto-strategy','推薦與配注設定')}</div></div></section>
<section class="story-section amount-section"><div class="wrap story-layout reverse"><div class="story-copy">{tag('02 / AMOUNT & TIME')}<h2>注額與時間，<br/><em>先設清楚。</em></h2><p>設定基本單注與單筆上限，並確認自動停止時間。開始前檢查每一項條件，操作中查看執行狀態。</p></div><div class="setting-stack">{img('auto-amount','投注金額設定')}{img('auto-timer','自動停止時間設定')}</div></div></section>
<section class="story-section paper"><div class="wrap story-layout"><div class="story-copy">{tag('03 / STOP CONDITIONS')}<h2>停止條件，<br/>也是策略的一部分。</h2><p>查看止損與止盈設定、核對說明，確認停止條件後再執行。各項限制與結算方式以程式內顯示為準。</p><a class="text-link" href="/faq">查看自動下注常見問題 {icon('arrow')}</a></div><div class="story-image portrait-setting">{img('auto-limits','止損與止盈設定')}</div></div></section>
<section class="story-section history-section"><div class="wrap story-layout reverse"><div class="story-copy">{tag('04 / EXECUTION HISTORY')}<h2>當前狀態，<br/><em>每次回來都看得到。</em></h2><p>依序查看送出、接受與結算事件。遇到停止狀態時，先閱讀面板原因，再確認後續操作。</p><p class="subtle-note">本頁介面截圖中的金額與紀錄僅為畫面內容，不代表即時或未來結果。</p></div><div class="story-image">{img('auto-history','執行紀錄與目前狀態')}</div></div></section>'''

def simplehero(kicker,title,desc):return f'<section class="simple-hero"><div class="wrap">{tag(kicker)}<h1>{title}</h1><p>{desc}</p></div></section>'

guide=simplehero('TUTORIALS / 操作教學','選擇你的系統，<br/><em>查看對應教學。</em>','百家輔助與自動下注各有獨立的操作流程。<br/>請依正在使用的系統，進入對應教學。')+f'''<section class="guide-selection paper"><div class="wrap"><div class="product-choice-grid"><article class="product-choice choice-matrix"><div class="choice-identity">{logo()}<div><span>MT MATRIX / GUIDE</span><h3>百家輔助教學</h3></div></div><p class="choice-description">平台連線、多桌雷達、AI 分析，<br/>以及四式算牌與奇偶模型。</p><div class="choice-actions">{button('查看百家輔助教學','/guide/matrix','dark')}</div></article><article class="product-choice choice-auto"><div class="choice-identity">{logo(True)}<div><span>MT AUTO / GUIDE</span><h3>自動下注教學</h3></div></div><p class="choice-description">配注策略、注額、停止條件，<br/>以及執行狀態與事件紀錄。</p><div class="choice-actions">{button('查看自動下注教學','/guide/auto','dark')}</div></article></div></div></section>'''

def tutorial(auto,steps):
 route='/guide/auto' if auto else '/guide/matrix'
 title='自動下注教學' if auto else '百家輔助教學'
 desc='從配注策略、注額到停止條件，逐項確認後再執行。' if auto else '從連線狀態到多桌觀察，逐步認識百家輔助介面。'
 intro=simplehero(('MT AUTO' if auto else 'MT MATRIX')+' / 操作教學',title+'。<br/><em>一步一步，清楚操作。</em>',desc)
 switch=f'<nav class="tutorial-switch" aria-label="切換操作教學"><div class="wrap"><a href="/guide/matrix" {"aria-current=page" if not auto else ""}>{logo()}百家輔助教學</a><a href="/guide/auto" {"aria-current=page" if auto else ""}>{logo(True)}自動下注教學</a></div></nav>'
 nav=''.join(f'<a href="#step{i}">{i:02d} {short}</a>' for i,(short,heading_,description,shots) in enumerate(steps,1))
 articles=''
 for i,(short,heading_,description,shots) in enumerate(steps,1):
  pictures=''.join(img(name,label) for name,label in shots)
  articles+=f'<article id="step{i}"><span class="step-num">{i:02d}</span><h2>{heading_}</h2><p>{description}</p><div class="tutorial-screens">{pictures}</div></article>'
 end=f'<div class="tutorial-finish"><h3>準備好開始了？</h3><p>確認帳號授權與設定後，再進入對應系統。</p>{button("進入自動下注" if auto else "進入百家輔助",AUTO if auto else MATRIX,"dark")}</div>'
 return intro+switch+f'<section class="guide-content paper"><div class="wrap guide-layout"><aside><span>{title} / 使用流程</span>{nav}<a class="text-link" href="/contact">需要操作協助 {icon("arrow")}</a></aside><div class="guide-steps">{articles}{end}</div></div></section>'

matrix_guide=tutorial(False,[
 ('登入與連線','登入帳號，確認平台連線。','進入百家輔助，完成帳號登入及授權確認。查看連線狀態，選擇正在使用的平台，再由對應入口進入。',[('platform-connection','百家輔助平台連線與切換')]),
 ('多桌雷達','從雷達查看桌台資訊。','多桌雷達並列各桌台、方向與可信度。左右滑動查看其他桌台，再選擇需要觀察的桌台；連線與資料狀態以程式內顯示為準。',[('multitable-radar','多桌雷達完整介面')]),
 ('AI 綜合分析','切換分析來源，檢視主面板。','開啟模型選單，依需要選擇分析來源或牌路策略。主面板可查看當局牌型、推薦資訊與 AI 分析內容。',[('analysis-models','AI 模型選單'),('matrix-assist','百家輔助主面板與 AI 分析')]),
 ('四式算牌','檢視當局牌值與公式結果。','由主面板的「算牌」開啟 V38 四式算牌，核對 Shoe、Round、閒莊牌面與點數，再查看四式結果及下一局投票。',[('four-formulas','V38 四式算牌完整面板')]),
 ('終值奇偶','查看計算過程與終值。','由主面板的「奇偶」開啟終值奇偶模型。依序查看牌面、牌值、計算過程、終值與顯示方向；這些資訊不保證下一局結果。',[('parity-model','終值奇偶模型完整面板')]),
])
auto_guide=tutorial(True,[
 ('登入與準備','登入自動下注，確認操作桌台。','由自動下注入口登入並確認帳號授權。開始前先確認使用的平台、桌台，以及面板顯示的連線與目前狀態。',[]),
 ('推薦與配注','設定配注方式與推薦來源。','在「推薦與配注」確認配注方式、開始方式及推薦來源。若選擇馬丁，請閱讀程式內的跨局階梯與多桌限制說明。',[('auto-strategy','自動下注推薦與配注設定')]),
 ('投注金額','確認基本單注與單筆上限。','在「投注金額」設定基本單注與單筆上限。開始前再次核對金額，避免沿用不符合本次操作需求的設定。',[('auto-amount','自動下注投注金額設定')]),
 ('停止時間','設定自動停止時間。','確認「自動停止時間（分鐘）」欄位及下方說明。時間到後停止新增下注，已接受注單的後續結算方式，以程式內顯示為準。',[('auto-timer','自動停止時間設定')]),
 ('止損與止盈','確認止損、止盈與核對說明。','在「止損與止盈」設定停止條件，閱讀送單前核對、結算及配注限制說明。各項限制以程式內提示為準。',[('auto-limits','止損與止盈設定')]),
 ('執行與紀錄','開始後，持續查看狀態與紀錄。','核對設定後依程式操作開始。查看執行桌台、接受金額與目前狀態；需要停止時使用程式的停止按鈕。若顯示已停止，先閱讀原因，再依提示確認是否需要手動重新開始。',[('auto-running','自動下注執行面板'),('auto-history','執行紀錄與目前狀態')]),
])

questions=[('兩套系統','多桌百家輔助與自動下注有什麼不同？','MT MATRIX 主要整理桌台、牌路、AI 分析與算牌資訊；MT AUTO 著重配注策略、下注金額、停止條件及執行紀錄。可依需求從對應入口進入。'),('使用方式','電腦和手機都能使用嗎？','以瀏覽器開啟系統，可使用電腦、Android 手機與 iPhone。實際平台及遊戲操作方式以登入後的程式介面為準。'),('使用方式','需要下載安裝檔案嗎？','不需要另行下載安裝檔，直接由瀏覽器進入系統即可。'),('帳號授權','登入或授權有問題，要找誰協助？','請聯繫官方 LINE 客服 @116cfqfk，提供會員帳號、問題描述與錯誤畫面，方便確認。不要提供密碼。'),('自動下注','開始前要確認哪些設定？','請確認配注方式、推薦來源、基本單注、單筆上限、止損、止盈及停止時間，再查看執行狀態。各項限制與核對方式以程式內說明為準。'),('自動下注','畫面顯示停止時該怎麼處理？','先查看目前狀態與停止原因。若顯示頁面進入背景而停止新增操作，返回後依面板提示確認是否需要手動重新開始。'),('分析與結果','AI 分析或配注策略可以保證獲利嗎？','不可以。百家樂結果具有不確定性；分析方向、公式及配注策略都不保證可以預測下一局或獲利。'),('介面展示','官網展示的是即時資料嗎？','功能頁展示的是介面截圖，不是即時桌台或實際送單畫面。請進入正式系統查看當前狀態。')]
faq=simplehero('HELP CENTER / 常見問題','你想了解的，<br/><em>這裡先說清楚。</em>','從使用方式到自動下注設定，<br/>找到開始之前需要知道的資訊。')+f'<section class="faq-content paper"><div class="wrap faq-layout"><aside><h2>還需要協助？</h2><p>把遇到的問題與畫面<br/>提供給官方客服。</p>{button("聯繫 LINE 客服",LINE,"dark")}</aside><div class="faq-main"><label class="faq-search">{icon("search")}<input id="faqSearch" type="search" placeholder="搜尋問題，例如：登入、停止、手機" aria-label="搜尋常見問題"/></label><p id="faqEmpty" hidden>沒有符合的問題，請嘗試其他關鍵字或聯繫客服。</p>'+''.join(f'<details class="faq-item"><summary><span><small>{category}</small>{q}</span>{icon("plus")}</summary><p>{a}</p></details>' for category,q,a in questions)+'</div></div></section>'

contact=simplehero('OFFICIAL SUPPORT / 客服中心','問題有人協助，<br/><em>操作更有方向。</em>','帳號授權、功能使用或連線問題，<br/>請透過官方客服管道聯繫。')+f'''<section class="contact-section paper"><div class="wrap"><div class="contact-card"><div class="contact-symbol">{icon('chat')}</div><div><span>LINE 官方客服</span><h2>@116cfqfk</h2><p>請留下會員帳號、問題描述與錯誤截圖，<br/>方便客服協助確認。</p></div>{button('開啟 LINE 客服',LINE,'dark')}</div><div class="support-notes"><div>{tag('BEFORE YOU CONTACT')}<h3>提供這些資訊，<br/>方便確認問題。</h3></div><ol><li><b>01</b><span>正在使用的系統：多桌百家或自動下注</span></li><li><b>02</b><span>使用裝置、瀏覽器與發生時間</span></li><li><b>03</b><span>錯誤畫面與操作步驟，請勿提供密碼</span></li></ol></div><a class="social-row" href="https://www.threads.net/@uss0857"><span>THREADS / @uss0857</span><b>查看公開動態</b>{icon('arrow')}</a></div></section>'''

pages={
 '/':('御策百家輔助｜多桌百家分析・百家自動下注','御策百家輔助官方網站，探索 MT MATRIX 多桌百家、牌路分析、AI 輔助與 MT AUTO 自動下注。',home,''),
 '/features':('多桌百家輔助・牌路分析｜御策百家輔助','了解 MT MATRIX 多桌雷達、AI 綜合、V38 四式算牌與終值奇偶，查看完整功能介面。',features,''),
 '/auto':('百家自動下注・策略設定｜御策百家輔助','了解 MT AUTO 配注策略、注額、停止時間、止損止盈與執行紀錄，查看百家自動下注介面。',auto,'theme-auto'),
 '/guide':('操作教學｜御策百家輔助','從選擇系統、登入授權、平台連線到策略設定，了解御策百家輔助使用流程。',guide,''),
 '/guide/matrix':('百家輔助操作教學｜御策百家輔助','MT MATRIX 百家輔助專屬教學：平台連線、多桌雷達、AI 分析、四式算牌與終值奇偶。',matrix_guide,''),
 '/guide/auto':('自動下注操作教學｜御策百家輔助','MT AUTO 自動下注專屬教學：配注策略、投注金額、停止時間、止損止盈與執行紀錄。',auto_guide,'theme-auto'),
 '/faq':('常見問題｜御策百家輔助','查詢多桌百家、自動下注、手機使用、登入授權及停止條件的常見問題。',faq,''),
 '/contact':('客服中心・LINE 官方客服｜御策百家輔助','透過官方 LINE @116cfqfk 聯繫御策百家輔助客服，取得帳號授權與操作協助。',contact,''),
}
(PUBLIC/'pages').mkdir(exist_ok=True)
for route,(title,desc,content,theme) in pages.items():
 p=PUBLIC/'index.html' if route=='/' else PUBLIC/'pages'/(route[1:].replace('/','-')+'.html')
 p.write_text(page(route,title,desc,content,theme))
sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{r}</loc></url>' for r in pages)+'</urlset>'
(PUBLIC/'sitemap.xml').write_text(sitemap)
print('Built 8 complete pages with original product assets.')

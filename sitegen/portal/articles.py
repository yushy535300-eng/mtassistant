"""First-party product guides grounded in the existing UI and verified workflows."""
from html import escape
from ..common import screen, arrow, button, asset_url, DATA

ARTICLES = [
 {'slug':'matrix-workflow','title':'多桌百家輔助怎麼用？先連線，再看雷達與分析','category':'多桌輔助','summary':'從平台連線、桌台選擇到模型核對，建立不跳步的 MT MATRIX 使用流程。','image':'matrix-assist','read':'4 分鐘','sections':[
 ('開始前，先分清楚兩套工具','MT MATRIX 用來整理多桌雷達、牌路與模型資訊；MT AUTO 則處理配注、停止條件與執行紀錄。兩套工具有各自的入口，閱讀教學時也要選擇對應系統。進入 MATRIX 前，先確認帳號已完成授權，並準備好要使用的平台。'),
 ('第一步：確認平台與連線','登入後先看平台連線區，不要只看得到主面板就認為資料已更新。核對目前選擇的平台、連線狀態，以及對應的進入按鈕。如果切換過平台，重新確認一次目前位置，再查看其他資料。','platform-connection'),
 ('第二步：先選桌，再讀面板','多桌雷達把多個桌台放在同一個觀察區，原圖比較寬，手機需要左右滑動。先找到桌台名稱，再核對桌台資訊與目前資料狀態。不同桌台或不同局次的數值不要放在一起解讀。'),
 ('第三步：核對模型與局次','切換 AI 綜合、四式算牌或終值奇偶時，先確認目前的模型與畫面上的桌台。四式面板可以核對 Shoe、Round、牌面及點數；奇偶面板則提供牌值、計算過程與終值。資訊顯示方向不是下一局的結果保證。'),
 ('看到異常時，先記錄再處理','如果桌台、局次或連線看起來不一致，先保留錯誤畫面，記下裝置、瀏覽器及發生時間。需要客服協助時提供系統名稱與操作步驟，不要把密碼或驗證碼傳出去。')], 'related':'model-panels','cta':('/guide?system=matrix','閱讀多桌五步教學')},
 {'slug':'auto-checklist','title':'自動下注開始前：配注、金額與停止條件怎麼核對','category':'自動下注','summary':'把啟動前的設定拆成五項，確認每一個條件，再檢查實際執行狀態。','image':'auto-strategy','read':'4 分鐘','sections':[
 ('先確認你要執行的設定','自動下注不是只按一下開始。MT AUTO 會依目前設定處理操作，因此啟動前要重新核對平台、桌台、推薦來源、配注方式與金額。不要把上一次的設定或畫面的預設值，直接當成本次已確認的條件。'),
 ('推薦與配注分開看','在「推薦與配注」區核對開始方式及推薦來源，再看選擇的配注方法。若使用跨局階梯類型，先閱讀程式內對多桌與階梯的說明。任何配注方式都不能消除遊戲結果的不確定性。','auto-strategy'),
 ('基本單注不等於全部風險','基本單注與單筆上限是不同欄位。檢查時兩者都要看，並確認畫面顯示的數字與本次需求相符。不要只看基本金額，忽略其他會影響後續執行的設定。','auto-amount'),
 ('時間、止損與止盈逐項確認','自動停止時間、止損及止盈要分別核對。填寫設定後，重新確認單位、數值與目前狀態。觸發停止條件或顯示已停止時，要讀取停止原因與紀錄；已被接受的操作及後續結算，以實際系統顯示為準。','auto-limits'),
 ('開始後仍要查看執行紀錄','啟動後核對狀態、目前配注與執行紀錄。遇到不明狀態時，先在原程式內確認停止操作，不要反覆點擊開始。若仍有疑問，記下停止原因、時間及畫面，帶著資訊聯繫客服。')], 'related':'execution-status','cta':('/guide?system=auto','閱讀自動下注六步教學')},
 {'slug':'model-panels','title':'AI 綜合、四式算牌與終值奇偶：三種面板怎麼看','category':'介面解析','summary':'辨識各模型顯示的欄位，先核對牌面與局次，再閱讀分析資訊。','image':'four-formulas','read':'3 分鐘','sections':[
 ('先看資料是哪一桌、哪一局','模型畫面再多，第一步仍是確認資料所屬的桌台與局次。切換桌台或模型後，重新核對目前標示，避免把上一個畫面當成本局資訊。畫面中的數值是當時的介面紀錄，不能拿展示截圖判斷目前桌台。'),
 ('AI 綜合：核對來源與主面板','模型選單是切換分析來源的位置，主面板則集中顯示當局牌型與分析內容。切換後確認目前模型名稱，閱讀畫面說明，而不是只取一個方向欄位就跳過其他資訊。','analysis-models'),
 ('四式算牌：從牌面與點數開始','V38 四式面板包含 Shoe、Round、閒莊牌面、點數及公式顯示。建議由上往下核對，先確認牌面及局次，再閱讀 A、B、MUL、ADD 與投票欄位。若基礎資料不一致，先處理連線或資料問題。','four-formulas'),
 ('終值奇偶：閱讀計算過程','終值奇偶面板把牌面、牌值、計算與終值放在一起。先核對輸入牌面，再讀中間過程與結果。這能幫助辨識面板在顯示什麼，並不代表可以保證下一局。','parity-model'),
 ('模型的共同使用邊界','不同模型是不同的資訊整理方式，不應把名稱、圖示或顯示方向當作獲利承諾。遇到欄位改版時，以登入後的實際程式及最新教學為準；有疑問可提供畫面請客服協助辨識。')], 'related':'matrix-workflow','cta':('/features#matrix-formulas','查看模型功能與原圖')},
 {'slug':'mobile-home-screen','title':'iPhone 與 Android：把程式加入主畫面的正確入口','category':'手機使用','summary':'官網與程式入口不同。選對工具、用對瀏覽器，再依裝置完成主畫面設定。','image':'platform-connection','read':'3 分鐘','sections':[
 ('先開程式，再加入主畫面','御策官網提供介紹、教學與客服資訊；多桌輔助與自動下注則有各自的程式網址。要建立程式捷徑，應先從下載安裝頁選擇對應工具，開啟程式後再操作。把官網直接加入主畫面，開啟的仍會是官網。'),
 ('iPhone：使用 Safari 操作','在 Safari 開啟選好的程式入口，再從分享選單尋找「加入主畫面」。依目前 iOS 畫面確認名稱及新增操作。瀏覽器與系統版本不同，分享按鈕的位置可能不同，可對照下載安裝頁的圖文步驟。'),
 ('Android：使用 Chrome 操作','在 Chrome 開啟程式，再從三點選單尋找新增至主畫面或安裝相關選項。選單文字會因系統、瀏覽器版本及程式支援情形而不同，依目前畫面完成確認。'),
 ('新增後，確認開啟的是哪個工具','完成後從主畫面開啟捷徑，確認畫面對應 MT MATRIX 或 MT AUTO。兩套工具用途不同，建議使用容易辨識的名稱。新增捷徑不會自動完成帳號授權或平台連線，仍要依程式內流程確認。'),
 ('找不到選項時怎麼辦','如果是在社群 App 內建瀏覽器開啟，先改用 Safari 或 Chrome 再確認。若仍找不到選項，記下手機型號、系統版本與瀏覽器名稱，對照安裝教學或聯繫客服。')], 'related':'connection-troubleshooting','cta':('/download','開啟圖文安裝教學')},
 {'slug':'execution-status','title':'自動下注顯示已停止？先看狀態，再核對執行紀錄','category':'操作支援','summary':'分清設定畫面、執行狀態與紀錄，避免在不清楚原因時反覆重新開始。','image':'auto-running','read':'3 分鐘','sections':[
 ('三種資訊不要混在一起','設定區用來確認你希望程式採用的條件；執行面板顯示目前狀態；紀錄則幫助回看已發生的流程。看到停止提示時，先閱讀完整文字，不要只憑按鈕顏色或單一數值判斷原因。'),
 ('第一步：讀取停止原因','查看畫面是否顯示時間到、條件觸發或其他提示。不同狀況需要核對不同設定，應以程式內的實際訊息為準。若不確定訊息的意思，先保留畫面。','auto-history'),
 ('第二步：回到條件設定','重新查看自動停止時間、止損止盈、金額上限，以及配注與開始方式。每次重新開始前都要再次確認，避免沿用與本次需求不相符的數值。','auto-limits'),
 ('第三步：核對已接受的操作','目前狀態與已接受注單的後續處理，不一定是同一件事。查看紀錄與實際結算顯示，不要用關閉網頁代替確認程式已停止，也不要在狀態不明時連續按開始。'),
 ('需要協助時，整理最少但完整的資訊','提供系統名稱、發生時間、裝置、操作順序、停止提示與相關截圖。客服摘要工具可以在本機整理資訊，再由你自行複製並聯繫。請勿加入密碼、驗證碼或其他私密資料。')], 'related':'auto-checklist','cta':('/contact#support-prep','整理客服問題')},
 {'slug':'connection-troubleshooting','title':'登入後沒看到資料：平台、授權與連線的檢查順序','category':'操作支援','summary':'依序確認入口、帳號授權、平台與桌台，不靠反覆刷新碰運氣。','image':'platform-connection','read':'3 分鐘','sections':[
 ('先確認不是開錯系統','從官網的工具入口選擇 MT MATRIX 或 MT AUTO。兩套工具的操作畫面不同，對照教學時也要確認目前選擇的產品。若畫面與教學完全不同，先檢查入口，不要把另一套工具的設定流程套上來。'),
 ('確認帳號授權與提示','能開啟網頁不代表已完成帳號授權。閱讀畫面上的登入、授權及連線提示，若有明確錯誤訊息，記下完整文字。授權問題請聯繫客服，不要嘗試繞過提示。'),
 ('核對平台與連線狀態','在平台連線區查看目前平台。切換後重新核對狀態，再由對應入口進入。若畫面仍沒有更新，記下操作時間和平台，避免把未完成連線的畫面當成當前資料。','platform-connection'),
 ('再看桌台、局次與資料','連線完成後才查看桌台名稱、局次及相關資訊。如果切桌前後畫面看起來不一致，先核對資料所屬位置；不要把不同桌台的截圖或不同時間的數值互相比較。'),
 ('聯繫客服時要提供什麼','提供系統名稱、帳號識別、平台、裝置、瀏覽器及錯誤畫面。描述問題前做了哪一步，以及從哪裡開始沒有資料。密碼和驗證碼不需要提供，公開分享截圖前也應遮蔽個人資料。')], 'related':'mobile-home-screen','cta':('/contact','前往客服中心')},
]
BY_SLUG = {a['slug']:a for a in ARTICLES}


# Every article uses a distinct existing product image, not generated stock art.
# Reference dimensions for screenshots are read directly from the product data contract.
COVERS = {
    'matrix-workflow': 'matrix-assist',
    'auto-checklist': 'auto-strategy',
    'model-panels': 'four-formulas',
    'mobile-home-screen': 'install-ios',
    'execution-status': 'auto-running',
    'connection-troubleshooting': 'platform-connection',
}

def cover_path(article):
    name=COVERS[article['slug']]
    return '/assets/install/yuce-matrix-ios-install.webp' if name == 'install-ios' else '/assets/interfaces/' + name + '.webp'

def cover_dimensions(article):
    name=COVERS[article['slug']]
    return DATA['sizes'].get(name)

def cover_image(article, eager=False):
    path=cover_path(article)
    dimensions=cover_dimensions(article)
    size_attrs=f' width="{dimensions[0]}" height="{dimensions[1]}"' if dimensions else ''
    return f'<img src="{asset_url(path)}" alt="{escape(article["title"],quote=True)}：原有產品或安裝教學畫面" loading="{"eager" if eager else "lazy"}" decoding="async"{size_attrs}>'

def cards(limit=None):
    items=ARTICLES[:limit] if limit else ARTICLES
    return '<div class="editorial-grid">'+''.join(f'''<a class="editorial-card" href="/articles/{a['slug']}"><div class="editorial-art editorial-photo">{cover_image(a)}</div><div class="editorial-copy"><p class="kicker">{a['category']} <span>· {a['read']}</span></p><h3>{a['title']}</h3><p>{a['summary']}</p><span class="text-link">閱讀文章 {arrow()}</span></div></a>''' for a in items)+'</div>'

def render():
    return '''<section class="portal-pagehead"><div><p class="kicker">THE YUCE JOURNAL</p><h1>使用指南與操作筆記</h1><p>從真實介面出發，把連線、模型、設定與手機操作說清楚。</p></div></section><section class="portal-section" aria-labelledby="journal-title"><div class="section-top"><div><p class="kicker">實用內容，完整閱讀</p><h2 id="journal-title">找到你現在需要的解答</h2></div></div>'''+cards()+'''</section>'''

def render_article(slug):
    a=BY_SLUG[slug]
    toc=''.join(f'<a href="#article-section-{i}"><span>{i:02d}</span>{escape(s[0])}</a>' for i,s in enumerate(a['sections'],1))
    sections=''.join(f'<section id="article-section-{i}"><h2>{escape(s[0])}</h2><p>{escape(s[1])}</p>{screen(s[2],s[0]) if len(s)>2 else ""}</section>' for i,s in enumerate(a['sections'],1))
    related=BY_SLUG[a['related']]
    return f'''<article class="journal-article"><header class="journal-header"><p class="kicker">{a['category']} ／ 御策使用指南</p><h1>{a['title']}</h1><p class="journal-intro">{a['summary']}</p><div class="journal-meta"><span>御策編輯團隊</span><span>更新：2026.11.17</span><span>閱讀約 {a['read']}</span></div></header><div class="journal-layout"><aside class="journal-toc"><p class="kicker">本文目錄</p><nav aria-label="文章目錄">{toc}</nav><a class="text-link" href="/articles">全部文章 {arrow()}</a></aside><div class="journal-body"><div class="journal-lead-media"><a class="journal-cover-link" href="{cover_path(a)}" data-image="{cover_path(a)}" data-title="{escape(a['title'],quote=True)}" aria-label="放大查看本文主圖">{cover_image(a,True)}<span class="screen-zoom">＋ 放大查看原圖</span></a></div>{sections}<div class="journal-note">本文依既有產品介面整理，畫面與狀態以目前程式為準。分析與配注策略僅供輔助，不能保證預測結果或獲利。</div><div class="journal-next"><p class="kicker">接著閱讀</p><a href="/articles/{related['slug']}">{related['title']} {arrow()}</a></div><div class="inline-actions">{button(a['cta'][1],a['cta'][0])}<a class="text-link" href="/articles">回到文章專區 {arrow()}</a></div></div></div></article>'''

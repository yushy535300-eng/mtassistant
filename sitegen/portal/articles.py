"""First-party product guides grounded in the existing UI and verified workflows."""
from html import escape
from ..common import screen, arrow, button

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
ARTICLES.extend([

 {'slug':"baccarat-basics",'title':"百家樂新手入門：莊、閒、和局與一局怎麼進行",'category':"百家樂入門",'summary':"介紹百家樂的基本角色、比牌流程與注意事項。",'image':"matrix-assist",'read':'4 分鐘','sections':[
 ("先理解莊、閒、和","百家樂比較的是兩手牌的最終點數，通常稱為莊與閒；也可能出現和局。這些名稱代表投注選項與比牌結果，不代表你一定要擔任發牌者。"),
 ("牌點怎麼計算","A 算 1 點、2 到 9 按牌面數字計算，10、J、Q、K 算 0 點；總點數只保留個位數。因此 7 加 8 等於 15，計為 5 點。"),
 ("補牌不能自己任意決定","一般百家樂的第三張牌依固定規則處理，並不是投注者可自由決定。不同變體可能有差異，應先閱讀平台規則。"),
 ("開始前最重要的事情","理解玩法、賠付表與限制比猜下一局更重要。每一局結果存在不確定性，請勿將任何輔助工具理解為保證結果。"),
 ],'related':'banker-player-tie','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"banker-player-tie",'title':"百家樂莊、閒、和怎麼分？賠付與抽水常見觀念",'category':"規則解析",'summary':"分辨不同投注結果與不同平台的賠付差異。",'image':"four-formulas",'read':'4 分鐘','sections':[
 ("莊與閒是比較對象","莊與閒並非兩位玩家的技術對決，而是依百家樂規則發出、補牌並比較的兩手牌。勝負由最終點數決定。"),
 ("和局不是每個投注都一樣處理","常見規則下，莊或閒投注遇到和局可能退回本金，但仍應以當局遊戲版本的實際說明為準。"),
 ("抽水與特殊賠率","部分標準百家樂會對莊贏投注收取佣金，也有免佣、特定點數特別賠付等變體。不能把其他遊戲的賠率直接套過來。"),
 ("正確比較要看規則表","查看每個投注選項的賠率、佣金、限額及特殊條件，不要單憑名稱推算實際回報。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"roadmap-explained",'title':"百家樂路單怎麼看？珠盤路、大路與衍生路入門",'category':"路單教學",'summary':"用清楚的順序理解常見路單顯示，而非迷信走勢。",'image':"multitable-radar",'read':'4 分鐘','sections':[
 ("路單記錄已發生的結果","路單是歷史局次的整理工具，能協助快速檢視莊閒分布，但不能提前決定下一局會出現什麼。"),
 ("珠盤路與大路","珠盤路通常按局次記錄莊、閒、和等結果，大路則以連續結果形成不同排列方式；各平台圖示可能略有差異。"),
 ("大眼仔、小路、曱甴路","這些衍生路使用既有大路的排列形態計算標記，不等同於預測真實牌面。看到紅藍標記也要先確認平台的定義。"),
 ("如何避免看錯","先核對目前桌台、局次與路單類型，再查看既有紀錄。不同桌台的路單不可任意拼接。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"streaks-and-misconceptions",'title':"連莊、連閒一定會反轉？百家樂常見三大誤區",'category':"觀念解析",'summary':"認識連續結果與賭徒謬誤，避免被歷史走勢誤導。",'image':"parity-model",'read':'4 分鐘','sections':[
 ("連續出現不等於下一局必定反轉","前面連續出現莊或閒，並不會因此產生下一局必須補償的機制。沒有足夠證據時，不要把短期連續結果當成確定規律。"),
 ("反過來也不是一定延續","看見連莊，不代表後續一定繼續莊。把過去結果直接延伸到下一局，同樣是缺乏依據的判斷。"),
 ("加倍投注不能消除風險","加倍策略可能快速提高單筆金額，還受到資金與平台限額限制；即使某一段期間奏效，也不能因此保證長期回報。"),
 ("較好的做法","區分歷史紀錄、程式顯示與實際結算三種資訊。將工具視為閱讀與整理資訊的輔助，不是獲利保證。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"multi-table-overview",'title':"多桌百家樂怎麼觀察？同時看多桌時的資訊整理方法",'category':"多桌觀察",'summary':"多桌畫面先辨識桌台與更新時間，避免資料混淆。",'image':"analysis-models",'read':'4 分鐘','sections':[
 ("先確認每張桌的名稱","多桌畫面能同時顯示不同桌台的資訊，但需要先分清桌台、局次、遊戲規則及資料狀態。"),
 ("確認更新狀態","若切換平台或頁面後資料尚未更新，不應把舊畫面當成即時結果。"),
 ("使用篩選與分類","將需要閱讀的資訊按平台、桌台及模型分別整理，避免在小螢幕一次塞進過多面板。"),
 ("資訊多不代表判斷更準","同時看到很多路單或指標，並不會改變遊戲本身的不確定性。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"baccarat-odds-basics",'title':"百家樂機率與期望值：為什麼不能把勝率當成獲利保證",'category':"機率知識",'summary':"理解單局機率、賠率與長期結果的不同。",'image':"auto-amount",'read':'4 分鐘','sections':[
 ("勝率與回報率不是同一回事","某個選項出現的比例與投注後實際拿到的回報並不相同，還受到賠付方式及佣金影響。"),
 ("短期結果會波動","少量局數可能偏離長期平均。短時間出現連勝或連敗，都不能直接用來證明某種系統一定有效。"),
 ("期望值是不同結果的加權平均","評估投注時，要把可能勝、負、和的情形與賠付條件放在一起考量，而不是只看單一命中率。"),
 ("理解風險比尋找必勝法重要","不存在因為某一張路單或某套配注順序，就能保證每局獲利的做法。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"responsible-limits",'title':"百家樂風險管理：事前預算、停止條件與紀錄怎麼做",'category':"風險管理",'summary':"先訂限制與中止條件，不以追損作為預設策略。",'image':"auto-limits",'read':'4 分鐘','sections':[
 ("事先設定能承受的上限","如有參與任何金錢投注，應僅使用可承受損失的預算，並遵守所在地法規及年齡限制。"),
 ("不要在情緒中追加金額","因為想要把前一局的損失追回而反覆提高金額，容易超出原本的預算。"),
 ("停止條件要可執行","若使用具備停止時間或限額設定的工具，啟用前核對數值與單位，操作中也要確認實際執行狀態。"),
 ("保留清楚紀錄","把投注設定、實際結果與中止原因分別記錄。當無法判斷執行狀態時，先核對系統，不要連續重複操作。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
 {'slug':"live-vs-online-baccarat",'title':"真人百家樂與電子桌台有什麼不同？畫面與規則閱讀指南",'category':"遊戲知識",'summary':"分清真人直播、電子桌台及資訊展示畫面的用途。",'image':"platform-connection",'read':'4 分鐘','sections':[
 ("先分辨內容類型","真人百家樂通常呈現實際發牌畫面，電子桌台則可能採用數位動畫或其他形式。畫面外觀不同，不代表規則完全相同。"),
 ("比對規則而不是只看畫面","不同桌台可能有佣金、限額、補牌、特殊投注等差異；選擇前應閱讀對應說明。"),
 ("展示截圖不等於即時桌台","官網教學圖片只協助辨識操作位置與功能，不能被當作正在進行的牌局或實際回報。"),
 ("切換桌台後重新確認","進入新桌台前，確認桌台名稱、平台及目前狀態，避免把另一張桌的資料誤認為當前畫面。"),
 ],'related':'baccarat-basics','cta':('/articles','閱讀更多百家樂文章')},
])

# Audited weekly publications, released via the scheduled publisher.
import json as _json
from pathlib import Path as _Path
_published_manifest = _Path(__file__).with_name("editorial_published.json")
if _published_manifest.exists():
    ARTICLES.extend(_json.loads(_published_manifest.read_text(encoding="utf-8")))

# External editorial photographs are sourced from specific Wikimedia Commons file pages.
# Keep their attribution visible in article pages; product manuals retain real interface shots.
PHOTO_ASSETS = {
    "baccarat-basics": ("https://commons.wikimedia.org/wiki/Special:FilePath/BaccaratTables-Casino-MarinaBaySands-Singapore-20100507.jpg?width=960", "https://commons.wikimedia.org/wiki/File:BaccaratTables-Casino-MarinaBaySands-Singapore-20100507.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "banker-player-tie": ("https://commons.wikimedia.org/wiki/Special:FilePath/King_playing_card_and_casino_tokens_01.jpg?width=960", "https://commons.wikimedia.org/wiki/File:King_playing_card_and_casino_tokens_01.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "roadmap-explained": ("https://commons.wikimedia.org/wiki/Special:FilePath/Kartenschlitten.jpg?width=960", "https://commons.wikimedia.org/wiki/File:Kartenschlitten.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "streaks-and-misconceptions": ("https://commons.wikimedia.org/wiki/Special:FilePath/Playing_Cards.JPG?width=960", "https://commons.wikimedia.org/wiki/File:Playing_Cards.JPG", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "multi-table-overview": ("https://commons.wikimedia.org/wiki/Special:FilePath/Norwegian_Dawn_casino_1.JPG?width=960", "https://commons.wikimedia.org/wiki/File:Norwegian_Dawn_casino_1.JPG", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "baccarat-odds-basics": ("https://commons.wikimedia.org/wiki/Special:FilePath/CasinoCards.jpg?width=960", "https://commons.wikimedia.org/wiki/File:CasinoCards.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "responsible-limits": ("https://commons.wikimedia.org/wiki/Special:FilePath/Trente_et_Quarante_table_(dealer's_view).jpg?width=960", "https://commons.wikimedia.org/wiki/File:Trente_et_Quarante_table_(dealer's_view).jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "live-vs-online-baccarat": ("https://commons.wikimedia.org/wiki/Special:FilePath/Casino_for_you.jpg?width=960", "https://commons.wikimedia.org/wiki/File:Casino_for_you.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "baccarat-natural-eight-nine": ("https://commons.wikimedia.org/wiki/Special:FilePath/Baccara_Palette.jpg?width=960", "https://commons.wikimedia.org/wiki/File:Baccara_Palette.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "baccarat-commission-variants": ("https://commons.wikimedia.org/wiki/Special:FilePath/King_playing_card_and_casino_tokens_02.jpg?width=960", "https://commons.wikimedia.org/wiki/File:King_playing_card_and_casino_tokens_02.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "baccarat-record-reading": ("https://commons.wikimedia.org/wiki/Special:FilePath/BaccaratTables-Casino-MarinaBaySands-Singapore-20100507.jpg?width=960", "https://commons.wikimedia.org/wiki/File:BaccaratTables-Casino-MarinaBaySands-Singapore-20100507.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
    "baccarat-mobile-checklist": ("https://commons.wikimedia.org/wiki/Special:FilePath/MC_%E6%BE%B3%E9%96%80%E9%87%91%E6%B2%99_Sands_Macao_Casino_interior_%E7%99%BE%E5%AE%B6%E6%A8%82_Baccarate_cards_gamble_machine_terminals_dispaly_system_November_2016_Lnv_01.jpg?width=960", "https://commons.wikimedia.org/wiki/File:MC_%E6%BE%B3%E9%96%80%E9%87%91%E6%B2%99_Sands_Macao_Casino_interior_%E7%99%BE%E5%AE%B6%E6%A8%82_Baccarate_cards_gamble_machine_terminals_dispaly_system_November_2016_Lnv_01.jpg", "Wikimedia Commons（請見來源頁）", "授權條款見來源頁"),
}

def editorial_image(a):
    source = PHOTO_ASSETS.get(a['slug'])
    if source:
        return (source[0], f"與百家樂文章主題相關的撲克牌、籌碼或賭場情境：{a['title']}", source)
    return (f"/assets/interfaces/{a['image']}.webp", f"御策真實程式操作畫面：{a['title']}", None)

BY_SLUG = {a['slug']:a for a in ARTICLES}

def cards(limit=None, topic=None):
    if topic == 'baccarat':
        base = {'baccarat-basics','banker-player-tie','roadmap-explained',
                'streaks-and-misconceptions','multi-table-overview','baccarat-odds-basics',
                'responsible-limits','live-vs-online-baccarat'}
        pool = [a for a in ARTICLES if a['slug'] in base or a.get('published_at')]
        items = sorted(pool, key=lambda a: (a.get('published_at','2026-11-17'), a['slug']), reverse=True)
    else:
        items = ARTICLES[:]
    if limit:
        items = items[:limit]
    result = []
    for a in items:
        src, alt, _ = editorial_image(a)
        result.append(
            f'<a class="editorial-card" href="/articles/{escape(a["slug"],quote=True)}">'
            f'<div class="editorial-art editorial-art-photo">'
            f'<img src="{escape(src,quote=True)}" alt="{escape(alt,quote=True)}" loading="lazy" decoding="async"></div>'
            f'<div class="editorial-copy"><p class="kicker">{escape(a["category"])} <span>· {escape(a["read"])}</span></p>'
            f'<h3>{escape(a["title"])}</h3><p>{escape(a["summary"])}</p>'
            f'<span class="text-link">閱讀文章 {arrow()}</span></div></a>'
        )
    return '<div class="editorial-grid">' + ''.join(result) + '</div>'


def render():
    return '''<section class="portal-pagehead"><div><p class="kicker">THE YUCE JOURNAL</p><h1>百家樂知識與操作教學</h1><p>從百家樂規則、牌路與機率觀念，到御策程式的實際操作說明。</p></div></section><section class="portal-section" aria-labelledby="journal-title"><div class="section-top"><div><p class="kicker">實用內容，完整閱讀</p><h2 id="journal-title">找到你現在需要的解答</h2></div></div>'''+cards()+'''</section>'''

def render_article(slug):
    a=BY_SLUG[slug]
    image_url, image_alt, photo = editorial_image(a)
    if photo:
        lead = (f'<figure class="journal-photo"><img src="{escape(image_url,quote=True)}" '
                f'alt="{escape(image_alt,quote=True)}" loading="eager" decoding="async">'
                f'<figcaption>攝影：{escape(photo[2])} · {escape(photo[3])} · '
                f'<a href="{escape(photo[1],quote=True)}" target="_blank" rel="noopener">圖片來源與授權</a></figcaption></figure>')
    else:
        lead = screen(a['image'], a['title'])
    toc=''.join(f'<a href="#article-section-{i}"><span>{i:02d}</span>{escape(s[0])}</a>' for i,s in enumerate(a['sections'],1))
    sections=''.join(f'<section id="article-section-{i}"><h2>{escape(s[0])}</h2><p>{escape(s[1])}</p>{screen(s[2],s[0]) if len(s)>2 else ""}</section>' for i,s in enumerate(a['sections'],1))
    related=BY_SLUG[a['related']]
    return f'''<article class="journal-article"><header class="journal-header"><p class="kicker">{a['category']} ／ 御策使用指南</p><h1>{a['title']}</h1><p class="journal-intro">{a['summary']}</p><div class="journal-meta"><span>御策編輯團隊</span><span>更新：{a.get("published_at","2026-11-17").replace("-",".")}</span><span>閱讀約 {a['read']}</span></div></header><div class="journal-layout"><aside class="journal-toc"><p class="kicker">本文目錄</p><nav aria-label="文章目錄">{toc}</nav><a class="text-link" href="/articles">全部文章 {arrow()}</a></aside><div class="journal-body"><div class="journal-lead-media">{lead}</div>{sections}<div class="journal-note">本文為百家樂知識及使用資訊整理，規則以實際桌台為準。分析工具不能保證預測結果或獲利。</div><div class="journal-next"><p class="kicker">接著閱讀</p><a href="/articles/{related['slug']}">{related['title']} {arrow()}</a></div><div class="inline-actions">{button(a['cta'][1],a['cta'][0])}<a class="text-link" href="/articles">回到文章專區 {arrow()}</a></div></div></div></article>'''

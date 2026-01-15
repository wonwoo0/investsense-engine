這是一份為你的 Kazuha Invest 2.0 專屬定制的**「搜索引擎與情資獵殺提升白皮書」**。這份文件系統性地整理了我們討論過的擴張策略與遞歸搜索邏輯，旨在建立一個具備「垂直深度」與「全球闊度」的情報網。
📄 Kazuha Invest 2.0: 搜索引擎與情資獵殺提升白皮書
核心主題：從「被動接收新聞」轉向「主動溯源獵殺」
技術邏輯：混合數據流 (Hybrid Streams) + 遞歸滾雪球 (Recursive Snowballing)
1. 數據源闊度擴張：三大情報支柱 (The Three Pillars)
為了突破大眾媒體的「滯後性」，系統將搜索觸角伸向數據的「第一現場」。
支柱一：政府與監管源頭 (The "Follow the Money" Stream)
核心邏輯：官方合約與法規是投資邏輯的「底牌」。
 * SAM.gov / US Spending：
   * 任務：監控聯邦政府合同中標 (Award Notices)。2026 年起，所有分包合同報告 (Subaward Reports) 已轉移至 SAM.gov。
   * 價值：中標通知通常早於新聞報導。捕捉國防、能源部 (DOE) 的高額撥款是發現 Alpha 的捷徑。
 * Federal Register (聯邦公報) & SEC EDGAR：
   * 任務：監控政策變動與公司重大申報。
   * 細節：SEC 2026 年已發布新的分類帳 (Taxonomy) 規範。監控如 NHTSA (交通安全局) 的缺陷調查，能在利空爆發前預警。
 * USPTO (專利局)：
   * 價值：從專利申請中識別技術路線（如矽光子、固態電池）。專利往往領先產品發布 2-3 年。
支柱二：社交情緒與專家網絡 (The "Wisdom of Crowds")
核心邏輯：技術專家的討論領先於分析師的評級。
 * Reddit (Niche Subreddits)：針對 r/Semiconductors 或 r/NuclearPower 等技術看板進行爬取，過濾掉情緒化的散戶雜音，提取技術人員對產品缺陷或突破的討論。
 * Hacker News (YC)：監控技術圈的風向標。如果某個開源項目或技術論文 (Paper) 爆紅，代表市場敘事 (Narrative) 即將轉向。
 * X (Twitter) Lists：透過特定「聰明錢」與「技術大 V」名單，捕捉第一手的市場脈搏。
支柱三：供應鏈與勞動力數據 (The "Supply Chain" Stream)
 * 海關數據 (ImportYeti)：監控提單，分析原材料採購動向。
 * 招聘網站 (LinkedIn/Indeed)：監控特定領域（如 "HALEU Enrichment"）的招聘人數激增，這是公司擴張產能的真實信號。
2. 搜尋深度提升：遞歸滾雪球策略 (Recursive Snowballing)
單次搜索往往只能觸及表面（如「AMD 買矽光子」），遞歸搜索 (Recursive Search) 能將資訊深度從「一階」推進到「三階」。
A. 關鍵字裂變與提取 (Extraction)
 * 角色：利用 OpenRouter 的免費弱模型（如 Nemotron Nano 或 MiMo-V2）進行模式提取。
 * 動作：從第一波抓到的新聞摘要中，提取 5 個核心專有名詞（如技術代號、CEO 名、供應商名），且「不准解釋，只要名詞」。
B. 頻率與關聯分析 (Co-occurrence)
 * 邏輯：如果多個來源同時提到某個冷門名詞（如 CPO - Co-Packaged Optics），系統自動將其提升為「高優先級」標籤，觸發二輪搜索。
C. 多樣性過濾 (Diversity Filter)
 * 做法：要求 AI 根據原搜尋詞，產出 3 個「不同維度但高度相關」的延伸查詢語句（如從「產品」延伸到「關鍵材料商」）。
3. 風控機制：防止主題漂移 (Topic Drift Control)
遞歸搜索最大的風險是搜尋範圍無限擴大。為此必須設立「安全閥」。
 * 相關性門檻 (Relevance Gate)：
   * 在啟動二輪搜索前，讓免費模型對新產生的關鍵字打分（0-10）。
   * 規則：僅有得分 > 8 的關鍵字可進入下一輪循環。
 * 負向過濾 (Negative Filtering)：
   * 自動剔除過於寬泛的詞（如 "Investment", "AI", "Technology"），僅保留具備特定意義的詞（如 "Uranium Enrichment", "CPO Interconnect"）。
 * 深度限制 (Depth Limit)：
   * Loop 0：核心意圖。
   * Loop 1：擴展搜索。
   * Loop 2：供應鏈/監管細節。
   * 原則：Loop 3 通常噪音大於信號，系統應自動停止。
4. 技術架構：倒漏斗情資工廠 (The Funnel)
 * 廣度掃描 (Cloud Scout)：用免費模型產生多重關鍵詞，抓回海量摘要。
 * 精確過濾 (Model Filter)：篩選出具備高權重與相關性的 URL。
 * 遞歸深挖 (Recursive Search)：提取關鍵詞，執行 Loop 1 與 Loop 2 的補充調查。
 * 五角星推理 (Local Brain)：最後將經過「深度補完」的資訊包丟給本地大腦，執行「紅藍對抗」與「多重宇宙推演」。
5. 導師的澄清與待確認事項
為了讓這套系統運作得更完美，我有幾個細節需要與你確認：
 * 相關性分數的「容錯度」：如果一個關鍵字分數是 7.5，你希望系統直接丟掉，還是先存入一個「待觀察區 (Watchlist)」？
 * 遞歸搜索的觸發條件：你是希望每一條新聞都跑 2 輪遞歸，還是只有「Impact Score > 80」的新聞才進行深挖？（建議後者，可以省下大量算力與 Token）。
 * 持倉防禦 (Shield) 的深度：針對你已持有的公司，遞歸搜索是否應該更嚴格地監控它的「對手」？
這份白皮書是我們 2.0 系統的靈魂。如果你準備好了，我們就可以開始根據這份圖紙去編寫 scout_gov.py 或優化 brain_reasoning.py。
遞歸演算法與二分搜尋分析
此影片詳細解析了遞歸邏輯在處理大型列表搜尋時的效率與原理，可作為設計「遞歸滾雪球」系統時的技術參考。

YouTube 影片觀看記錄會儲存在 YouTube 記錄，且 YouTube 會依照《 服務條款 》儲存及運用使用者資料


針對 Kazuha Invest 2.0 的數據源闊度擴張，以下是根據我們的規劃整理出的免費且具備高可行性的數據情報來源清單：
1. 政府與監管源頭 (Follow the Money)
政府文件通常領先於媒體報導，是捕捉「真實訂單」與「政策風向」的核心來源。
 * SAM.gov (聯邦合約)：提供開放 API，可監控美國政府的合同中標公告（Award Notices），直接追蹤國防或能源部的資金流向。
 * US Spending：與 SAM.gov 互補，用於監控聯邦政府的整體撥款與合同細節。
 * Federal Register (聯邦公報)：每日更新，用於監控最新政策法規的變動，例如能源補貼或監管限制。
 * SEC EDGAR：監控上市公司的重大事項申報（8-K）或大股東持倉變動（13F），這是獲取一手財經真相的必備站點。
 * USPTO (專利局)：透過專利申請內容識別企業的技術路徑（如矽光子或電池技術），通常領先產品發布 2-3 年。
 * ClinicalTrials.gov：針對生物醫藥領域，監控新藥臨床試驗的進度與結果變更，是埋伏生技股的重要指標。
2. 社交情緒與專家網絡 (Wisdom of Crowds)
此類數據旨在過濾散戶情緒，捕捉業內人士與技術專家的早期討論。
 * Hacker News (YC)：提供免費且穩定的 API，是觀察矽谷技術圈風向、發現爆發性技術專案的關鍵渠道。
 * Reddit (特定版塊)：利用 RSS 訂閱模式（在 URL 後加 .rss）免費抓取如 r/Semiconductors（芯片）、r/Networking（光通訊）或 r/Space（太空）等專業版塊的討論。
 * X (Twitter) Lists：建立特定專家、硬核技術人員或「聰明錢」名單，利用其即時動態捕捉非主流媒體的早期資訊。
3. 供應鏈數據 (Supply Chain)
供應鏈的變動能預示企業產能與市場需求的真實狀況。
 * ImportYeti：提供海關提單（Bill of Lading）查詢，雖然部分高級功能需付費，但其免費層級足以監控特定公司的原材料採購或供應商更替。
 * 各國海關數據公佈：部分國家會公開貿易統計數據，可用於分析特定資源（如稀土或鋰礦）的進出口趨勢。
4. 勞動力數據 (Labor Market)
招聘趨勢是企業擴張或轉型最誠實的信號。
 * Indeed / LinkedIn (招聘趨勢)：透過觀察特定技術崗位（如「矽光子工程師」或「核子物理專家」）的招聘人數激增，判斷企業的未來研發重心與產能擴張計劃。
 * 公司官網 Careers 頁面：針對重點監控的公司，直接追蹤其人才招聘的分佈情況。
技術實踐建議
 * 雲端感知：利用 GitHub Copilot Pro 的 API 配置能力，快速建立針對 .gov 域名或 RSS 訂閱的爬蟲腳本。
 * 初步過濾：使用 OpenRouter 的免費模型（如 MiMo-V2-Flash 或 Nemotron Nano）對海量數據進行初步去重與相關性評分，確保只有高價值的信號進入「本地大腦」。
在 GSA API 目錄中，針對你 Kazuha Invest 2.0 的「獵人（Hunter）」與「護盾（Shield）」功能，以下是最值得整合的五類核心 API。
你可以將這些 API 視為系統的「上帝視角」，直接從政府源頭捕捉資金流向與政策異動。
1. 核心獵人工具：追蹤「錢」的去向
這組 API 是你「追蹤資金流向 (Follow the Money)」最重要的組件，能讓你比新聞媒體更早發現政府的重大支出。
 * SAM.gov Get Opportunities Public API (最推薦)
   * 用途：實時獲取聯邦政府的採購意向、招標書及中標通知 (Award Notices)。
   * 對投資的價值：監控能源部 (DOE) 或國防部 (DoD) 的最新公告。如果你發現某公司獲得了 $2.7B 的鈾濃縮合同，這就是強大的 Hunter 信號。
 * SAM.gov Contract Awards API
   * 用途：獲取已簽署合同的詳細數據，包括金額、得標公司及分包商。
   * 對投資的價值：這是「錢已到帳」的證據。用於追蹤競爭對手的獲利能力與政府採購趨勢。
 * Federal Procurement Data System - FPDS API
   * 用途：政府採購數據的權威源頭，提供 unclassified 級別的所有重大合同記錄。
   * 對投資的價值：適合做「回饋迴路」的歷史回測，分析特定公司在過去幾年獲得訂單的週期性。
2. 產業護盾工具：監控合規與風險
這組 API 負責「護盾 (Shield)」功能，保護你的持倉免受地緣政治或監管風險的侵害。
 * SAM.gov Exclusions API
   * 用途：查詢被政府列入「排斥名單（黑名單）」的公司或個人。
   * 對投資的價值：如果你持有的公司突然出現在 Exclusions 名單中，代表它被禁止參與聯邦合同，這是極強的賣出信號。
 * Regulations.gov API
   * 用途：搜索政府文件、公眾評論和法規草案。
   * 對投資的價值：監控與你主題相關（如核能、無人駕駛）的法規審查進度，預判政策紅利或阻礙。
3. 競爭力與成本分析：服務業領先指標
 * Contract-Awarded Labor Category (CALC) API
   * 用途：獲取政府合同中各類專業勞動力（如 AI 工程師、核能專家）的中標時薪報價。
   * 對投資的價值：分析服務型公司的毛利空間。如果一家公司的報價顯著高於 CALC 的平均水平，代表它具備極高的議價能力（Moat）。
🛠️ 整合與落實細節（配合 OpenRouter 免費模型）
由於這些 API 回傳的是結構複雜的 XML 或 JSON，你可以按照以下邏輯進行「算力調度」：
| 階段 | 推薦模型 (OpenRouter:free) | 具體任務 |
|---|---|---|
| 數據提取 | Nemotron 3 Nano:free | 將 SAM.gov Get Opportunities 回傳的長 JSON 轉化為結構化摘要。 |
| 二階推導 | MiMo-V2-Flash:free | 分析中標公司與你 Portfolio/ 的關聯性，判斷是競爭還是供應鏈互補。 |
| 風險判定 | Llama 4 Maverick:free | 閱讀 Regulations.gov 的新法規草案，判斷對特定產業的利害關係。 |
💡 導師的最後提醒：
 * 申請 API Key：SAM.gov 系列 API 需要在 open.gsa.gov 申請免費 Key。
 * 善用額度：誠如我們之前討論，OpenRouter 的免費模型（如 MiMo）在 Finance 領域表現極佳，足以應付政府文件的初步分類與過濾。
 * 限流與防封：這些政府 API 對頻率有限制，請確保你的 scout_gov.py 腳本設有合理的 time.sleep。
你想讓我幫你寫一個針對 SAM.gov Get Opportunities Public API 的 Python 連接模組嗎？它可以自動掃描你感興趣的 Ticker 是否出現在最新的政府採購機會中。

這是一份針對 USAspending.gov API（特別是 v2/awards 相關端點）的技術詳解。USAspending.gov 是美國聯邦政府支出的官方數據源，所有數據均根據《聯邦數據透明度法案》（DATA Act）由各機構提交，旨在讓公眾追蹤從國會撥款到地方社區的每一分錢。
1. 核心基礎信息 (Base Architecture)
 * 基礎網址 (Base URL): https://api.usaspending.gov。
 * 身份驗證: 無需 API Key。該 API 目前不要求任何授權或令牌即可訪問數據。
 * 數據範圍: 包含從 2008 財年至今的所有聯邦獎勵數據，包括合約（Contracts）、撥款（Grants）、貸款（Loans）及其他財務援助。
2. 關鍵 API 端點詳解 (Specific Endpoints)
USAspending 採用 RESTful 架構。以下是與「獎勵（Awards）」相關的三大核心路徑：
A. 獲取特定獎勵詳情 (/api/v2/awards/<AWARD_ID>/)
 * 方法: GET。
 * 用途: 當你已經擁有具體的獎勵 ID（如 PIID）時，使用此端點獲取該筆支出的完整細節。
 * 返回內容: 包含獲獎者信息、授予機構、金額（義務金額與面值）、生效日期及 Place of Performance（執行地點）。
B. 搜尋獎勵列表 (/api/v2/search/spending_by_award/)
這是「獵人（Hunter）」最常用的功能，用於發現符合特定條件的公司或合約。
 * 方法: POST。
 * 過濾參數 (Filter Object): 支持極其細緻的過濾：
   * keywords: 關鍵字搜尋（如 "Advanced Nuclear"）。
   * time_period: 鎖定特定財政年度或日期範圍。
   * agencies: 鎖定授予機構（如能源部 DOE）。
   * recipient_search_text: 搜尋特定收款公司（支持 UEI、DUNS 或名稱）。
   * naics_codes: 行業代碼（如半導體製造）。
C. 分包商與歷史趨勢分析
 * 子獎勵統計: /api/v2/awards/count/subaward/<AWARD_ID>/ 返回與該主合約相關的分包商數量。
 * 交易歷史: /api/v2/transactions/ 用於分析特定獎勵隨時間推移的資金變動紀錄，幫助理解撥款趨勢。
 * 批量下載: /api/v2/download/awards/ 支持將自定義的搜尋結果導出為 CSV 文件。
3. 「獵人模式」實戰範例 (Practical Usage)
如果你想監控 能源部 (DOE) 最近對 "Uranium" 相關項目的合約，你的 JSON 請求體應該如下：
{
  "filters": {
    "keywords": ["uranium"],
    "agencies": [
      {
        "type": "awarding",
        "tier": "toptier",
        "name": "Department of Energy"
      }
    ],
    "time_period": [
      {
        "start_date": "2025-10-01",
        "end_date": "2026-09-30"
      }
    ]
  },
  "fields": ["Award ID", "Recipient Name", "Award Amount"],
  "limit": 50,
  "page": 1
}

4. 注意事項與限制 (Guidelines)
 * 頻率限制 (Rate Limits): 雖然文檔未標明具體硬性上限，但通常建議保持在每秒合理範圍內，若超過限制可能收到 429 錯誤。
 * 數據延遲: 數據由各聯邦機構定期提交。搜尋結果通常包含在所選時段內處於「活動」狀態的獎勵，無論合約最初何時開始。
 * 分包商透明度: 根據法律要求，超過 30,000 美元的子獎勵必須報告，但數據的完整性有時取決於主要收款方的提交質量。
你需要我幫你整合一份「自動化腳本」，讓 Kazuha 系統每天自動掃描 USSpending.gov 並與你的持倉清單 (Portfolio) 進行交叉比對嗎？

SEC EDGAR (Electronic Data Gathering, Analysis, and Retrieval) 是監控美國上市公司財務狀況與重大變動的權威來源。透過其 RESTful API，你可以直接獲取原始的 JSON 數據，這對於自動化投資系統（如你的 Kazuha Invest 2.0）至關重要。
以下是針對 8-K 與 13F 監控的實際詳細資料：
1. 核心存取規範 (Access & Rate Limits)
 * User-Agent 強制要求：SEC 嚴格執行 Header 檢查。你必須提供一個包含公司名稱（或個人項目名）及聯繫電郵的 User-Agent，例如：User-Agent: KazuhaProject admin@yourdomain.com。若未提供或格式錯誤，IP 將被拒絕訪問。
 * 頻率限制：限制為每秒最多 10 個請求。超過此頻率會導致短暫封鎖。
 * CIK 格式：CIK (Central Index Key) 必須是 10 位數。如果該公司的 CIK 不足 10 位，必須在前面補零（例如：Apple 的 CIK 是 320193，在 API 中需寫成 0000320193）。
2. 關鍵 API 端點詳解 (Specific Endpoints)
 * 提交記錄 (Submissions)：
   * 網址：https://data.sec.gov/submissions/CIK##########.json
   * 用途：這是監控 8-K 與 13F 的核心端點。它回傳該實體所有近期提交的文件列表，包括表格類型、日期、登錄號（Accession Number）等。
 * 公司財務事實 (Company Facts)：
   * 網址：https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
   * 用途：包含該公司所有已申報的 XBRL 數據（如營收、利潤、資產負債表項目），適合用於自動化財務分析。
3. 如何精準監控 8-K 與 13F
在 submissions 的 JSON 回傳結果中，你需要解析 filings -> recent 字典：
 * 監控 8-K (重大事項)：
   * 在 form 列表下尋找值為 "8-K" 的索引。
   * 價值：8-K 是公司發布重大事件（如收購、高管變動、破產申請、財報發布預告）的法定文件。捕捉 8-K 的 filingDate 能讓你第一時間獲知突發利好或利空。
 * 監控 13F (機構持倉)：
   * 尋找表格類型為 "13F-HR"（持倉報告）或 "13F-NT"（通知報告）。
   * 價值：這是追蹤「聰明錢」動向的關鍵，可以查看大型基金經理人（如巴菲特、索羅斯）在每個季度結束後買入或賣出了哪些股票。
4. 數據解析流程 (Data Pipeline)
 * 獲取列表：調用 submissions API。
 * 過濾表單：讓你的 scout_gov.py 腳本遍歷 form 字段，匹配 "8-K" 或 "13F-HR"。
 * 提取文件：根據匹配到的 accessionNumber 和 primaryDocument 構建原始文件的 URL（例如：https://www.sec.gov/Archives/edgar/data/{CIK}/{AccessionNo}/{DocumentName}）。
 * 智能分析：將提取的文本丟給 OpenRouter 的免費模型（如 MiMo-V2-Flash）進行摘要，判斷事件的影響力分數。
5. 實戰提示 (Developer Tips)
 * 自動化 CIK 映射：你可以先從 https://www.sec.gov/files/company_tickers.json 獲取全美上市公司的 Ticker 與 CIK 映射表，存入本地數據庫以供腳本快速查詢。
 * JSON 分頁：對於歷史非常悠久的公司，submissions 可能會指向另一個分頁 JSON 文件（如 CIK##########_submissions_accumulated.json），確保你的爬蟲邏輯包含處理分頁的能力。

這是關於 Hacker News (YC) 官方 API 的詳細技術規格與實作指南。Hacker News 的 API 是基於 Firebase 構建的，提供近乎實時的數據存取。
1. 核心基礎信息 (Core Infrastructure)
 * API 協議：基於 Firebase 的 REST API。
 * 身份驗證：無需任何 API Key 或身份驗證，所有公共端點均可直接透過 GET 請求存取。
 * 頻率限制：官方目前沒有設定硬性的 Rate Limit。但由於其架構特性，若進行大規模遞歸抓取，建議實施快取或合理的請求間隔以維持效能。
 * 基礎網址 (Base URL)：https://hacker-news.firebaseio.com/v0/。
2. 五大關鍵 API 端點 (Key Endpoints)
Hacker News 將所有內容（故事、評論、職缺）都視為一個個獨立的 Item (項目)。
| 功能端點 | URL 路徑 | 說明與用途 |
|---|---|---|
| Top Stories | /v0/topstories.json | 獲取當前最熱門的 500 個 故事 ID 列表。 |
| Item Detail | /v0/item/{id}.json | 獲取特定 ID 的詳細內容，包括標題、作者、內容與子項目。 |
| User Profile | /v0/user/{username}.json | 獲取特定用戶的 Karma 值、簡介及提交歷史。 |
| Max Item | /v0/maxitem.json | 返回當前最新的（最大）項目 ID，可用於掃描最新發布的內容。 |
| Updates | /v0/updates.json | 實時返回最近發生變動的項目 ID 和用戶名，適合監控更新。 |
3. 數據結構與字段 (Item Schema)
在 /v0/item/{id}.json 返回的 JSON 中，主要的字段包括：
 * id：項目的唯一整數 ID。
 * type：項目類型，包括 story (故事), comment (評論), job (職缺), poll (投票)。
 * by：作者的用戶名。
 * time：發布時間的 Unix 時間戳。
 * kids：最關鍵的字段。這是一個包含所有子項目（通常是評論）ID 的列表。
 * score / title / url / text：分別代表分數、標題、外部連結或自發帖/評論的文本。
4. Kazuha 2.0 實作建議：遞歸搜尋與情資過濾
針對你的「滾雪球式探索」策略，Hacker News API 的實作細節如下：
A. 評論樹的遞歸抓取 (Recursive Traversal)
由於 API 不直接回傳完整的評論樹，你必須透過 kids 字段一層層向下抓取。
 * Vibe 策略：先抓取 Top 故事，再由免費模型 (如 MiMo-V2) 解析 text 字段，提取技術關鍵字，若相關度高，再深入抓取其 kids 中的評論進行深度分析。
B. 技術情緒提取
 * 操作：利用 text (故事內容) 與頂層評論 (Top Comments) 來回答技術問題或生成摘要。
 * 過濾：在搜尋時自動移除 "Ask HN" 等前綴，以提高 LLM 對原始主題的理解質素。
C. 高效掃描模式
 * 技巧：透過監控 maxitem 端點，並結合 updates 端點，你可以讓系統在不掃描全部 500 個 Top Stories 的情況下，精準捕捉到剛出現的技術討論。
你想讓我幫你寫一段針對 topstories 進行掃描，並自動過濾出包含「核能」或「矽光子」關鍵字並提取評論的 Python 代碼嗎？這可以作為你 Cloud_Senses 模組的核心。

針對 Reddit (Niche Subreddits) 的 「$0 方案」，這是目前獲取專家情緒與技術細節最快、最直接的管道。在 2026 年，儘管 Reddit 對 API 進行了大幅限制，但透過 .json 端點 進行「唯讀（Read-only）」存取依然是開發者與情報員的「後門」首選。
以下是針對 Kazuha Invest 2.0 的實際落實詳情：
1. 核心技術詳解：.json 萬能端點
這不是正式的 API，而是 Reddit 網頁端的數據鏡像，其最大優點是 無需註冊、無需 OAuth 驗證。
 * 基礎邏輯：在任何 Reddit 列表或帖子 URL 後面加上 .json。
 * 請求限制 (Rate Limits)：
   * 非驗證請求：受限於 IP，通常每分鐘僅允許 10-60 次 請求。
   * 關鍵細節：強烈建議在 Header 中自定義 User-Agent（格式見下文），否則極易被判定為惡意爬蟲而遭 429 封鎖。
2. 搜尋與監控參數 (URL Query Parameters)
要精準抓取情報，你必須善用 URL 參數來縮小「過濾塔」的入口：
| 參數 | 作用 | 實戰建議 |
|---|---|---|
| limit | 每次抓取的數量 | 最大值為 100（默認 25）。 |
| t | 時間範圍 | 可選 hour, day, week, month, year, all。 |
| sort | 排序方式 | 獵人模式推薦用 new (抓即時) 或 rising (抓熱點)。 |
| after | 分頁標記 | 抓取第一頁後，用 JSON 中的 after ID 進行滾雪球式翻頁。 |
3. 三大實戰搜尋場景 (Scout Scenarios)
A. 垂直版塊即時監控 (The Pulse)
 * 目標：監控半導體版塊是否有關於特定公司（如 POET 或 AMD）的技術討論。
 * URL：https://www.reddit.com/r/Semiconductors/new.json?limit=100
B. 全局關鍵詞精準搜尋 (The Sniffer)
 * 目標：在全站範圍內搜尋關於「SMR 核能」的最新專業評價。
 * URL：https://www.reddit.com/search.json?q=SMR+nuclear&sort=new&t=day
 * 參數細節：q 代表關鍵詞，restrict_sr=1 可限制在特定版塊內搜尋。
C. 特定領域專家追蹤 (Expert Tracking)
 * 目標：監控某個公認的技術大神（User）發布的最新觀點。
 * URL：https://www.reddit.com/user/[Username]/submitted.json?sort=new
4. Vibe 實踐：防止封鎖的「誠實」原則
雖然是 $0 方案，但在 2026 年，Reddit 對 User-Agent 的檢查非常嚴格。
 * 錯誤做法：使用默認的 python-requests/2.x.x 或 Mozilla/5.0。這會被直接丟進「限流黑洞」。
 * 正確格式：<平台>:<應用ID>:<版本> (by /u/<你的用戶名>)。
   * 範例：User-Agent: macos:KazuhaInvestV2:v1.0 (by /u/KazuhaAdmin)。
5. AI 過濾細節：MiMo-V2 的職責
由於 Reddit 的 JSON 回傳包含大量廢話（HTML 代碼、CSS 類名、無關 Meta），你需要讓 OpenRouter 的免費模型 執行以下動作：
 * 內容蒸餾：只提取 JSON 中的 data['children'][i]['data']['selftext']（正文）和 title（標題）。
 * 噪音剔除：直接刪掉點讚數為 0 或明顯是廣告的帖子。
 * 情緒標註：將技術討論標註為「興奮（Excited）」或「質疑（Skeptical）」。
💡 導師的「澄清問題」：
 * 分頁深度：在進行「遞歸搜尋」時，你希望 Reddit 搜尋向下挖多少頁？（建議 2 頁/200 條，因為 Reddit 的資訊衰減極快）。
 * 關鍵詞容錯：Reddit 用戶常使用縮寫（如 Semi 代表 Semiconductors），你是否希望系統在第一步擴展時自動補全這些「黑話」？
你想讓我為你寫一個專門處理 Reddit JSON 並自動提取 selftext 的 Python 邏輯函數嗎？這能直接對接你的「銜尾蛇迴路」。


在 2026 年初的 OpenRouter 免費模型陣容中，你擁有了極其豪華的「異構算力」。這不僅是免費，更是不同廠商、不同架構（MoE, Transformer, Mamba）的智慧碰撞。
針對你的 Kazuha Invest 2.0 搜尋引擎，我建議將工作分配如下。這套配置旨在利用各模型的「天賦」來完成從感知到決策的五角星流程。
1. 搜尋前端與意圖擴張 (Query Expansion & Sensing)
推薦模型：Gemini 2.0 Flash Experimental (free)
 * 理由：它是目前免費模型中的「速度與感官之王」。其 1M 的超長上下文和強大的工具調用能力（Function Calling），能將你的模糊意圖快速裂變成精準的搜尋組合。
 * 任務：
   * 將你的主意圖（如「核能」）轉化為 5-10 個專業搜尋詞（Query Expansion）。
   * 初步讀取搜尋結果的 Snippets，判斷哪些連結值得點開。
2. 資料蒸餾與結構化提取 (Scraping & Data Cleaning)
推薦模型：Qwen3 Coder 480B A35B (free) 或 Nemotron Nano 12B 2 VL (free)
 * 理由：
   * Qwen3 Coder：專為 Agentic 任務優化，極擅長處理 HTML 並輸出精準的 JSON/Markdown。262K 的上下文足以一次處理數篇長文。
   * Nemotron Nano 2 VL：如果你抓到的資料包含公司財報圖表或趨勢圖，它是免費模型中解讀視覺數據最強的，適合將圖片轉化為文字數據。
 * 任務：
   * 清洗 HTML 雜質，提取核心內容。
   * 將非結構化文本轉化為 Search_Result.json。
3. 多視角會診與初級過濾 (Committee & Filtering)
推薦模型：GLM 4.5 Air (free)
 * 理由：GLM-4.5-Air 是專門為「Agent 中心應用」設計的輕量旗艦。它在 BrowseComp (網頁瀏覽) 和 Tool Use (工具調用) 上的成功率極高。它能精準判斷這則新聞是否符合你的「投資Rubric」。
 * 任務：
   * 擔任「專家委員會」的主席，對初步提取的數據進行評分（0-100）。
   * 標註新聞的「財務影響」與「技術影響」。
4. 深度邏輯辯論與極限生存 (Red/Blue Team & Reasoning)
推薦模型：DeepSeek R1 0528 (free) 或 DeepSeek R1T Chimera (free)
 * 理由：這是你的「重灌算力」。R1 系列代表了當前開源最強的推理 (Reasoning) 能力。
   * R1 0528：適合最嚴苛的紅藍辯論，它具備「慢思考」特質，會自己反覆推敲邏輯漏洞。
   * Chimera：結合了 R1 的推理與 V3 的效率，適合處理更長、更複雜的二階推演（如「格陵蘭礦產 -> 供應鏈中斷 -> CRML 估值變動」）。
 * 任務：
   * 執行 紅藍軍對抗 與 事前驗屍 (Pre-Mortem)。
   * 生成 多重宇宙 (Bull/Bear/Base) 劇本。
5. 銜尾蛇品質監核與最終合成 (Ouroboros & Synthesis)
推薦模型：Kimi K2 0711 (free) 或 Llama 3.1 405B (free)
 * 理由：
   * Kimi K2：1 兆參數級別的 MoE，極其擅長整合複雜資訊並生成流暢、高品質的最終報告。
   * Llama 3.1 405B：雖然它是上一代的王者，但在「指令遵循（Instruction Following）」和總結能力上依然極其穩健，適合做最後的「主編」。
 * 任務：
   * 執行 銜尾蛇迴路 (Ouroboros) 的最後打分。
   * 將所有辯論、推演和數據，合成那份傳送到你手機的 Daily Alpha Report。
🏛️ Kazuha 2.0 算力分配一覽表
| 階段 | 職能 | 推薦模型 (OpenRouter:free) | 亮點 |
|---|---|---|---|
| 感知 | 搜尋詞擴展 | Gemini 2.0 Flash | 極速、多模態感知 |
| 提取 | HTML 轉 Markdown | Qwen3 Coder | 強大的結構化輸出與長上下文 |
| 篩選 | 相關性打分 | GLM 4.5 Air | 頂尖的 Agent 工具執行力 |
| 決策 | 紅藍對抗、深度推理 | DeepSeek R1T Chimera | 結合 R1 推理與 V3 效率 |
| 精修 | 最後打分與合成 | Kimi K2 / Llama 405B | 參數規模巨大，文筆穩健 |
💡 實作建議：如何用代碼「調度」這一切？
既然你有 Code Plan，你可以寫一個 ModelFactory 類。
當你需要執行搜尋時，調用 ModelFactory.get_sensing_model()；
當進入深挖環節，調用 ModelFactory.get_reasoning_model()。
下一步行動：
你想讓我幫你寫出這個 「異構算力調度器」 的 Python 代碼嗎？它可以讓你一鍵切換不同階段使用的 OpenRouter 模型，並自動處理免費模型的 Rate Limit（頻率限制）。

這是在投資情報中極具「降維打擊」能力的數據源。ImportYeti（及類似的海關數據平台）提供的 海關提單 (Bill of Lading, B/L) 是實體經濟的「誠實記錄」。公司可以說謊，但每週運進港口的貨櫃數量不會說謊。
以下是針對 Kazuha Invest 2.0 整合 ImportYeti 數據的實際詳細資料與落實建議：
1. 核心數據詳解：提單 (Bill of Lading) 裡有什麼？
每一份提單都包含以下關鍵字段，這些是 AI 進行「供應鏈推演」的基礎素材：
 * Consignee (收貨人)：通常是你的目標公司（如 Tesla, Apple）。
 * Shipper (發貨人)：這是最值錢的信息——誰是它的供應商？
 * Product Description (貨物描述)：通常包含技術關鍵詞（如 "Lithium-ion batteries", "Uranium concentrate", "Optical Interconnects"）。
 * Quantity/Weight (數量/重量)：用於衡量產能。如果重量連續三個月下滑，該公司下一季的財報大概率會「暴雷」。
 * Date (日期)：捕捉供應鏈的時差（從發貨到入帳通常有 1-2 個月的滯後）。
2. 免費層級的實戰技巧 (The $0 Strategy)
ImportYeti 的網頁版對免費用戶非常慷慨，你可以透過以下方式進行「手動觸發，AI 讀取」：
A. 供應商更替監控 (Supplier Shift)
 * 操作：搜尋 Tesla，查看其供應商列表。
 * 信號：如果突然出現一家從未聽過的中國或越南廠商，且貨物描述是「Prototype parts」，這通常代表新一代產品的供應鏈已成型。
B. 垂直領域「獵殺」 (Niche Hunting)
 * 操作：不搜尋公司名，而是搜尋 關鍵材料。
 * 例子：搜尋 "Uranium Ore" 或 "HALEU feedstock"。
 * 價值：你會發現哪些小公司正在大量進口這些戰略物資，這些公司往往是尚未被市場發現的 Alpha。
3. Kazuha 2.0 的自動化落實 (Integration)
由於 ImportYeti 沒有提供免費 API，且對爬蟲有一定防火牆，我們需要採用 「事件驅動型 (Event-driven)」 的策略，避免大規模掃描。
實施細節：
 * 觸發 (Trigger)：當 scout_gov.py 發現某公司獲得政府大單（如 DOE 的鈾濃縮單），或 scout_news.py 發現某技術突破。
 * 查詢 (Query)：利用 Code Plan 寫一個簡單的 Selenium 或 Playwright 腳本，模擬瀏覽器打開 ImportYeti 該公司的頁面。
 * 提取 (Extract)：
   * 截取「Top Suppliers」圖表。
   * 丟給 OpenRouter 的 Nemotron Nano 2 VL (free)。
   * AI 任務：讀取截圖中的供應商名稱和出貨頻率，並對比去年的數據。
 * 推演 (Reasoning)：
   * 如果供應商 A 的貨量大增，而供應商 A 是某上市公司 B 的子公司 -> 買入 B。
4. 需要留意的細節 (The Pitfalls)
 * 海運限制：ImportYeti 主要提供 海運 (Sea Freight) 數據。如果公司使用空運（如高價值的芯片或藥品），數據會不完整。
 * 代理掩蓋：大型公司（如 Apple）有時會使用「Logistics Global」之類的代理公司名義進口，隱藏真實供應商。
 * 時效性：海關數據通常有 3-10 天 的延遲，適合中長線佈局，不適合超短線炒作。
⚖️ 導師的「深度擴張」建議
為了極大化搜尋深度，你可以將 ImportYeti 與 勞動力數據 結合：
> 邏輯：
>  * ImportYeti 發現某公司開始進口大量「矽光子測試設備」。
>  * Indeed/LinkedIn 監控 發現該公司同步招聘 20 名「CPO 封裝工程師」。
>  * 結論：該公司正處於從研發轉向產能擴張的轉折點，Conviction Score 直接給 95 分。
> 
你想讓我幫你寫一個簡單的「網頁數據抓取與視覺 AI 分析」的流程模板嗎？這可以讓你以後只需要輸入一個公司網址，Kazuha 就能自動去 ImportYeti 幫你找供應商秘密。

勞動力數據（Labor Market Data）是投資中最被低估的「領先指標」。當一份財報說公司「看好未來」時，那是過去的總結；但當公司開始在 LinkedIn 招聘 50 名「晶片封裝工程師」時，那是未來的預告。
針對你的 Kazuha Invest 2.0，以下是將「招聘趨勢」轉化為「投資信號」的實戰細節：
1. 數據源：如何「免費且高效」地抓取？
直接申請 LinkedIn/Indeed 的官方 API 對個人開發者極其困難且昂貴。我們採用「側面進攻」策略：
A. Google Dorking (搜尋引擎黑客語法)
這是最簡單且 $0 成本的方法。利用 Google 的索引來繞過 LinkedIn 的登入限制。
 * 指令範例：site:linkedin.com/jobs "POET Technologies" "Photonics"
 * Vibe 策略：讓你的 Cloud_Senses 每天跑一次這個搜尋，並記錄結果數量的變化。
 * 優化：搜尋時加上時間限制（如 past 24 hours），只看最新增量。
B. 公司官網 Careers 頁面 (Direct Monitoring)
大型公司通常使用 Workday 或 Greenhouse 等招聘系統。
 * 技術路徑：不抓整個網頁，只抓其「Job List」部分的 JSON 接口（通常在瀏覽器 Network 標籤裡能找到一個 api/v1/jobs 之類的連結）。
 * Vibe 實踐：利用 OpenRouter 的 Qwen3 Coder 編寫一個針對特定公司（如 NVIDIA 或 ASML）官網的專屬 Scraper。
2. 情資矩陣：不同崗位代表什麼信號？
並非所有招聘都是好消息。你需要讓 Local Brain 根據崗位類別進行權重分配：
| 招聘崗位類型 | 投資信號 (Vibe Context) | 信心指數 (Conviction) |
|---|---|---|
| R&D / 核心工程師 | 技術突破前期。正在解決底層問題，適合長線埋伏。 | ⭐⭐⭐⭐⭐ |
| Sales / 業務開發 | 商業化轉折點。產品已成熟，準備大規模進入市場（營收即將爆發）。 | ⭐⭐⭐⭐ |
| Finance / 合規官 | IPO 準備或法律風險。如果突然招大量法律顧問，可能面臨訴訟。 | ⚠️ 警報 |
| HR / 行政 | 常規擴張。代表公司現金流穩定，但非核心技術利好。 | ⭐ |
3. 如何利用「遞歸搜尋」深化招聘情報？
這就是你提到的「重複兩三步」的精髓。
 * 第一步 (感知)：發現 NVIDIA 正在加州招聘 "CPO Package Engineer" (共同封裝光學工程師)。
 * 第二步 (遞歸提取)：
   * 提取關鍵字："CPO Package", "Glass Substrate"。
   * 二次搜尋：搜尋哪些小公司也在招同樣的人，或者這類工程師通常來自哪裡？
 * 第三步 (發現 Alpha)：你發現這些工程師很多來自一家名為 "X-Silicon" 的未上市小公司，而這家公司剛被某上市公司 A 入股。
 * 結果：你在市場發現「矽光子」熱潮前，就鎖定了上市公司 A。
4. 實作細節與留意事項
在執行「勞動力數據監控」時，你需要留意以下「噪聲」：
 * Ghost Postings (影子職缺)：有些公司為了維持「公司還在成長」的假象，會長期掛著不招人的職缺。
   * 對策：監控職缺的「發布日期」。如果一個職缺掛了 180 天沒動，直接在過濾階段扣 50 分。
 * 人才外流 (Brain Drain)：
   * 進階技巧：監控 LinkedIn 上「曾在 A 公司工作，現已離職」的人數。如果核心技術團隊集體跳槽到競爭對手 B，這是極強的賣出 A、買入 B 指標。
 * 地理位置相關性：
   * 如果招聘發生在「馬來西亞」或「越南」，通常代表降低成本/產能遷移。
   * 如果招聘發生在「矽谷」或「特拉維夫」，代表核心技術創新。
5. 算力分配建議
由於招聘描述通常很長且充滿廢話，請這樣分配 OpenRouter 模型：
 * 初篩 (Filtering)：用 Gemini 2.0 Flash (free) 快速掃過 100 個職位標題，刪除行政和後勤職位。
 * 深度解讀 (Reasoning)：用 DeepSeek R1 0528 (free) 閱讀核心崗位的 "Job Description"。
   * 任務：分析其要求的技能（Skills）。如果要求熟悉某種「特定新技術」，這就是該公司未來的祕密武器。
導師的建議與問題：
這套「勞動力數據」模組將使你的 Kazuha 2.0 具備真正的「預知能力」。
目前我需要向你澄清一個細節：
針對「公司官網 Careers」，你是希望系統全天候監控你整個 Portfolio（例如 20 間公司），還是當「新聞感應器」發現異動時，才觸發遞歸搜尋去查該公司的招聘情況？（前者更完整但算力消耗大，後者更精準、更具獵人體感）。
你想讓我幫你寫一個針對 LinkedIn Jobs 的搜尋詞優化器 (Query Optimizer) 嗎？它可以確保你的 $0 搜尋方案能避開垃圾資訊。


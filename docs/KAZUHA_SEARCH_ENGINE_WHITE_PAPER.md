# Kazuha Invest 2.0: 搜索引擎與情資獵殺提升白皮書

> **核心主題**：從「被動接收新聞」轉向「主動溯源獵殺」
> **技術邏輯**：混合數據流 (Hybrid Streams) + 遞歸滾雪球 (Recursive Snowballing)

本白皮書系統性地整理了 Kazuha Invest 2.0 的擴張策略與技術實作細節，旨在建立一個具備「垂直深度」與「全球闊度」的情報網。

---

## 1. 數據源闊度擴張：三大情報支柱 (The Three Pillars)

為了突破大眾媒體的「滯後性」，系統將搜索觸角伸向數據的「第一現場」。

### 1.1 支柱一：政府與監管源頭 (The "Follow the Money" Stream)
**核心邏輯**：官方合約與法規是投資邏輯的「底牌」，通常領先於新聞報導。

#### A. 核心數據源與監控目標
1.  **SAM.gov (聯邦合約) & US Spending**
    *   **任務**：監控聯邦政府合同中標 (Award Notices) 及分包合同報告 (Subaward Reports，2026 年起轉移至 SAM.gov)。
    *   **價值**：捕捉國防部 (DoD)、能源部 (DOE) 的高額撥款，是發現 Alpha 的捷徑。中標通知通常早於新聞。
    *   **API 實作重點**：
        *   **SAM.gov API**：
            *   `Get Opportunities Public API`：實時獲取採購意向、招標書及中標通知。
            *   `Contract Awards API`：獲取已簽署合同細節（金額、得標者）。
            *   `Exclusions API` (Shield)：查詢黑名單公司，作為持倉風控（賣出信號）。
        *   **US Spending API** (`api.usaspending.gov`)：
            *   `/api/v2/search/spending_by_award/` (Hunter)：使用 `keywords`, `time_period`, `agencies`, `naics_codes` 等過濾器搜尋特定合同。
            *   `/api/v2/awards/<AWARD_ID>/`：獲取單筆獎勵詳情。
            *   `/api/v2/transactions/` & `/api/v2/download/awards/`：分析資金變動趨勢與批量下載。
    *   **進階分析工具**：
        *   **CALC API (Contract-Awarded Labor Category)**：查詢專業勞動力（如 AI 工程師）的中標時薪。若某公司報價顯著高於平均，代表具備高護城河 (Moat)。
2.  **Federal Register (聯邦公報) & Regulations.gov**
    *   **任務**：監控政策變動、法規草案及公眾評論。
    *   **價值**：預判政策紅利或阻礙（如核能、無人駕駛法規）。
    *   **細節**：監控如 NHTSA (交通安全局) 的缺陷調查，能在利空爆發前預警。
3.  **SEC EDGAR (財經真相)**
    *   **任務**：監控上市公司重大申報。
    *   **關鍵端點**：
        *   **8-K (重大事項)**：收購、高管變動、破產等突發利好/利空。
        *   **13F (機構持倉)**：追蹤「聰明錢」動向。
        *   **Company Facts**：XBRL 財務數據自動化分析。
    *   **實作注意**：
        *   需嚴格遵守 User-Agent 規範 (包含聯繫電郵) 及 10 req/sec 頻率限制。
        *   **CIK 格式**：API 要求 10 位數 CIK，不足需前補零 (如 Apple: `0000320193`)。
        *   可參考 `submissions` 端點下的 `recent` 字典解析 8-K/13F。
4.  **USPTO (專利局)**
    *   **價值**：從專利申請識別技術路線（如矽光子、固態電池），領先產品發布 2-3 年。
5.  **ClinicalTrials.gov (生物醫藥)**
    *   **任務**：監控新藥臨床試驗進度與結果，埋伏生技股指標。

---

### 1.2 支柱二：社交情緒與專家網絡 (The "Wisdom of Crowds")
**核心邏輯**：過濾散戶雜音，提取技術專家的討論，因為技術人員的看法往往領先於分析師評級。

#### A. Hacker News (YC)
*   **價值**：矽谷技術圈風向標。若開源項目或論文爆紅，代表市場敘事 (Narrative) 即將轉向。
*   **API 實作 (Firebase)**：
    *   **遞歸抓取**：利用 `kids` 字段深入抓取評論樹。
    *   **策略**：掃描 `topstories`，用 AI 提取技術關鍵字；若相關度高，深入分析評論情緒。
    *   **高效模式**：監控 `maxitem` 與 `updates` 端點，精準捕捉最新討論；利用 `user/{id}` 端點檢查發文者 Karma 與歷史，驗證專家身分。

#### B. Reddit (Niche Subreddits)
*   **價值**：針對專業看板（如 r/Semiconductors, r/Networking, r/NuclearPower）進行爬取，獲取技術人員對產品缺陷或突破的真實討論。
*   **$0 方案技術細節**：
    *   **方法**：使用 `.json` 端點 (如 `/r/Semiconductors/new.json`)。
    *   **避坑指南**：必須自定義 User-Agent (如 `macos:KazuhaInvestV2:v1.0`) 以免被 429 封鎖。
    *   **參數技巧**：善用 `limit=100`, `sort=new`。
    *   **AI 過濾**：提取 `selftext` 與 `title`，剔除廣告與低分貼文，標註「興奮」或「質疑」情緒。

#### C. X (Twitter) Lists
*   **任務**：透過特定「聰明錢」與「技術大 V」名單，捕捉第一手市場脈搏。

---

### 1.3 支柱三：供應鏈與勞動力數據 (The "Supply Chain" Stream)
**核心邏輯**：供應鏈變動與招聘趨勢是企業擴張最誠實的信號（誠實記錄）。

#### A. 供應鏈數據 (ImportYeti / 海關)
*   **核心價值**：海關提單 (Bill of Lading) 不會說謊。
*   **監控指標**：
    *   **Shipper (發貨人)**：發現隱藏的供應商關係。
    *   **Quantity/Weight**：重量下滑預示財報暴雷；激增代表產能擴張。
    *   **Product Description**：識別技術關鍵詞（如 "Uranium concentrate"）。
*   **操作策略**：
    *   **事件驅動**：當新聞/政府合約觸發信號時，才啟動腳本去查 ImportYeti。
    *   **AI 視覺分析**：截取「Top Suppliers」圖表，用視覺模型 (如 Nemotron Nano 2 VL) 讀取並分析。
    *   **限制與注意**：數據通常有 3-10 天延遲；留意大公司使用「Logistics Global」等代理掩蓋真實供應商。

#### B. 勞動力數據 (Labor Market)
*   **核心價值**：招聘是未來的預告。
*   **監控渠道**：
    *   **Google Dorking**：`site:linkedin.com/jobs "Company" "Keyword"` ($0 成本)。
    *   **公司官網 Careers**：針對重點持倉 (Portfolio) 直接監控 JSON 接口。
*   **信號解讀矩陣**：
    *   **R&D/核心工程師** (⭐⭐⭐⭐⭐)：技術突破前期。
    *   **Sales/BD** (⭐⭐⭐⭐)：商業化轉折點，營收即將爆發。
    *   **Legal/Finance** (⚠️)：可能面臨 IPO 準備或訴訟風險。
*   **噪聲過濾**：
    *   **影子職缺 (Ghost Postings)**：監控發布日期，若掛單 > 180 天無變動，直接過濾或扣分。
    *   **人才外流 (Brain Drain)**：監控核心團隊跳槽至競爭對手 (賣出信號)。
    *   **地理位置相關性**：越南/馬來西亞招聘 = 產能擴張/降本；矽谷/特拉維夫 = 核心技術創新。

---

## 2. 搜尋深度提升：遞歸滾雪球策略 (Recursive Snowballing)

單次搜索只能觸及表面，遞歸搜索將資訊深度從「一階」推進到「三階」。

### A. 關鍵字裂變與提取 (Extraction)
*   **角色**：利用 OpenRouter 免費弱模型 (Gemini Flash/Nemotron Nano)。
*   **動作**：從第一波摘要提取 5 個核心名詞（技術代號、CEO、供應商），強調「只要名詞，不准解釋」。

### B. 頻率與關聯分析 (Co-occurrence)
*   **邏輯**：多來源同時提及冷門名詞（如 "CPO - Co-Packaged Optics"），自動提升為「高優先級」標籤，觸發二輪搜索。

### C. 多樣性過濾 (Diversity Filter)
*   **做法**：AI 產出 3 個「不同維度但高度相關」的延伸查詢（從「產品」延伸到「關鍵材料商」）。

---

## 3. 風控機制：防止主題漂移 (Topic Drift Control)

設立「安全閥」防止搜尋範圍無限擴大。

### A. 相關性門檻 (Relevance Gate)
*   **規則**：啟動二輪搜索前，模型對關鍵字打分 (0-10)。僅 > 8 分者進入下一輪。

### B. 負向過濾 (Negative Filtering)
*   **動作**：剔除寬泛詞 (Investment, AI)，保留具體詞 (Uranium Enrichment)。

### C. 深度限制 (Depth Limit)
*   **Loop 0**：核心意圖。
*   **Loop 1**：擴展搜索。
*   **Loop 2**：供應鏈/監管細節。
*   **Loop 3**：系統自動停止（噪音 > 信號）。

---

## 4. 技術架構：倒漏斗情資工廠 (The Funnel) & 算力調度

採用「異構算力 (Heterogeneous Compute)」配置，利用 OpenRouter 免費模型陣容。

### 4.1 處理流程
1.  **廣度掃描 (Cloud Scout)**：產生多重關鍵詞，抓回海量摘要。
2.  **精確過濾 (Model Filter)**：篩選高權重 URL。
3.  **遞歸深挖 (Recursive Search)**：執行 Loop 1 & 2 補充調查。
4.  **五角星推理 (Local Brain)**：最後進行深度補完、紅藍對抗與多重宇宙推演。

### 4.2 算力分配矩陣 (OpenRouter Free Tier)

| 階段 | 職能 | 推薦模型 | 具體任務 |
| :--- | :--- | :--- | :--- |
| **1. 感知** | 搜尋詞擴展 | **Gemini 2.0 Flash** | 利用 1M 上下文與工具調用，將意圖裂變為精準搜尋組合；初步判斷 Snippets。 |
| **2. 提取** | 數據清洗/結構化 | **Qwen3 Coder** / **Nemotron Nano 2 VL** | Qwen 處理 HTML 轉 Markdown/JSON；Nemotron 處理財報圖表與視覺數據。 |
| **3. 篩選** | 相關性打分 | **GLM 4.5 Air** | 擔任「專家委員會」，對資訊進行評分 (0-100) 與財務/技術影響標註。 |
| **4. 決策** | 深度推理/紅藍對抗 | **DeepSeek R1 / Chimera** | 執行慢思考邏輯辯論、事前驗屍 (Pre-Mortem)、多重宇宙劇本推演。 |
| **5. 精修** | 最終合成 | **Kimi K2** / **Llama 3.1 405B** | 執行銜尾蛇迴路 (Ouroboros) 最後打分，合成 Daily Alpha Report。 |

---

## 5. 待確認事項與實作建議 (From Tutor)

### A. 需要確認的細節
1.  **相關性分數容錯度**：7.5 分關鍵字是直接丟棄，還是存入「待觀察區 (Watchlist)」？
2.  **遞歸觸發條件**：建議僅對「Impact Score > 80」的新聞進行深挖，以節省算力。
3.  **持倉防禦深度**：針對 Portfolio 持倉，是否應更嚴格監控其競爭對手？
4.  **招聘監控範圍**：全天候監控 Portfolio，還是由新聞信號觸發遞歸查詢？（建議後者，具備獵人體感）。

### B. 技術實作提醒
1.  **User-Agent**：所有爬蟲（SEC, Reddit, etc.）必須設置合規 User-Agent。
2.  **Rate Limiting**：嚴格遵守各平台頻率限制，腳本需包含 `time.sleep`。
3.  **API Keys**：SAM.gov 需申請 Key；其他多數為開放數據。
4.  **代碼模組化**：建議編寫 `ModelFactory` 類別來調度不同階段的 AI 模型。

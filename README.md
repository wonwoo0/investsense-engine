這是一份集大成之作。這份白皮書整合了我們從最初的 API 討論，到 Copilot Pro 的應用，再到剛剛補充的三大盲點（通知、防禦、回饋），構建出的 **Kazuha Invest 2.0 終極架構**。

這不僅是文檔，更是你接下來開發的 **「施工圖紙」**。

---

# 📄 Kazuha Invest 2.0: The Anticipatory Intelligence System

**Project Codename:** `Vibe-Hunter`
**Status:** Architecture Finalized (Jan 2026)
**Core Philosophy:** From "Passive Indexing" to "Active Anticipation"

---

## 1. 核心願景 (The Vision)

系統不再是一個等待指令的「資料整理器」，而是一個 24/7 運行的「自主投資生命體」。

* **目標**：在新聞成為主流敘事之前（Time Arbitrage），捕捉二階效應（如格陵蘭 -> 稀土 -> CRML）。
* **手段**：利用「雲端感應」突破網絡限制，利用「本地算力」進行深度推演。
* **結果**：不僅提供資訊，更提供 **信心 (Conviction)** 與 **警報 (Alerts)**。

---

## 2. 混合架構拓撲 (Hybrid Architecture Topology)

我們採用 **「雲端感知 (Sensing) + 本地思考 (Reasoning)」** 的分離式架構，並由 **Copilot Pro** 擔任運維中樞。

### A. 雲端感知層 (The Cloud Senses)

* **基礎設施**：GitHub Actions (US IP Runner)。
* **運維指揮**：**GitHub Copilot Pro ($10/mo)** —— 負責自動生成 YAML、修復報錯、監視日誌。
* **任務**：
1. **獵殺 (Hunting)**：廣度掃描未知機會 (DDG)。
2. **防禦 (Shielding)**：**[NEW]** 針對持倉進行負面監測。
3. **閱讀 (Reading)**：利用 **Jina** 將網頁蒸餾為 Markdown。
4. **通知 (Notifying)**：**[NEW]** 高權重信號直接推送到手機。



### B. 本地大腦層 (The Local Brain)

* **基礎設施**：你的本地電腦 (Coding Plan Environment)。
* **核心算力**：無限本地推理 (Cursor/Windsurf) + 多模型切換 (GPT-4o / Claude 3.7)。
* **任務**：
1. **深度推演**：二階思考、紅藍軍辯論。
2. **結構重組**：動態調整目錄結構 (Taxonomy Refactoring)。
3. **進化回饋**：**[NEW]** 月度回測與邏輯修正。



---

## 3. 功能模組詳解 (Core Modules)

### 模組一：全域偵測矩陣 (The Detection Matrix)

*位置：雲端 (GitHub Actions)*

1. **`scout_hunter.py` (獵人)**
* **邏輯**：基於「異動偵測」。掃描不在追蹤列表中的熱詞（如 "Greenland"）。
* **工具**：`duckduckgo-search` (News mode)。


2. **`scout_shield.py` (護盾) [NEW]**
* **邏輯**：鎖定 `Portfolio/` 中的公司列表，專門搜索風險詞（"Lawsuit", "Fraud", "Delay", "Short Seller"）。
* **觸發**：一旦發現，標記為 `DEFCON_1` 緊急級別。


3. **`scout_reader.py` (閱讀者)**
* **邏輯**：接收上述偵測到的 URL，通過 `r.jina.ai` 抓取內容，並進行「初級去重」。
* **輸出**：存入 `Incoming/raw_intents.json`。



### 模組二：二階思考引擎 (The Second-Order Engine)

*位置：本地 (Local Brain)*

1. **`brain_reasoning.py` (推演)**
* **輸入**：讀取 `Incoming/` 數據。
* **過程**：
* *關聯掃描*：這個新聞跟 1 年前的 `Macro/` 筆記有關嗎？
* *假設生成*：如果 A 發生，誰是受益的 B？(Auto-Ticker Mapping)。
* *估值檢核*：這是不是類似 SNDK 的分拆機會？


* **輸出**：生成 `Reports/Daily_Alpha.md`。


2. **`brain_review.py` (回饋迴路) [NEW]**
* **時機**：每月 1 號運行。
* **邏輯**：回測上個月 `High Confidence` 標記的資產表現。
* **修正**：如果準確率低，自動調整 `prompts/scoring_rubric.md` 的評分權重。



### 模組三：最後一哩路觸達 (The Last Mile)

*位置：雲端 + 手機*

1. **`notifier.py` (傳令兵) [NEW]**
* **工具**：Telegram Bot API 或 Discord Webhook (免費)。
* **邏輯**：
* 一般報告 -> 靜默更新 (Git Push)。
* **Alpha Alert (信心 > 85)** -> **即時推送**：「🚀 發現結構性機會：CRML (格陵蘭稀土)，建議立即查看。」
* **Shield Alert (風險 > 90)** -> **即時推送**：「⚠️ 持倉預警：XYZ 公司面臨做空機構報告。」





---

## 4. 數據與存儲策略 (Data Strategy)

採用 **「全新開始 (Clean Slate)」** 策略。

* **Repo**：建立新倉庫 `Kazuha-Invest-V2`。
* **遷移**：僅將 V1 的 `Data/` 目錄拷貝過來，舊腳本封存。
* **格式**：
* ❌ 不存 HTML (避免 Repo 膨脹)。
* ✅ 只存 Markdown (Jina 處理後) 與 JSON (結構化數據)。


* **Metadata**：所有文件必須包含 tags（如 `#Geopolitics`, `#Rare_Earths`），以便 Copilot 進行跨文件索引。

---

## 5. 技術堆棧與成本 (Tech Stack & Cost)

根據實測與成本效益分析，我們調整為 **「雙倉庫 (2-Repo)」** 策略，最大化運用免費資源並保障私隱。

| 組件 | 選擇工具 | 成本 | 作用 | 備註 |
| --- | --- | --- | --- | --- |
| **Repo Strategy** | **2-Repo System** | Free | `Engine` (Public) 放代碼, `Data` (Private) 放持倉 | 平衡開源與私隱 |
| **Compute (Cloud)** | **GitHub Actions** | Free | 負責定時掃描 (7AM/9PM) | Public Repo 無限分鐘 + Private Data Clone |
| **Compute (Local)** | **Gemini 2.5 Pro / DeepSeek V3** | Free / Low Cost | 二階推理、報告生成 | 取代 Copilot Pro |
| **Search** | DuckDuckGo Search | Free | 廣度發現新聞 | 需注意 Rate Limit |
| **Reading** | Jina Reader API | Free (Tier) | 網頁轉 Markdown、去重 | 需確認用量上限 |
| **Embedding** | Gemini text-embedding-004 | Free | 語義去重 (Semantic Deduplication) | 高效過濾重複內容 |
| **Notification** | Telegram Bot | Free | **只推** 極高風險 (DEFCON 1) | 避免疲勞轟炸 |

---

## 6. 實施路線圖 (Implementation Roadmap)

### Phase 0: 基礎架構 (The Foundation) - [即時]
1. **建立雙倉庫**：
    - `kazuha-invest-engine` (Public): 核心代碼、GitHub Actions workflow。
    - `kazuha-invest-data` (Private): Portfolio.yml、生成的 Reports、JSON 數據。
2. **配置 Secrets**：在 Public Repo 設定 `PAT_TOKEN` 以讀寫 Private Data Repo。

### Phase 1: 感官與簡報 (The Sense Maker) - [本週]
*目標：每日兩次 (7:00 AM, 9:00 PM) 自動生成簡報，不求快但求理解。*

1. **部署 `daily_brief.yml`**：設定 Cron Job，自動 trigger 掃描。
2. **實裝 `scout_hunter.py`**：接入 DDG + Jina，實現基礎 Hash 去重。
3. **實裝 `scout_shield.py`**：讀取 Private Repo 的 `portfolio.yml`，針對持倉進行風險掃描。
4. **輸出**：確保 Report 能自動 git push 回 Private Repo 的 `Reports/` 目錄。

### Phase 2: 大腦與推理 (The Brain) - [下週]
*目標：從單純的新聞堆砌，進化為有邏輯連結的二階思考。*

1. **開發 `brain_reasoning.py`**：
    - 接入 Gemini 2.5 Pro 或 DeepSeek V3 API。
    - 實作 **「語義去重」** (利用 Gemini Embeddings)。
    - 加入 Prompt 邏輯：「如果 A 發生，誰是受益的 B？」。
2. **模型競技 (A/B Testing)**：同時跑兩個模型，人手評估誰的邏輯推演更準確。

### Phase 3: 緊急機制與優化 (Alerts & Evolution) - [未來兩週]
1. **智能通知 (Smart Alert)**：
    - 只有當 `Risk Score > 90` 或 `Confidence > 95` 時才發送 Telegram，其餘只寫入報告。
2. **自我修正 (Feedback Loop)**：
    - 記錄每日「高信心」預測，一個月後進行回測 (Calibration)，調整 Prompt 權重。

---

## 7. 風險管理與應對 (Risk Management)

| 風險點 | 潛在影響 | 應對策略 (Mitigation) |
| --- | --- | --- |
| **GitHub Actions 限制** | Private Repo 分鐘數耗盡 | 採用 Public Repo 跑 Logic，只在 Pull/Push Data 時接觸 Private Repo (無限分鐘)。 |
| **Alert Fatigue (疲勞)** | 太多通知導致麻木 | **Strict Filter**: 只有 `DEFCON_1` (如欺詐、停牌、訴訟) 才推，普通波動只列入日報。 |
| **Privacy Leak** | 持倉被公開 | **嚴格分離**：Code 在 Public，Data 在 Private。`.gitignore` 必須包含 `.env` 與 `*.yml`。 |
| **Model Hallucination** | AI 亂作邏輯連結 | **查證機制**：要求 AI 必須附上 Source URL，並在報告中標示「推測」字眼。 |

---

這就是 **Kazuha Invest 2.0 (Refined)** 的完整形態。
它不再追求與機構比拼速度，而是利用 **機器人的勤奮 (24/7 掃描)** 與 **AI 的邏輯 (二階推理)**，為你提供 **開市前的上帝視角 (God-View Briefing)**。

**Next Step:**
現在，請前往 GitHub 建立 `kazuha-invest-engine` (Public) 與 `kazuha-invest-data` (Private)，然後開始 Phase 0 的 `daily_brief.yml` 配置。

---

## 8. 初始觀測範圍 (Initial Universe Scope)

系統啟動日 (Day 1) 將鎖定以下資產與主題，作為首批「感知」對象。

### 🎯 核心持倉 (Core Portfolio)
*警報級別：DEFCON 1 (極高敏感度)*
*   **RKLB** (Rocket Lab)
*   **TSLA** (Tesla)
*   **ONDS** (Ondas Holdings)
*   **POET** (POET Technologies)

### 🌍 宏觀主題 (Macro Themes)
*監測目標：尋找與核心持倉的二階連結 (Alpha)*

| 主題分類 | 關鍵詞示例 (Keywords Intent) |
| :--- | :--- |
| **Advanced Nuclear** | SMR, Uranium, Kairos Power, TerraPower |
| **AI Infrastructure** | Data Centers, Liquid Cooling, GPU Supply Chain |
| **Autonomous Vehicles** | FSD, Robotaxi, Waymo, Regulation |
| **Edge AI Inference** | On-device AI, TinyML, NPU |
| **eVTOL** | Urban Air Mobility, Archer, Joby, FAA Certification |
| **Photonics** | Optical Interconnects, Silicon Photonics, CPO |
| **Solid State Battery** | QuantumScape, Energy Density, EV Range |
| **Space Tech** | Satellite Constellations, Reusable Rockets, Space Debris |
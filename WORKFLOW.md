# 🔄 Kazuha Invest 2.0 Operational Workflow (Vibe-Hunter 2.1 Manual)

本文件詳述 Kazuha Invest 2.0 的 **「異構算力分發 (Heterogeneous Compute) + 深度情資獵殺」** 完整操作流程。這套系統旨在實現從「被動接收」到「主動預知」的投資轉型。

---

## 🏗 架構概覽 (Architecture)

### 1. 雙倉庫體系 (Twin-Repo System)
*   **Engine Repo (Public)**: `investsense-engine`
    *   負責所有自動化腳本、API 調度及 GitHub Actions 工作流。
*   **Data Repo (Private)**: `investsense-data`
    *   負責儲存敏感的持倉數據 (`portfolio.yml`)、情資來源 (`sources.yml`)、原始信號 (`Incoming/`) 及最終報告 (`Reports/`)。

### 2. 異構算力矩陣 (Model Factory)
系統根據任務難度，自動調度 OpenRouter 免費模型陣容：
| 任務階段 | 職能 | 推薦模型 (OpenRouter:free) | 亮點 |
| :--- | :--- | :--- | :--- |
| **感官 (Sensing)** | 抓取、長文閱讀 | Gemini 2.0 Flash | 1M 超長上下文 |
| **提取 (Extract)** | HTML 轉 JSON | Qwen3 Coder | 極強的結構化輸出能力 |
| **篩選 (Filter)** | 相關性打分 | GLM 4.5 Air | 工具執行力高，速度快 |
| **推理 (Reasoning)**| 二階推演 | DeepSeek R1 (Chimera) | 高 IQ 邏輯思維，紅藍對抗 |
| **精修 (Synthesis)**| 報告撰寫 | Llama 3.1 405B | 文筆穩健，指令遵循強 |

---

## 🔄 每日循環流程 (The Daily Loop)

### Step 1: Cloud Scouting (全域偵測)
*自動執行，無需人工干預*
*   **時間**: 每日 07:00 AM & 21:00 PM (HKT)。
*   **動作**:
    1.  **`scout_gov.py`**: 同時監控 **SAM.gov** (未來招標) 與 **US Spending** (歷史合約確認)。
    2.  **`scout_social.py`**: 監控 **Reddit** 垂直技術板塊 (如 r/Semiconductors)。
    3.  **`scout_feed.py`**: 抓取 **RSS** 高權重新聞源 (如 SpaceNews, World Nuclear News)。
    4.  **`scout_shield.py`**: 針對持倉進行 **負面關鍵字掃描** (DEFCON 1 級別)。
    5.  **`scout_hunter.py`**: 基於宏觀主題 (Macro Themes) 的 **機會挖掘**。
    6.  **`scout_labor.py`**: 透過 LinkedIn/Indeed 監控 **人才招聘趨勢**。

### Step 2: Semantic Deduplication (語義去重)
*   **指令**: `uv run -m src.scout_dedup`
*   **邏輯**: 使用 `all-MiniLM-L6-v2` 嵌入模型計算向量相似度。
*   **產出**: 將海量碎片合併為單一 `consolidated_signals.json`。

### Step 3: Local Brain Reasoning (本地/雲端大腦推理)
*   **指令**: `uv run -m src.brain_reasoning`
*   **核心動作**:
    1.  讀取合併後的信號與持倉數據。
    2.  **二階效應分析**: 「如果 A 發生，誰是受益的 B？」
    3.  **幻覺修正**: 自動比對真實合同數據與新聞描述。
    4.  **生成報告**: 寫入 `data/Reports/daily_alpha_YYYYMMDD.md`。

### Step 4: Alpha Alerts (即時警報)
*   **觸發機制**: 當 **Confidence > 85** 或 **Risk Score > 90** 時。
*   **通道**: Telegram Bot 即時推送標題、得分與來源連結。

---

## 🤖 未來 Agent 操作指令 (Protocol)

當你啟動 Kazuha 任務時，請依次執行：
1.  **同步**: `git pull` 獲取最新 `investsense-data`。
2.  **偵測**: 運行所有 `src/scout_*.py` 模組。
3.  **分析**: 運行 `src/brain_reasoning.py` 生成深度報告。
4.  **發布**: 將報告與新數據 `git push` 到私有倉庫。

---

## 🛠 常見問題排除 (Troubleshooting)

### 🔴 數據抓取失敗 (403/429)
*   **SEC/Reddit**: 檢查 `src/config.py` 中的 `USER_AGENT_EMAIL` 是否為真實邮箱。
*   **SAM.gov**: 確保使用的是 **SAM Profile Key** 而非 Data.gov Key。

### 🔴 報告生成失敗 (404 No Route)
*   **OpenRouter**: 檢查 OpenRouter 官網確認該免費模型 ID 是否變更或暫時下架，手動更新 `src/config.py` 中的 `MODELS` 映射。

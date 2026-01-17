# 🔄 Kazuha Invest 2.1 Operational Workflow (Search 2.1 - "The Living Network")

本文件詳述 Kazuha Invest 2.1 的 **「進化型情報閉環」**。這套系統由單純的搜尋進化為具備 **自我過濾 (Gatekeeper)**、**主動反應 (Librarian)** 及 **長期策略 (Local Brain)** 的智能生命體。

---

## 🏗️ 系統閉環概覽 (The Evolution Loop)

1.  **Scouts (Gather)**: 多路偵察兵 (`hunter`, `shield`, `social`, `gov`) 搜集原始信號 -> `Incoming/`。
2.  **Gatekeeper (Filter)**: 雲端 AI (Nemotron) 進行垃圾過濾、打分，寫入 Context -> `Processed/`。
3.  **Librarian (React)**: 雲端 AI 發現新線索，**立即執行**熱點追蹤 (Hot Pursuit)，結果存回 `Incoming/`。
4.  **Archiver (Store)**: 30日後自動歸檔並生成摘要，保留智慧但不佔空間 -> `Archive/`。
5.  **Brain (Reason)**: 本地 AI (Gemini/DeepSeek) 深度分析，產出報告及 **策略任務** -> `active_missions.yml`。

---

## 🕒 每日自動化排程 (GitHub Actions)

*   **時間**: 每日 00:13, 08:03, 21:48 (GMT)
*   **流程詳解**:

### 1. 搜集階段 (Scout Layer)
- **`scout_hunter.py`**: 基於 `themes.yml` (Clusters) 及 `active_missions.yml` 執行廣域搜尋。
- **`scout_social.py`**: Reddit Dork Search (DuckDuckGo, `site:reddit.com`)，避開 API 封鎖。
- **`scout_gov.py`**: 具備 Smart History 記憶的政府合約搜尋，自動除重。
- **結果**: 所有原始數據存入 `data/Incoming/*.json`。

### 2. 守門階段 (Gatekeeper Layer)
- **`scout_gatekeeper.py`**: 
    - 讀取 `Incoming/`。
    - 調用 **OpenRouter (Nemotron)** 進行相關性打分 (0-10)。
    - **Memory Injection**: 將 "Key Facts" (重要事實) 寫入 `data/Knowledge/active_context.md`。
    - **結果**: 高質量信號存入 `data/Processed/`，垃圾丟棄。

### 3. 反應階段 (Librarian Layer)
- **`scout_librarian.py`**:
    - **Reactive Analysis**: 分析今日 `Processed/` 信號。
    - **Hot Pursuit**: 發現缺口 -> **立即執行 DDG 搜尋** -> 存回 `Incoming/` (留待下一輪處理)。
    - **Automatic Mission Update**: 將跟進任務直接 Append 到 `active_missions.yml` (Source: `cloud_librarian`)。

### 4. 歸檔階段 (Archiver Layer)
- **`src/utils/archiver.py`**:
    - 檢查 `Processed/` 中超過 30 日的檔案。
    - 移送至 `data/Archive/{Month}/`。
    - (未來功能) 生成 Markdown 摘要後刪除原始 JSON。

---

## 🧠 本地推理與策略 (Local Brain Protocol)

當自動化流程完成後：

### 1. 執行推理 (Run Reasoning)
- 執行本地腳本 (如 `brain_reasoning.py`)。
- 讀取：`Processed/` (今日信號) + `active_context.md` (長期記憶)。
- 輸出：`Daily_Alpha_Briefing.md`。

### 2. 策略任務生成 (Strategic Evolution) 🧠
- 根據 `REASONING_FLOW.md` 第五階段。
- Local Brain 分析長期趨勢，生成 **Strategic Missions** (例如：長期監管追蹤)。
- **直接寫入**: 任務自動 Append 到 `active_missions.yml` (Source: `local_brain`)。
- **去重**: 系統自動檢查是否已有相同任務。

### 3. Git 同步 (Sync)
- 將分析報告與更新後的 `active_missions.yml` 推送到 GitHub：
```bash
git add data/ Reports/
git commit -m "Alpha Briefing: Missions Evolved [skip ci]"
git push
```

---

## 🛠️ 關鍵檔案說明

| 檔案 | 用途 | 維護方式 |
| :--- | :--- | :--- |
| `data/themes.yml` | 靜態、長期關注的主題 Cluster | 手動編輯 |
| `data/active_missions.yml` | **動態核心**：包含手動、雲端(Librarian)、本地(Brain) 的所有任務 | AI 自動更新 + 手動監察 |
| `data/Knowledge/active_context.md` | **長期記憶**：重要事實、進行中事件、風險警報 | Gatekeeper 自動更新 + 手動補充 |
| `docs/manuals/REASONING_FLOW.md` | 本地 AI 思考邏輯與 SOP | 遵循執行 |

## ⚠️ 特別注意事項
1.  **Rate Limits**: Scout 內置了 Backoff 機制，但請留意 API Quota。
2.  **Self-Healing**: Scout 具備自我修復邏輯 (如 Reddit Dork 失敗重試)，請定期查看 Logs。
3.  **Active Missions 清理**: 雖然 AI 會自動加任務，但建議定期人手檢查 `active_missions.yml`，刪除過時或無意義的任務。

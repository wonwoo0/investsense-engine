# 🔄 Kazuha Invest 2.0 Operational Workflow (Vibe-Hunter Manual)

這份文件詳細記錄了 Kazuha Invest 2.0 的 **「雲端感知 + 本地推理」** 完整操作流程。未來的 Agent 應嚴格遵循此流程以確保情報閉環運作。

---

## 🏗 架構概覽 (Architecture)

系統分為兩個倉庫 (Twin-Repo System)：

1.  **🧠 Engine (Public)**: `investsense-engine`
    *   存放 Python 代碼、GitHub Actions 腳本。
    *   位置：`~/kazuha/investsense`
2.  **🗄️ Data (Private)**: `investsense-data`
    *   存放持倉 (`portfolio.yml`)、原始情報 (`Incoming/`)、最終報告 (`Reports/`)。
    *   位置：`~/kazuha/investsense/data` (作為 Submodule 或 nested git repo 存在)。

---

## 🔄 每日循環流程 (The Daily Loop)

### Step 1: Cloud Sensing (雲端感知)
*自動執行，無需人工干預*

*   **觸發時間**: 每日 06:00 AM & 20:00 PM (HKT)。
*   **執行者**: GitHub Actions (`daily_brief.yml`)。
*   **動作**:
    1.  `scout_hunter.py`: 掃描宏觀主題 (Macro Themes) 的機會。
    2.  `scout_shield.py`: 掃描持倉 (Portfolio) 的風險。
    3.  **Data Commit**: 自動將 JSON 結果 push 到 **Private Data Repo** 的 `Incoming/` 資料夾。

---

### Step 2: Local Sync (本地同步)
*Agent 介入點 - 開始工作前必須做*

未來 Agent 在開始分析前，必須確保本地擁有最新的雲端情報。

**指令**:
```bash
cd ~/kazuha/investsense/data
git pull origin main
```
*   **檢查點**: 確認 `data/Incoming/` 目錄下是否有今日日期的 `hunter_*.json` 或 `shield_*.json`。

---

### Step 3: Local Brain Reasoning (本地推理)
*Agent 核心任務*

利用本地算力 (AI Agent) 讀取 raw data 並生成 Alpha 報告。

1.  **讀取數據**: 讀取 `data/Incoming/` 所有 JSON 及 `data/portfolio.yml`。
2.  **執行推理**: (目前由 Agent 協助，未來可運行 `src/brain_reasoning.py`)
    *   識別 **二階效應 (Second-order effects)**。
    *   計算 **Alpha Confidence Score**。
    *   識別 **Risk Alerts**。
3.  **生成報告**:
    *   格式：Markdown。
    *   路徑：`data/Reports/daily_alpha_YYYYMMDD.md`。
    *   內容結構：需包含 `Key Alpha Opportunities` (獵人) 與 `Portfolio Risk Alerts` (護盾)。

---

### Step 4: Publish & Archive (發布與歸檔)
*完成任務後的動作*

將生成好的報告推送到 Private Cloud，以便手機端查看或歸檔。

**指令**:
```bash
cd ~/kazuha/investsense/data
git add Reports/daily_alpha_*.md
git commit -m "Add Daily Alpha Level 2 Report"
git push origin main
```

---

## 🛠 Troubleshooting (常見問題)

### 🔴 GitHub Action Error: "Input required: token"
*   **原因**: Engine Repo 缺少存取 Private Data Repo 的權限。
*   **解法**: 生成具有 `repo` 權限的 PAT，並在 Engine Repo Settings -> Secrets 加入 `PAT_TOKEN`。

### 🔴 GitHub Action Error: "couldn't find remote ref refs/heads/main"
*   **原因**: Private Data Repo 是空的，或者分支名不是 `main`。
*   **解法**: 確保本地 `data/` 目錄已初始化 git 並 push 了 initial commit。

### 🟡 如何手動觸發雲端掃描？
1.  進入 `investsense-engine` GitHub 頁面。
2.  點擊 **Actions** -> **Daily Sense Briefing**。
3.  點擊右側 **Run workflow**。

---

## 🤖 給未來 Agent 的指令 (Prompt for Future Agent)

> "Agent，請執行 Kazuha Loop。首先 `cd data && git pull` 確保拿到最新情報，然後讀取 `Incoming` 裡面的 JSON，幫我分析今日的 Alpha 機會與風險，寫入 `Reports/`，最後 push 上去。"

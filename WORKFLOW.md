# 🔄 Kazuha Invest 2.0 Operational Workflow (Vibe-Hunter 2.2 - Closed Loop)

本文件詳述 Kazuha Invest 2.0 的 **「進化型搜尋閉環 (Scout-Reasoning Loop)」** 完整操作流程。這套系統實現了從固定關鍵字到 **AI 指令驅動** 的動態情報獵殺轉型。

---

## 🏗️ 系統閉環概覽 (The Evolution Loop)

1.  **Scout (Cloud)**: GitHub Actions 定時執行分佈式偵測，讀取固定 `themes.yml` 與 AI 生成的 `active_missions.yml`。
2.  **Consolidate**: 腳本自動進行「語義+時間」雙重去重，保留最權威、最新的資訊。
3.  **Context**: `brain_reasoning.py` 生成分析上下文，隨即 **自動歸檔 (Archive)** 原始信號以保持環境純淨。
4.  **Reasoning (Manual/Agent)**: 執行 `REASONING_FLOW.md` (V7)，手動/半自動產出決策報告。
5.  **Evolve**: 分析過程中發現的漏洞轉化為 **New Missions** 寫入 `active_missions.yml`。
6.  **Sync**: Git Push 更新，將新任務「餵返」給 GitHub Action，啟動下一輪精準獵殺。

---

## � 每日自動化排程 (GitHub Actions)

*   **時間**: 每日 00:13, 08:03, 21:48 (GMT) —— 覆蓋全球市場開盤前夕。
*   **動作**:
    1.  **`scout_hunter.py`**: 執行 **Static Themes** (長期關注) + **Active Missions** (AI 追蹤任務)。
    2.  **`scout_shield.py`**: 監控核心持倉及任務中新發現的競爭對手。
    3.  **`scout_gov.py`**: 追蹤 >$500k 的政府合同，支持任務關鍵字擴展。
    4.  **`scout_social.py`**: Reddit 動態話題追蹤。
    5.  **`scout_dedup.py`**: 語義合併及權威度排序。
    6.  **`brain_reasoning.py`**: 準備手動分析 Context 並 **Archive Incoming Data**。

---

## 🧠 手動操盤 SOP (Manual Analysis Protocol)

當你收到 Telegram 搜查完成通知後：

### 1. 讀取與推理 (Execute V7 Flow)
- 打開最新的 `data/Reports/YYYYMMDD/Context_Input.md`。
- 嚴格遵循 `REASONING_FLOW.md` 的專家委員會、多重宇宙、紅藍對抗邏輯。

### 2. 獵補缺口 (Capture Data Gaps)
- 在分析中標記 `[EVIDENCE_GAP]`。
- **關鍵動作**：在報告末尾生成 YAML 代碼塊，更新 `data/active_missions.yml`。

### 3. 持久化與閉環 (Closing the Loop)
- 保存報告至 `data/Reports/YYYYMMDD/Daily_Alpha_Briefing.md`。
- 執行以下 Git 指令完成閉環：
```bash
git add data/active_missions.yml data/Reports/
git commit -m "Manual Analysis: missions updated [skip ci]"
git push
```

---

## 🛠️ 配置與維護 (Maintenance)

### 關鍵檔案說明：
- **`src/config.py`**: 調整 `MIN_CONTRACT_VALUE` 門檻 (默認 $500k) 或去重閾值。
- **`data/themes.yml`**: 管理長期宏觀投資主題。
- **`data/active_missions.yml`**: AI 驅動的臨時任務區（24-48小時自動到期）。
- **`REASONING_FLOW.md`**: 推理解析的最高行動綱領。

### 權限提醒：
- 確保 GitHub Action 已開啟 `permissions: contents: write` 權限，否則閉環將失效。

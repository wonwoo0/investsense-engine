# Kazuha Invest 2.0 - Manual Pilot Reasoning Flow (V7)

## ⚠️ 執行前置 (Phase 0: Setup)
在開始分析前，請確保已讀取由 `brain_reasoning.py` 生成的最新上下文文件：
- **路徑**: `/Users/roy/kazuha/investsense/data/Reports/[YYYYMMDD]/Context_Input.md`

---

## 🏗️ 核心推理 (Core Reasoning)

### 第一階段：專家審核 (Expert Committee)
- 調用 `/Users/roy/kazuha/investsense/prompts/experts/` 下的所有角色。
- **目標**：識別證據缺口 `[EVIDENCE_GAP]`（例如：提及某項技術但無提及良率）。

### 第二階段：場景推演 (Multiverse)
- 調用 `/Users/roy/kazuha/investsense/prompts/reasoning/multiverse.md`。
- **目標**：定義領先觀測指標 `[SIGNPOST]`（例如：Tesla 2/14 嘅訂閱轉化率）。

### 第三階段：紅藍軍對抗 (The Arena)
- 調用 `/Users/roy/kazuha/investsense/prompts/reasoning/red_team.md` 與 `blue_team.md`。
- **目標**：找出「致命殺招」與「反脆弱護城河」。

### 第四階段：合成與打分 (Synthesis & Rubric)
- 調用 `/Users/roy/kazuha/investsense/prompts/reasoning/editor.md` 與 `/Users/roy/kazuha/investsense/prompts/scoring_rubric.md`。

---

## 💾 產出與部署 (Phase 5: Output & Deployment)

分析完成後，必須執行以下操作以完成閉環：

### 1. 寫入報告
將最終分析報告保存到：
`/Users/roy/kazuha/investsense/data/Reports/[YYYYMMDD]/Daily_Alpha_Briefing.md`

### 2. 更新搜尋任務 (Scout Mission Loop) 🚀
根據分析中發現的 `[EVIDENCE_GAP]` 或 `[SIGNPOST]`，更新以下檔案。**不要覆蓋現有任務，除非已過期。**
- **檔案路徑**: `/Users/roy/kazuha/investsense/data/active_missions.yml`
- **更新邏輯**:
```yaml
active_missions:
  - theme: "[分析中發現的新趨勢/缺口]"
    keywords: ["關鍵字A", "關鍵字B"]
    reason: "填補 [EVIDENCE_GAP] / 觀測 [SIGNPOST]"
    priority: "high"
    depth: 15
    created_at: "[YYYY-MM-DD]"
    expires_at: "[YYYY-MM-DD + 48h]"
```

### 3. Git 同步指令 (Git Sync)
如果你喺本地執行，完成後執行以下指令以觸發 GitHub Action 嘅下一次 Scout 循環：
```bash
cd /Users/roy/kazuha/investsense/data
git add .
git commit -m "Manual Alpha: [主題] & missions updated"
git push
```

---

## 🚀 執行準則 (Guidelines)
- **ANTICIPATE**: 如果新聞提到 A 公司合作，下一步指令要搜「B 公司（競爭對手）嘅反應」。
- **ACTION-FIRST**: 報告頭三行必須有明確的「買/賣/避」建議。
- **DATA PURITY**: 優先信任 `[Hard Data]`，貶低 `[Hype]`。

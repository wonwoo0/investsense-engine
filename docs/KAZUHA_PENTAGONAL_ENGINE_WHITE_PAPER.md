# 📄 Kazuha Pentagonal Reasoning Engine (PRE): The Local Brain Upgrade Whitepaper

**Version:** 1.0 (Final)
**Date:** Jan 2026
**Status:** Architecture Finalized
**Core Philosophy:** Adversarial (對抗), Probabilistic (概率), Iterative (迭代)

---

## 1. 核心願景 (The Vision)

**Kazuha Pentagonal Reasoning Engine (PRE)** 是一個運行在 **本地 (Local Host)** 的數位投資決策委員會。

我們不再依賴單一的 LLM 進行線性總結，而是利用本地環境的 **無限算力 (Code Plan)**，構建一個由多個 Agent 組成的「思維工廠」。這個工廠通過 **「分歧 (Divergence)」** 與 **「收斂 (Convergence)」** 的反覆迭代，將普通的市場資訊提煉為高信心的 **Alpha Conviction**。

**目標**：不追求預測準確，追求邏輯的 **「極致密度 (Logic Density)」** 與 **「抗脆弱性 (Antifragility)」**。

---

## 2. 五角星綜合推理架構 (The Pentagonal Architecture)

系統由五個獨立模組組成，並由一個「銜尾蛇迴路 (Ouroboros Loop)」包裹。

### 階段一：專家會診 (The Committee)
*   **角色**：打破思維盲區，引入多元視角。
*   **執行模式**：並行 (Parallel) 執行，互不干擾。
*   **Agent 陣容**：
    1.  **Macro Strategist (宏觀)**：分析利率、地緣政治、資金流向。
    2.  **Tech Specialist (技術)**：評估技術護城河、代碼質量、專利壁壘。
    3.  **Financial Analyst (財務)**：關注估值倍數、現金流健康度、商業模式。
*   **輸出**：`Expert_Opinions.json` (三份獨立觀點)。

### 階段二：時空分叉 (The Multiverse)
*   **角色**：拒絕線性預測，擁抱概率思維。
*   **執行模式**：合成專家意見，推演三條未來的世界線。
*   **劇本定義**：
    1.  **Bull Case (樂觀)**：所有催化劑 (Catalysts) 完美兌現的劇本。
    2.  **Bear Case (悲觀)**：風險全面爆發、邏輯被證偽的壓力測試劇本。
    3.  **Base Case (基準)**：最符合當前數據的中性路徑。
*   **輸出**：`Scenarios.md` (包含三個劇本的詳細描述)。

### 階段三：極限生存辯論 (The Arena)
*   **角色**：去偽存真，針對 **Bull Case** 進行極限施壓。
*   **執行模式**：**單次平行對抗 (Parallel Stance Generation)**。
    *   *註：採納用戶建議，不進行多輪對話，而是單次生成高品質的「控訴狀」與「辯護詞」，效率最高。*
*   **對陣雙方**：
    *   **🔴 Red Team (紅軍)**：空頭殺手。任務是尋找 Bull Case 中的邏輯斷層、監管死角、技術騙局。
    *   **🔵 Blue Team (藍軍)**：多頭衛士。任務是針對紅軍的潛在指控進行數據反擊與護城河重申。
*   **輸出**：`Debate_Log.md` (紅藍雙方的觀點對照表)。

### 階段四：煉金 (The Synthesis)
*   **角色**：主編 (Editor-in-Chief)。
*   **執行模式**：閱讀前三個階段的所有產出（專家觀點、平行宇宙、辯論實錄）。
*   **任務**：
    *   判斷 Bull Case 是否在紅軍的攻擊下倖存。
    *   若倖存，信心分數 (Confidence Score) 幾分？
    *   合成最終的 **Daily Alpha Report**。
*   **輸出**：`Draft_Report.md`。

### 階段五：銜尾蛇迴路 (The Ouroboros Loop)
*   **角色**：質量守門員 (Gatekeeper)。
*   **機制**：
    *   主編對自己的草稿進行評分 (0-100)。
    *   **< 90 分**：觸發 **Self-Correction**。帶著「自我批評 (Critique)」將草稿打回 **階段四** 進行重寫（Refinement）。
    *   **>= 90 分**：通過，輸出最終報告。
    *   **Hard Stop**：若循環 3 次仍未達標，強制輸出並標註「低信心」。

---

## 3. 數據與檔案管理 (Data & Artifacts)

### 3.1 提示詞管理 (Prompt Management)
所有 System Prompts 將從代碼中剝離，存放在 `prompts/` 目錄下，方便隨時用自然語言微調。

*   `prompts/experts/macro.md`
*   `prompts/experts/tech.md`
*   `prompts/experts/financial.md`
*   `prompts/reasoning/multiverse.md`
*   `prompts/reasoning/red_team.md`
*   `prompts/reasoning/blue_team.md`
*   `prompts/reasoning/editor.md` (含評分標準)

### 3.2 中間產物留存 (Artifact Preservation)
我們不僅保留最終結果，還保留思考過程。所有中間產物將存檔，形成「思維黑盒」。

*   **目錄結構**：
    ```
    data/
    ├── Reports/
    │   ├── 20260115/
    │   │   ├── Expert_Opinions.json   # 階段一產物
    │   │   ├── Scenarios.md           # 階段二產物
    │   │   ├── Debate_Log.md          # 階段三產物
    │   │   └── Daily_Alpha_Final.md   # 最終報告
    ```

---

## 4. 技術實作策略 (Implementation Strategy)

### 4.1 本地優先 (Local First)
*   **運算環境**：所有邏輯調度 (`brain_reasoning.py`) 在本地機器運行。
*   **模型調用**：通過 `src.utils.model_factory` 接口調用模型。
    *   *配置靈活性*：支持在 `config.py` 中切換模型源 (OpenRouter / Local Ollama)，但核心邏輯代碼保持不變。

### 4.2 數據流 (Data Flow)
1.  **Input**: 用戶提供的優化後搜索結果 (JSON)。
2.  **Orchestrator**: `brain_reasoning.py` 讀取 JSON -> 加載 `prompts/*.md` -> 順序調用各階段 Agent。
3.  **Loop**: 內置 `while` 循環處理 Ouroboros 邏輯。
4.  **Output**: 生成 Markdown 報告並保存中間文件。

---

## 5. 下一步行動 (Next Steps)

1.  **等待數據**：用戶提供「搜索完優化後的結果」作為測試數據。
2.  **建立 Prompt 庫**：根據白皮書創建 `prompts/` 目錄及所有 `.md` 文件。
3.  **編寫核心代碼**：開發 `brain_reasoning.py` 實現上述五角星邏輯。

---
**本白皮書已定稿，等待用戶提供測試數據後即可開始施工。**

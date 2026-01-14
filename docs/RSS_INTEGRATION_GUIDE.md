# 📡 RSS Integration Guide (Phase 2 Expansion)

**目標**：將 Kazuha Invest 2.0 從「主動狩獵 (Keyword Search)」升級至「被動感知 (RSS Feeds)」，捕捉未知二階機會。

---

## 🧠 核心策略：雷達站架構 (Radar Architecture)

### 當前系統 (Phase 1)
```
[DuckDuckGo Search] → [Incoming/*.json] → [Brain Analysis]
   ↑ 主動：只找你知道的關鍵字
```

### 升級後系統 (Phase 2)
```
[RSS Feeds]     ──┐
[DDG Hunter]    ──┼─→ [Rule Filter] → [Semantic Dedup] → data/Incoming/consolidated_YYYYMMDD.json
[DDG Shield]    ──┘                                              ↓
                                                        [Brain Reasoning] → Reports/
```
**數據流向說明**：
1. **原始數據** (`data/Incoming/`):
   - `rss_results_*.json` — RSS Feed 抓取結果
   - `hunter_results_*.json` — 宏觀主題搜尋結果
   - `shield_results_*.json` — 持倉風險監測結果

2. **合併去重** (`src/scout_dedup.py`):
   - 讀取上述所有 `*_results_*.json`
   - 執行語義去重 (Embedding Similarity)
   - 輸出 → `data/Incoming/consolidated_YYYYMMDD.json` ⭐

3. **本地推理** (`src/brain_reasoning.py`):
   - **只讀取** `consolidated_*.json`（已去重的高質量數據）
   - 生成 Daily Alpha 報告

---

## 📋 實施步驟 (Implementation Plan)

### Step 1: 建立 RSS 來源清單

建立檔案：`data/sources.yml`

```yaml
# Tier 1: 低噪音，高相關（第一週先加呢啲）
tier1:
  - name: SpaceNews
    url: https://spacenews.com/feed/
    category: Space Tech
    portfolio_relevance: [RKLB]
    priority: high

  - name: World Nuclear News
    url: https://world-nuclear-news.org/RSS
    category: Advanced Nuclear
    portfolio_relevance: []
    priority: high
    
  - name: Electrek
    url: https://electrek.co/feed/
    category: Automotive/EV
    portfolio_relevance: [TSLA]
    priority: high
    
  - name: Ars Technica Science
    url: https://feeds.arstechnica.com/arstechnica/science
    category: Advanced Nuclear, Space
    portfolio_relevance: []
    priority: medium

# Tier 2: 中噪音（第二週測試）
tier2:
  - name: SemiEngineering
    url: https://semiengineering.com/feed/
    category: Semiconductors, Photonics
    portfolio_relevance: [POET]
    priority: medium
    
  - name: Hacker News (Filtered)
    url: https://hnrss.org/newest?points=100
    category: Tech Breakthrough
    portfolio_relevance: []
    priority: low
```

---

### Step 2: 開發 RSS Scout (`src/scout_feed.py`)

#### 架構邏輯
```python
# Pseudo-code
def scout_feed():
    # 1. Load RSS sources from data/sources.yml
    sources = load_yaml("data/sources.yml")
    
    # 2. Fetch RSS feeds
    all_entries = []
    for source in sources['tier1']:  # 先只跑 tier1
        entries = feedparser.parse(source['url']).entries
        all_entries.extend(entries)
    
    # 3. Rule-based Pre-filter (第一層過濾)
    filtered = [e for e in all_entries if quick_filter(e)]
    
    # 3.1 Health Check (健康檢查)
    # Log if a source returns 0 entries for multiple days
    
    # 4. AI Semantic Filter (第二層過濾) - Optional
    # final = ai_relevance_filter(filtered)
    
    # 5. Save to Incoming/
    save_json(filtered, "data/Incoming/rss_results_{timestamp}.json")
```

#### 第一層：Rule-based Filter (免費，快速)

```python
def quick_filter(entry):
    """
    快速過濾規則，減少 AI 處理量
    """
    title = entry.get('title', '').lower()
    summary = entry.get('summary', '').lower() # 掃描摘要以防標題黨
    url = entry.get('link', '')
    content = title + " " + summary
    
    # 排除關鍵字 (Negative Keywords) - 減少噪音
    NEGATIVE_KEYWORDS = ['tutorial', 'how to', 'review', 'podcast', 'video only', 'giveaway']
    if any(nw in content for nw in NEGATIVE_KEYWORDS):
        return False

    # 白名單：可信來源直接通過
    TRUSTED_DOMAINS = ['spacenews.com', 'eetimes.com', 'semiengineering.com', 'world-nuclear-news.org']
    if any(domain in url for domain in TRUSTED_DOMAINS):
        return True
    
    # 持倉關鍵字：如果提到你的股票
    PORTFOLIO_KEYWORDS = ['rklb', 'rocket lab', 'tesla', 'tsla', 
                          'poet', 'photonics', 'ondas']
    if any(kw in content for kw in PORTFOLIO_KEYWORDS):
        return True
    
    # 財經信號：IPO、併購、新產品
    FINANCIAL_SIGNALS = ['ipo', 'acquired', 'acquisition', 'partnership', 
                         'raises $', 'closes $', 'announces']
    if any(signal in content for signal in FINANCIAL_SIGNALS):
        return True
    
    # 技術突破信號
    TECH_SIGNALS = ['breakthrough', 'first ever', 'record', 'milestone']
    if any(signal in content for signal in TECH_SIGNALS):
        return True
    
    # 其他全部過濾掉
    return False
```

**預期效果**：500條 RSS → 過濾後剩 **50-80 條**。

---

### Step 3: 語義去重 (Semantic Deduplication)

#### 為什麼需要？
- DuckDuckGo 搵到：*"Rocket Lab Launches Satellite for NASA"* (Source: Reuters)
- RSS 抓到：*"RKLB Mission Success for NASA Contract"* (Source: SpaceNews)
- **問題**：兩篇講同一件事，但標題唔同。

#### 解決方案：Vector Embedding + Cosine Similarity
- **跨時間視窗 (Time Window)**：建立 `history_hashes.json` 記錄過去 48 小時已處理的標題，防止跨時段重複報告。

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_dedup(articles):
    """
    使用 Gemini Embedding API 或 SentenceTransformer 本地模型
    """
    # 1. 將每篇文章的標題+摘要轉成 Vector
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 本地免費模型
    embeddings = [model.encode(a['title'] + ' ' + a.get('summary', '')) 
                  for a in articles]
    
    # 2. 計算相似度矩陣
    similarity_matrix = cosine_similarity(embeddings)
    
    # 3. 去重邏輯
    to_remove = set()
    for i in range(len(articles)):
        for j in range(i+1, len(articles)):
            if similarity_matrix[i][j] > 0.85:  # 相似度閾值
                # 保留來源權威性高的
                if is_more_authoritative(articles[i], articles[j]):
                    to_remove.add(j)
                else:
                    to_remove.add(i)
    
    # 4. 移除重複項
    return [a for idx, a in enumerate(articles) if idx not in to_remove]

def is_more_authoritative(article1, article2):
    """
    定義來源權威性排序
    """
    AUTHORITY_RANK = {
        'reuters.com': 10,
        'bloomberg.com': 10,
        'spacenews.com': 9,
        'eetimes.com': 9,
        'techcrunch.com': 7,
        'default': 5
    }
    score1 = max([AUTHORITY_RANK.get(d, 5) for d in AUTHORITY_RANK if d in article1['url']])
    score2 = max([AUTHORITY_RANK.get(d, 5) for d in AUTHORITY_RANK if d in article2['url']])
    return score1 > score2
```

---

### Step 4: 更新 GitHub Actions Workflow

修改 `.github/workflows/daily_brief.yml`，加入 RSS Scout：

```yaml
- name: Run RSS Scout (Passive Sensing)
  run: uv run python src/scout_feed.py
  env:
    PYTHONUNBUFFERED: 1

- name: Run Shield Scout (Defense)
  run: uv run python src/scout_shield.py

- name: Run Hunter Scout (Offense)
  run: uv run python src/scout_hunter.py
```

**執行順序**：RSS Feed → Shield → Hunter → Dedup → Push Data

---

## 🎯 分階段測試計劃

### Week 1: Tier 1 Only (低風險)
- 只開 **SpaceNews + Electrek + Ars Technica**
- 驗證：Rule Filter 能否將噪音控制在 50 條以內？
- 驗證：語義去重是否有效？

### Week 2: 加入中噪音源
- 加 **SemiEngineering**（針對 POET）
- 觀察：AI Filter 是否需要介入？

### Week 3: 高噪音挑戰
- 加 **Hacker News (Filtered)**
- 測試：白名單 domain 策略是否有效？

### Week 4: 全面評估
- 對比有無 RSS 的 Alpha 發現率
- 決定是否永久保留

---

## 🔧 技術依賴 (Dependencies)

### Python 套件
```bash
uv pip install feedparser sentence-transformers scikit-learn
```

### 可選：使用 Gemini Embedding API (免費額度大)
```python
import google.generativeai as genai

def get_embedding(text):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result['embedding']
```

---

## 📊 預期成本與效益

### 成本
- **計算成本**：Rule Filter (免費) + Local Embedding Model (免費)
- **API 成本**：如果用 Gemini Embedding API，每日 500 次調用 ≈ $0 (在免費額度內)

### 效益
- **發現率提升**：預計能捕捉到 **15-20% 的「未知機會」**（即你原本不知道要搜的關鍵字）
- **時間套利**：RSS 通常比 Google News 快 2-6 小時（因為 RSS 是直接推送）

---

## ⚠️ 風險與緩解

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| **噪音爆炸** | 報告太長，難以閱讀 | 嚴格執行 Rule Filter，初期只開 Tier 1 |
| **重複過多** | 浪費 AI 分析時間 | 實施語義去重（必須） |
| **誤報過濾** | 漏掉重要新聞 | 定期 Review 被過濾掉的內容 (Logging) |
| **RSS 源失效** | 數據斷流 | 定期檢查 RSS 是否仍然有效 |

---

## 📝 給未來 Agent 的指令

> "Agent，請實施 RSS Integration Phase 2。首先建立 `data/sources.yml` 並只加入 Tier 1 來源，然後開發 `src/scout_feed.py` 實作 Rule Filter 與語義去重。測試一週後再決定是否擴展至 Tier 2。記住：寧可漏過一條新聞，也不要被噪音淹沒。"

---

## 🔗 參考資源

- **RSS Best Practices**: https://www.rssboard.org/rss-specification
- **Sentence Transformers**: https://www.sbert.net/
- **Gemini Embedding API**: https://ai.google.dev/gemini-api/docs/embeddings

# PRD: RSS Passive Sensing Integration (Radar Architecture)

## TL;DR

- Implementing a passive news sensing layer using RSS feeds to supplement keyword-based active hunting.

## Goal

- Transform the system from a "Sniper" (active keywords only) to a "Radar" (passive industry sensing).
- Successfully capture second-order investment opportunities from high-signal RSS sources.
- Implement a noise-filtering and semantic deduplication pipeline to maintain report quality.

## Constraints

- **Source Quality**: Priority on Tier 1 (SpaceNews, World Nuclear News, Electrek, Ars Technica).
- **Noise Control**: Must implement Rule-based Pre-filtering to reduce LLM/Analysis load.
- **Data Integrity**: Must implement Semantic Deduplication using Vector Embeddings to prevent redundant entries.
- **Privacy**: Adhere to existing Engine/Data repository separation.

## Acceptance Criteria

- [x] `data/sources.yml` created with tiered RSS sources.
- [x] `src/scout_feed.py` implemented with RSS fetching logic.
- [x] Rule-based filter correctly handles Negative Keywords and Trusted Domains.
- [x] Semantic deduplication successfully identifies and merges similar news from different sources (RSS vs DDG).
- [x] `history_hashes.json` prevents duplicate reporting across a 48-hour window.
- [x] GitHub Actions workflow updated to include RSS Sensing in the daily pipeline.

## Verification

- **Manual Check**: Run `src/scout_feed.py` and verify `data/Incoming/rss_results_*.json` contains high-signal, non-redundant news. (Verified locally: Found 74 signals).
- **Health Check**: Verify workflow logs for any broken RSS links.
- **Quality Audit**: Review `Daily_Alpha.md` to see if RSS-sourced news leads to unique insights not captured by keyword search. (Pending first cloud run).

## Notes

- **Time Arbitrage**: RSS feeds often provide updates 2-6 hours faster than standard search indexing.
- **Authoritative Ranking**: When deduplicating, prioritize Reuters/Bloomberg/Vertical leaders over general aggregation sites.

## Progress

### Phase 2: RSS Planning - 2026-01-14

- **Summary**: Drafted the RSS Integration Guide and established the Radar Architecture logic.
- **Decisions**: 
    - Use `feedparser` for RSS retrieval.
    - Implement a two-layer filter (Rule-based then Semantic).
    - Use `sentence-transformers` (local) or Gemini Embedding API for deduplication.
    - Added "Negative Keywords" and "Time Window" constraints based on refinement discussion.
- **Assumptions**: 
    - GitHub Actions environment can handle the local embedding model or has API access for embeddings.
- **Risks**: 
    - RSS noise could overwhelm the analysis layer if filtering is too loose.
- **Status**: Planning Complete.

### Phase 2: Implementation - 2026-01-14

- **Summary**: Implemented RSS fetching, rule-based filtering, and semantic deduplication.
- **Decisions**: 
    - Implemented `scout_feed.py` using `requests` with custom User-Agent to bypass 403s.
    - Implemented `scout_dedup.py` using `all-MiniLM-L6-v2` for efficient local semantic analysis.
    - Consolidated all incoming signals into a single file post-deduplication to simplify analysis.
- **Assumptions**: 
    - `uv` or `pip` will install large dependencies in GitHub Actions without timeout.
- **Risks**: 
    - `sentence-transformers` memory usage in GitHub Actions runner (Standard runner has 7GB RAM, should be fine).
- **Status**: Implementation Complete.
- **Next**: Monitor first automated run and refine filtering if needed.

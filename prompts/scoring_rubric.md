# Kazuha Invest 2.0 - Scoring Rubric (V3 - Professional Quant & Execution)

## Purpose
This document defines the quantitative framework for AI-generated scores in the Daily Alpha Briefing. It ensures consistency, accounts for execution reality, and provides a structured protocol for `brain_review.py` to recalibrate the system's weights based on backtesting results.

---

## 1. Alpha Confidence Score (0-100)
Used to rank opportunities. High score = High conviction + High asymmetry.

### Core Weighted Factors:
| Factor | Weight | High Score Criteria | Low Score Criteria |
| :--- | :--- | :--- | :--- |
| **Evidence Purity** | 25% | Verified Hard Data (10-K, Terminals). | Narrative, Hype, or Rumors. |
| **Risk/Reward Asymmetry** | 20% | > 4:1 Upside/Downside ratio. | 1:1 or unknown asymmetry. |
| **Directness of Link** | 15% | Direct impact on terminal valuation. | Vague sector "tailwinds." |
| **Crowdedness Discount** | 15% | Non-consensus / Early discovery. | Front-page news / Crowded trade. |
| **Time Arbitrage** | 15% | Market is mispricing a catalyst. | Catalyst is fully priced-in. |
| **Source Integrity** | 10% | Top-tier reporting / Official data. | Social media hype / Unverified blogs. |

**Threshold for Telegram Alert: >95**

---

## 2. Risk Score (0-100)
Used for Portfolio Alerts. High score = Imminent systemic or fundamental threat.

### Core Weighted Factors:
| Factor | Weight | High Score Criteria | Low Score Criteria |
| :--- | :--- | :--- | :--- |
| **Severity & Irreversibility** | 30% | "Game Over" events (Fraud, Defaults). | Temporary setbacks. |
| **Liquidity & Execution** | 20% | Wide spreads / Low ADV / Exit risk. | High liquidity / Narrow spreads. |
| **Systemic Contagion** | 15% | Ripple effect across sectors/macro. | Isolated incident. |
| **Imminence** | 15% | Materializes in < 5 trading days. | Vague long-term threat. |
| **Cluster Exposure** | 10% | Correlated with existing heavy holdings. | Diversified / Uncorrelated. |
| **Source Integrity** | 10% | Documented evidence / Fact-checking. | Rumor / Sentiment-driven. |

**Threshold for Telegram Alert: >90**

---

## 3. Adjustment Protocol (for `brain_review.py`)
This section maps backtesting failure modes to specific rubric modifications.

### Failure Mode: "False Positives" (High Confidence, Poor Performance)
- **If accuracy @ Confidence > 90 is < 50%**: Decrease **Source Integrity** weight and increase **Evidence Purity** requirements.
- **If performance lags after 30 days**: Increase **Time Arbitrage** penalty (market was already efficient).
- **If "Hype" winners fail**: Apply a mandatory -20 point penalty for any score purely based on **Narrative**.

### Failure Mode: "False Negatives" (Low Confidence, High Performance)
- **If missed opportunities were "Non-Consensus"**: Increase the weight of **Crowdedness Discount** (reward early hunting).
- **If performance was macro-driven**: Adjust **Macro Strategist** prompt weights within the synthesis logic.

### Failure Mode: "Risk Misses" (Low Risk Score, Significant Drawdown)
- **If drawdowns were liquidity-driven**: Increase the weight of **Liquidity & Execution** risk factor.
- **If losses were correlated**: Increase **Cluster Exposure** penalty for correlated assets.

---
*(This rubric is a living document. Initially, brain_review.py will propose changes in the monthly report for manual approval.)*

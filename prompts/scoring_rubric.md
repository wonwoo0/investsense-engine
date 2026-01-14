# Kazuha Invest 2.0 - Scoring Rubric

## Purpose
This document provides the Sisyphus AI with a rubric for generating Confidence scores for Alpha Opportunities and Risk Scores for Portfolio Alerts within the Daily Alpha Briefing. It also serves as a template for `brain_review.py` to propose adjustments based on monthly backtesting.

## General Scoring Principles

*   **Confidence (Alpha Opportunity)**:
    *   **Scale**: 0-100. Higher score indicates stronger conviction.
    *   **Factors**:
        *   **Strength of Signal**: How clear and impactful is the news/event? (e.g., policy change > general trend).
        *   **Directness of Link**: How directly does the news link to the identified Alpha?
        *   **Portfolio Relevance**: How significant is the opportunity for the current portfolio or defined macro themes?
        *   **Uniqueness/Arbitrage**: How early is this signal? Is it widely known? (Time Arbitrage).
        *   **Source Credibility**: Reliability of the news source.
    *   **Threshold for Alert**: >95 (for Telegram notification).

*   **Risk Score (Portfolio Alert)**:
    *   **Scale**: 0-100. Higher score indicates greater perceived risk.
    *   **Factors**:
        *   **Severity of Event**: How negative or impactful is the event? (e.g., fraud > minor delay).
        *   **Directness of Impact**: How directly does it impact the specific portfolio asset?
        *   **Magnitude of Impact**: Potential financial or reputational damage.
        *   **Imminence**: How quickly could the risk materialize?
        *   **Contagion/Systemic Risk**: Could it spread to other assets or the broader market?
        *   **Source Credibility**: Reliability of the news source.
    *   **Threshold for Alert**: >90 (for Telegram notification).

## Adjustment Guidelines (for `brain_review.py`)

Based on monthly backtesting results from `brain_review.py`, adjustments to Sisyphus's internal interpretation of these factors may be suggested here.

*   **If Alpha predictions with Confidence > 95 consistently underperform:**
    *   Suggest increasing the "Strength of Signal" or "Directness of Link" factor weight.
    *   Suggest being more conservative on "Uniqueness/Arbitrage" assessment.
*   **If Alpha predictions with Confidence < 70 consistently outperform:**
    *   Suggest being more aggressive on "Portfolio Relevance" or "Source Credibility" factor weight.
*   **If Risk predictions with Risk Score > 90 consistently fail to materialize or are overblown:**
    *   Suggest increasing "Severity of Event" or "Magnitude of Impact" factor weight.
    *   Suggest being more conservative on "Imminence" or "Contagion" assessment.
*   **If significant risks are missed (false negatives):**
    *   Suggest broadening the interpretation of "Risk Type" or lowering the bar for "Directness of Impact".

(This section is a placeholder for future automated adjustments. Initially, `brain_review.py` will log suggestions for manual review.)

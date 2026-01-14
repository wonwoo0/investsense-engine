import os
import json
import yaml
from datetime import datetime
import asyncio
import re
from src.notifier import send_telegram_message

# Configuration
INCOMING_DIR = "data/Incoming"
PORTFOLIO_PATH = "data/portfolio.yml"
REPORTS_DIR = "data/Reports"

def load_data(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                    all_data.extend(data)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {filepath}")
    return all_data

def load_portfolio(filepath):
    if not os.path.exists(filepath):
        return {"portfolio": []}
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

async def main():
    # 1. Load all *.json from data/Incoming/
    incoming_data = load_data(INCOMING_DIR)
    
    # 2. Load data/portfolio.yml
    portfolio_data = load_portfolio(PORTFOLIO_PATH)

    # 3. Formulate a prompt for Sisyphus (this AI)
    #    including the JSON data, portfolio, and the desired report structure.
    
    prompt_template = """
You are Kazuha Invest 2.0, an AI tasked with generating a daily Alpha Briefing based on incoming market intelligence.
Your goal is to perform "second-order thinking" and identify potential opportunities (Alpha) and risks for the portfolio.

Here is the current portfolio for context:
{portfolio_context}

Here is the raw market intelligence data collected today:
{incoming_intelligence}

Based on this information, please generate a "Daily Alpha Briefing" in Markdown format, following this exact structure:

```markdown
# 🚀 Daily Alpha Briefing - YYYY-MM-DD

## 💡 Key Alpha Opportunities (獵人發現)

### [宏觀主題 1 標題]
- **概述**: [與此主題相關的新聞/信號簡要總結。]
- **信號**:
    - [信號 1 - URL, 標題, 來源]
    - [信號 2 - URL, 標題, 來源]
- **二階思考**: [我對潛在影響、相關股票或未來發展的分析。]
- **信心 (Confidence)**: [0-100 score]

### [宏觀主題 2 標題]
- ... (類似結構)

## ⚠️ Portfolio Risk Alerts (護盾監測)

### [資產代碼 1] - [資產名稱]
- **風險類型**: [例如：訴訟、調查、負面新聞]
- **概述**: [風險新聞的簡要總結。]
- **信號**:
    - [風險信號 1 - URL, 標題, 來源]
- **影響評估**: [我對資產、其行業或更廣泛市場潛在影響的分析。]
- **風險評分 (Risk Score)**: [0-100 score]

### [資產代碼 2] - [資產名稱]
- ... (類似結構)

## 📊 總體情緒與結論

- **概述**: [從新聞中得出整體市場情緒的簡要總結。]
- **可行洞察**: [任何清晰、簡潔的可行洞察或值得進一步調查的領域。]
```

Please replace YYYY-MM-DD with today's date. For each opportunity and risk, provide a **信心 (Confidence)** score (0-100) and **風險評分 (Risk Score)** (0-100) respectively. Fill in all sections based on the provided data, providing concrete examples and insightful analysis. If no opportunities or risks are found for a category, state that clearly (e.g., "無發現潛在風險。").Focus on high-conviction insights and prioritize information relevant to the provided portfolio and macro themes.
"""
    
    # Format the prompt
    formatted_prompt = prompt_template.format(
        portfolio_context=yaml.dump(portfolio_data, allow_unicode=True, default_flow_style=False),
        incoming_intelligence=json.dumps(incoming_data, indent=2, ensure_ascii=False)
    )

    # Output the prepared data and instructions for Sisyphus
    print("--- Sisyphus Prompt Start ---")
    print(formatted_prompt)
    print("--- Sisyphus Prompt End ---")
    print("\n-------------------------------------------------------------")
    print("Please copy the content between '--- Sisyphus Prompt Start ---' and '--- Sisyphus Prompt End ---'")
    print("and provide it to Sisyphus for reasoning and report generation.")
    print("Once Sisyphus returns the Markdown report, save it to a file")
    
    # Simulate Sisyphus's response and report generation
    # For now, let's use a placeholder or read a pre-generated report for testing alert logic
    # In a real scenario, this would involve receiving actual output from Sisyphus.
    
    # Placeholder for generated_report_content
    # Example for testing alert logic:
    generated_report_content = """
# 🚀 Daily Alpha Briefing - 2026-01-14

## 💡 Key Alpha Opportunities (獵人發現)

### Advanced Nuclear (高階核能)
- **概述**: 美國能源部已撥款 27 億美元用於鈾濃縮能力，旨在提升國內產能並減少對外國燃料的依賴。
- **信號**:
    - [DOE Selects 3 Companies for $2.7B Uranium Enrichment Capacity Initiative](https://executivegov.com/articles/energy-department-task-orders-haleu-leu) - ExecutiveGov
- **二階思考**: 政策利好，長期機會。
- **信心 (Confidence)**: 88

### Autonomous Vehicles (自動駕駛)
- **概述**: Waymo擴張與監管挑戰並存，紐約州政策帶來新機遇。
- **信號**:
    - [Waymo Targets 1 Million Robotaxi Rides A Week](https://www.forbes.com/sites/alanohnsman/2025/12/10/waymo-targets-1-million-robotaxi-rides-a-week/) - Forbes
- **二階思考**: 對TSLA等有潛在影響，需關注法規。
- **信心 (Confidence)**: 75

## ⚠️ Portfolio Risk Alerts (護盾監測)

### TSLA - Tesla
- **風險類型**: 監管與社會阻力
- **概述**: Lyft和Uber司機抗議Waymo機器人計程車，加州考慮進一步監管。
- **信號**:
    - [Lyft and Uber drivers protest Waymo robotaxis as California considers further regulations](https://www.msn.com/en-us/money/companies/lyft-and-uber-drivers-protest-waymo-robotaxis-as-california-considers-further-regulations/ar-AA1TUOqV) - Associated Press News
- **影響評估**: 對自動駕駛商業化進程構成潛在阻礙，可能間接影響TSLA。
- **風險評分 (Risk Score)**: 92

## 📊 總體情緒與結論

- **概述**: 市場技術創新活躍，但自動駕駛面臨監管阻力。
- **可行洞察**: 核能、光子學長期看好。自動駕駛需關注監管風險。
"""
    
    report_filename = f"daily_alpha_{datetime.now().strftime('%Y%m%d')}.md"
    report_filepath = os.path.join(REPORTS_DIR, report_filename)
    
    with open(report_filepath, 'w') as f:
        f.write(generated_report_content)
    print(f"Report saved to {report_filepath}")

    # --- ALERT TRIGGERING LOGIC ---
    opportunity_alerts = []
    risk_alerts = []

    # Simplified parsing: First extract blocks, then within blocks extract details
    
    # Pattern for Alpha Opportunities blocks
    alpha_opportunity_pattern = re.compile(r"## 💡 Key Alpha Opportunities \(獵人發現\)(.*?)(?=\n## ⚠️ Portfolio Risk Alerts \(護盾監測\))", re.DOTALL)
    alpha_opportunities_section = alpha_opportunity_pattern.search(generated_report_content)

    if alpha_opportunities_section:
        opportunities_text = alpha_opportunities_section.group(1)
        # Each opportunity block starts with ### and ends before next ### or end of section
        individual_opportunity_blocks = re.findall(r"(###.*?)(?=(?:###|$))", opportunities_text, re.DOTALL)
        
        for block in individual_opportunity_blocks:
            theme_match = re.search(r"###\s*(.*?)\s*\(.*?\)", block)
            confidence_match = re.search(r"- \*\*信心 \(Confidence\)\*\*: (\d+)", block)
            url_match = re.search(r"\[.*?\]\((https?://[^\s\)]+)\)", block) # Capture any URL in the block

            if theme_match and confidence_match and url_match:
                theme = theme_match.group(1).strip()
                confidence_score = int(confidence_match.group(1))
                url = url_match.group(1)

                if confidence_score > 95:
                    alert_message = (
                        f"🚀 Kazuha Invest Alert: 高置信度 Alpha 機會！\n"
                        f"主題: {theme}\n"
                        f"信心分數: {confidence_score}\n"
                        f"相關連結: {url}"
                    )
                    opportunity_alerts.append(alert_message)

    # Pattern for Portfolio Risk Alerts blocks
    risk_alert_pattern = re.compile(r"## ⚠️ Portfolio Risk Alerts \(護盾監測\)(.*?)(?=\n## 📊 總體情緒與結論|$)", re.DOTALL)
    risk_alerts_section = risk_alert_pattern.search(generated_report_content)

    if risk_alerts_section:
        risks_text = risk_alerts_section.group(1)
        individual_risk_blocks = re.findall(r"(###.*?)(?=(?:###|$))", risks_text, re.DOTALL)
        
        for block in individual_risk_blocks:
            asset_match = re.search(r"###\s*(.*?)\s*-\s*(.*)", block)
            risk_score_match = re.search(r"- \*\*風險評分 \(Risk Score\)\*\*: (\d+)", block)
            url_match = re.search(r"\[.*?\]\((https?://[^\s\)]+)\)", block) # Capture any URL in the block

            if asset_match and risk_score_match and url_match:
                asset_ticker = asset_match.group(1).strip() # Ticker
                asset_name = asset_match.group(2).strip()
                risk_score = int(risk_score_match.group(1))
                url = url_match.group(1)

                if risk_score > 90:
                    alert_message = (
                        f"⚠️ Kazuha Invest Alert: 高風險警報！\n"
                        f"資產: {asset_ticker} - {asset_name}\n"
                        f"風險分數: {risk_score}\n"
                        f"相關連結: {url}"
                    )
                    risk_alerts.append(alert_message)
    
    if opportunity_alerts or risk_alerts:
        for alert_msg in opportunity_alerts:
            await send_telegram_message(alert_msg)
        for alert_msg in risk_alerts:
            await send_telegram_message(alert_msg)
        print("Critical alerts processed and sent via Telegram if thresholds met.")
    else:
        print("No critical alerts triggered based on current thresholds.")

    print("-------------------------------------------------------------")
    print(f"Daily Alpha Briefing generated and saved to '{report_filepath}'.")
    print("Alerts (if any) have been sent via Telegram.")
    print("-------------------------------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())

import os
import json
import yaml
from datetime import datetime
import asyncio
import re
from src.notifier import send_telegram_message
from src.utils.model_factory import ai_factory

# Configuration
INCOMING_DIR = "data/Incoming"
PORTFOLIO_PATH = "data/portfolio.yml"
REPORTS_DIR = "data/Reports"

def load_data(directory):
    all_data = []
    if not os.path.exists(directory):
        return []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {filepath}")
    return all_data

def load_portfolio(filepath):
    if not os.path.exists(filepath):
        return {"portfolio": []}
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

async def main():
    # 1. Load data
    incoming_data = load_data(INCOMING_DIR)
    portfolio_data = load_portfolio(PORTFOLIO_PATH)

    if not incoming_data:
        print("No incoming data found. Skipping report generation.")
        return

    prompt_template = """
You are Kazuha Invest 2.0, an AI tasked with generating a daily Alpha Briefing based on incoming market intelligence.
Your goal is to perform "second-order thinking" and identify potential opportunities (Alpha) and risks for the portfolio.

Here is the current portfolio for context:
{portfolio_context}

Here is the raw market intelligence data collected today:
{incoming_intelligence}

Based on this information, please generate a "Daily Alpha Briefing" in Markdown format, following this exact structure:

```markdown
# 🚀 Daily Alpha Briefing - {date}

## 💡 Key Alpha Opportunities (獵人發現)

### [宏觀主題 1 標題]
- **概述**: [與此主題相關的新聞/信號簡要總結。]
- **信號**:
    - [信號 1 - URL, 標題, 來源]
    - [信號 2 - URL, 標題, 來源]
- **二階思考**: [我對潛在影響、相關股票或未來發展的分析。]
- **信心 (Confidence)**: [0-100 score]

## ⚠️ Portfolio Risk Alerts (護盾監測)

### [資產代碼 1] - [資產名稱]
- **風險類型**: [例如：訴訟、調查、負面新聞]
- **概述**: [風險新聞的簡要總結。]
- **信號**:
    - [風險信號 1 - URL, 標題, 來源]
- **影響評估**: [我對資產、其行業或更廣泛市場潛在影響的分析。]
- **風險評分 (Risk Score)**: [0-100 score]

## 📊 總體情緒與結論

- **概述**: [從新聞中得出整體市場情緒的簡要總結。]
- **可行洞察**: [任何清晰、簡潔的可行洞察或值得進一步調查的領域。]
```

Please provide a **信心 (Confidence)** score (0-100) and **風險評分 (Risk Score)** (0-100) respectively. 
Fill in all sections based on the provided data. 
If no opportunities or risks are found for a category, state that clearly (e.g., "無發現潛在風險。").
Focus on high-conviction insights and prioritize information relevant to the provided portfolio and macro themes.
"""
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    formatted_prompt = prompt_template.format(
        portfolio_context=yaml.dump(portfolio_data, allow_unicode=True, default_flow_style=False),
        incoming_intelligence=json.dumps(incoming_data, indent=2, ensure_ascii=False),
        date=current_date
    )

    print("Generating report with OpenRouter...")
    raw_content = ai_factory.call("REASONING", formatted_prompt)
    
    if not raw_content:
        print("Failed to generate report.")
        return

    # Extract Markdown content if blocks exist (to strip preamble/thinking)
    if "```markdown" in raw_content:
        generated_report_content = raw_content.split("```markdown")[1].split("```")[0].strip()
    elif "```" in raw_content:
        generated_report_content = raw_content.split("```")[1].split("```")[0].strip()
    else:
        generated_report_content = raw_content.strip()

    # 4. Save Report
    report_filename = f"daily_alpha_{datetime.now().strftime('%Y%m%d')}.md"
    report_filepath = os.path.join(REPORTS_DIR, report_filename)
    
    with open(report_filepath, 'w') as f:
        f.write(generated_report_content)
    print(f"Report saved to {report_filepath}")

    # 5. Alert Triggering Logic
    opportunity_alerts = []
    risk_alerts = []

    alpha_section = re.search(r"## 💡 Key Alpha Opportunities \(獵人發現\)(.*?)(?=\n## ⚠️|$)", generated_report_content, re.DOTALL)
    if alpha_section:
        blocks = re.findall(r"(###.*?)(?=(?:###|$))", alpha_section.group(1), re.DOTALL)
        for block in blocks:
            theme_m = re.search(r"###\s*(.*?)\s*[\n\(]", block)
            conf_m = re.search(r"Confidence\)\*\*: (\d+)", block)
            url_m = re.search(r"\[.*?\]\((https?://[^\s\)]+)\)", block)
            
            if theme_m and conf_m:
                score = int(conf_m.group(1))
                if score > 85: # PRD Threshold
                    msg = f"🚀 Alpha Alert: {theme_m.group(1).strip()}\nScore: {score}"
                    if url_m: msg += f"\nLink: {url_m.group(1)}"
                    opportunity_alerts.append(msg)

    risk_section = re.search(r"## ⚠️ Portfolio Risk Alerts \(護盾監測\)(.*?)(?=\n## 📊|$)", generated_report_content, re.DOTALL)
    if risk_section:
        blocks = re.findall(r"(###.*?)(?=(?:###|$))", risk_section.group(1), re.DOTALL)
        for block in blocks:
            asset_m = re.search(r"###\s*(.*?)\s*-\s*(.*)", block)
            risk_m = re.search(r"Risk Score\)\*\*: (\d+)", block)
            url_m = re.search(r"\[.*?\]\((https?://[^\s\)]+)\)", block)
            
            if asset_m and risk_m:
                score = int(risk_m.group(1))
                if score > 90: # PRD Threshold
                    msg = f"⚠️ Risk Alert: {asset_m.group(1).strip()}\nScore: {score}"
                    if url_m: msg += f"\nLink: {url_m.group(1)}"
                    risk_alerts.append(msg)

    for msg in opportunity_alerts + risk_alerts:
        await send_telegram_message(msg)
        print(f"Sent alert: {msg.splitlines()[0]}")

if __name__ == "__main__":
    asyncio.run(main())

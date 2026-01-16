```python
import yaml
import json
import time
import os
from datetime import datetime
import random # Added random import
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from src.config import PATHS, STRATEGY

RISK_KEYWORDS = [
    "Lawsuit", "Fraud", "Investigation", "SEC", "Short Seller", 
    "Delay", "Crash", "Explosion", "Hacked", "Bankruptcy", "Scandal",
    "Layoff", "CEO Resigns", "Product Recall", "Cyberattack"
]

def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def search_risks(name, ticker):
    results = []
    risk_query_part = " OR ".join([f'"{k}"' for k in RISK_KEYWORDS])
    query = f'"{name}" ({risk_query_part})'
    
    print(f"Shield Scan: {ticker}...")
    
    try:
        with DDGS() as ddgs:
            news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=5)
            for res in news_results:
                res['asset'] = ticker
                res['risk_level'] = "HIGH"
                res['source_type'] = "Shield"
                results.append(res)
            time.sleep(1)
    except Exception as e:
        print(f"Error shielding {ticker}: {e}")
        
    return results

def main():
    os.makedirs(PATHS["INCOMING"], exist_ok=True)
    
    # 1. Official Portfolio
    portfolio_data = load_yaml(PATHS["PORTFOLIO"])
    portfolio = portfolio_data.get('portfolio', [])
    
    # 2. Dynamic Missions (Check themes as potential competitors/risks)
    missions_data = load_yaml(PATHS["MISSIONS"])
    active_missions = missions_data.get('active_missions', [])
    
    targets = []
    # Add portfolio assets
    for asset in portfolio:
        targets.append({'name': asset['name'], 'ticker': asset['ticker']})
    
    # Add dynamic mission themes if they look like tickers or specific company names
    for m in active_missions:
        targets.append({'name': m['theme'], 'ticker': f"DYN:{m['theme'][:4]}"})

    all_alerts = []
    print(f"Starting Shield Scan for {len(targets)} targets...")
    
    for t in targets:
        alerts = search_risks(t['name'], t['ticker'])
        all_alerts.extend(alerts)
            
    if all_alerts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(PATHS["INCOMING"], f"shield_results_{timestamp}.json")
        with open(output_file, 'w') as f:
            json.dump(all_alerts, f, indent=2)
        print(f"Saved {len(all_alerts)} alerts to {output_file}")

if __name__ == "__main__":
    main()

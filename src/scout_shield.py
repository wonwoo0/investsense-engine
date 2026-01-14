import yaml
import json
import time
import os
from datetime import datetime
from duckduckgo_search import DDGS

# Configuration
PORTFOLIO_PATH = "data/portfolio.yml"
OUTPUT_DIR = "data/Incoming"
RISK_KEYWORDS = [
    "Lawsuit", "Fraud", "Investigation", "SEC", "Short Seller", 
    "Delay", "Crash", "Explosion", "Hacked", "Bankruptcy", "Scandal"
]

def load_portfolio():
    if not os.path.exists(PORTFOLIO_PATH):
        print(f"Error: {PORTFOLIO_PATH} not found.")
        return []
    with open(PORTFOLIO_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('portfolio', [])

def search_risks(asset):
    results = []
    ticker = asset.get('ticker')
    name = asset.get('name')
    keywords = asset.get('keywords', [])
    
    # Construct a query combining the name and risk terms
    # "Rocket Lab" AND ("Lawsuit" OR "Fraud" ...)
    risk_query_part = " OR ".join([f'"{k}"' for k in RISK_KEYWORDS])
    
    # We search for the Name primarily, adding Ticker if short
    search_term = f'"{name}"'
    
    query = f'{search_term} ({risk_query_part})'
    print(f"Scanning: {ticker} - {query}...")
    
    try:
        with DDGS() as ddgs:
            # Search news from last 7 days ('w') or day ('d'). 'm' is month.
            # strict=True disables safe search which might filter relevant bad news? 
            # safe="off"
            news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=5)
            
            for res in news_results:
                res['asset'] = ticker
                res['risk_level'] = "HIGH" # Potential high risk
                res['source_type'] = "Shield"
                results.append(res)
                
            time.sleep(1) # Rate limit politeness
            
    except Exception as e:
        print(f"Error searching for {ticker}: {e}")
        
    return results

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    portfolio = load_portfolio()
    all_alerts = []
    
    print(f"Starting Shield Scan for {len(portfolio)} assets...")
    
    for asset in portfolio:
        alerts = search_risks(asset)
        if alerts:
            print(f"⚠️ Found {len(alerts)} potential risks for {asset['ticker']}")
            all_alerts.extend(alerts)
        else:
            print(f"✅ No immediate risks found for {asset['ticker']}")
            
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"shield_results_{timestamp}.json")
    
    if all_alerts:
        with open(output_file, 'w') as f:
            json.dump(all_alerts, f, indent=2)
        print(f"Saved {len(all_alerts)} alerts to {output_file}")
    else:
        print("System Clean. No risks detected.")

if __name__ == "__main__":
    main()

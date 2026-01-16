```python
import yaml
import json
import time
import os
import random
from datetime import datetime
from ddgs import DDGS
from src.config import PATHS, STRATEGY

RISK_KEYWORDS = [
    "Lawsuit", "Fraud", "Investigation", "SEC", "Short Seller", 
    "Delay", "Crash", "Explosion", "Hacked", "Bankruptcy", "Scandal",
    "Layoff", "CEO Resigns", "Product Recall", "Cyberattack"
]

# Rate limiting state
rate_limit_count = 0
max_rate_limit_tolerance = 3
query_count = 0
max_queries_per_run = 50  # Cap queries per run

def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def search_risks(name, ticker):
    global rate_limit_count, query_count
    
    # Check query cap
    if query_count >= max_queries_per_run:
        print(f"⚠️  Query cap reached ({max_queries_per_run}). Skipping {ticker}.")
        return []
    
    # Check rate limit tolerance
    if rate_limit_count >= max_rate_limit_tolerance:
        print(f"⚠️  Rate limit threshold reached ({max_rate_limit_tolerance}). Cooldown active. Skipping {ticker}.")
        return []
    
    results = []
    risk_query_part = " OR ".join([f'"{k}"' for k in RISK_KEYWORDS])
    query = f'"{name}" ({risk_query_part})'
    
    print(f"Scanning: {ticker} - \"{name}\" ({risk_query_part})...")
    
    # Add jitter to prevent thundering herd
    jitter = random.uniform(1, 3)
    time.sleep(jitter)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            query_count += 1
            with DDGS() as ddgs:
                news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=5)
                for res in news_results:
                    res['asset'] = ticker
                    res['risk_level'] = "HIGH"
                    res['source_type'] = "Shield"
                    results.append(res)
                
                # Reset rate limit count on success
                rate_limit_count = 0
                time.sleep(1)
                return results
        except Exception as e:
            error_msg = str(e)
            if "202" in error_msg or "Ratelimit" in error_msg or "rate" in error_msg.lower():
                rate_limit_count += 1
                wait_time = (2 ** attempt) * 5 + random.uniform(0, 3)  # Exponential backoff with jitter
                print(f"Error searching for {ticker}: {query} {error_msg}")
                
                if rate_limit_count >= max_rate_limit_tolerance:
                    print(f"⚠️  Rate limit threshold reached. Entering cooldown mode.")
                    return []
                
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries reached for {ticker}. Skipping.")
            else:
                print(f"Error searching for {ticker}: {e}")
                break
        
    return results

def main():
    global rate_limit_count, query_count
    rate_limit_count = 0
    query_count = 0
    
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
    print(f"Starting Shield Scan for {len(targets)} assets...")
    
    for t in targets:
        alerts = search_risks(t['name'], t['ticker'])
        all_alerts.extend(alerts)
        
        # Early exit if rate limited
        if rate_limit_count >= max_rate_limit_tolerance:
            print(f"⚠️  Rate limit cooldown. Stopping shield scan early.")
            break
            
    if all_alerts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(PATHS["INCOMING"], f"shield_results_{timestamp}.json")
        with open(output_file, 'w') as f:
            json.dump(all_alerts, f, indent=2)
        print(f"🛡️  Shield: {len(all_alerts)} potential risks detected. Saved to {output_file}")
    else:
        print("✅ No immediate risks found for " + ", ".join([t['ticker'] for t in targets]))
    
    print("System Clean. No risks detected.")

if __name__ == "__main__":
    main()

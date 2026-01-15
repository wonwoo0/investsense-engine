import json
import time
import os
import re
import yaml
from datetime import datetime
from duckduckgo_search import DDGS

PORTFOLIO_PATH = "data/portfolio.yml"
OUTPUT_DIR = "data/Incoming"

def load_portfolio():
    if not os.path.exists(PORTFOLIO_PATH):
        return []
    with open(PORTFOLIO_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('portfolio', [])

def scout_labor(asset):
    results = []
    name = asset.get('name')
    ticker = asset.get('ticker')
    
    # We focus on key technical terms mentioned in White Paper
    LABOR_TERMS = ["Engineer", "Packaging", "Enrichment", "Physicist", "Deployment", "Scale"]
    term_query = " OR ".join([f'"{t}"' for t in LABOR_TERMS])
    
    # Google Dorking style via DDG
    query = f'site:linkedin.com/jobs "{name}" ({term_query})'
    
    print(f"Labor Scouting: {ticker}...")
    
    try:
        with DDGS() as ddgs:
            # Using text search for job boards
            search_results = ddgs.text(keywords=query, region="wt-wt", safesearch="off", max_results=5)
            for res in search_results:
                res['asset'] = ticker
                res['source_type'] = "Labor"
                results.append(res)
            time.sleep(1)
    except Exception as e:
        print(f"Error scouting labor for {ticker}: {e}")
        
    return results

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    portfolio = load_portfolio()
    all_signals = []
    
    for asset in portfolio:
        signals = scout_labor(asset)
        all_signals.extend(signals)
        
    if all_signals:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"labor_results_{timestamp}.json")
        with open(output_file, 'w') as f:
            json.dump(all_signals, f, indent=2)
        print(f"Saved {len(all_signals)} labor signals to {output_file}")
    else:
        print("No significant labor trends found.")

if __name__ == "__main__":
    main()

import json
import time
import os
import random
import yaml
from datetime import datetime
from ddgs import DDGS

PORTFOLIO_PATH = "data/portfolio.yml"
OUTPUT_DIR = "data/Incoming"

# Rate limiting state
rate_limit_count = 0
max_rate_limit_tolerance = 3
query_count = 0
max_queries_per_run = 50  # Cap queries per run

def load_portfolio():
    if not os.path.exists(PORTFOLIO_PATH):
        return []
    with open(PORTFOLIO_PATH, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('portfolio', [])

def scout_labor(asset):
    global rate_limit_count, query_count
    
    # Check query cap
    if query_count >= max_queries_per_run:
        print(f"⚠️  Query cap reached ({max_queries_per_run}). Skipping {asset.get('ticker')}.")
        return []
    
    # Check rate limit tolerance
    if rate_limit_count >= max_rate_limit_tolerance:
        print(f"⚠️  Rate limit threshold reached. Cooldown active. Skipping {asset.get('ticker')}.")
        return []
    
    results = []
    name = asset.get('name')
    ticker = asset.get('ticker')
    
    # We focus on key technical terms mentioned in White Paper
    LABOR_TERMS = ["Engineer", "Packaging", "Enrichment", "Physicist", "Deployment", "Scale"]
    term_query = " OR ".join([f'"{t}"' for t in LABOR_TERMS])
    
    # Google Dorking style via DDG
    query = f'site:linkedin.com/jobs "{name}" ({term_query})'
    
    print(f"Labor Scouting: {ticker}...")
    
    # Add jitter to prevent thundering herd
    jitter = random.uniform(1, 3)
    time.sleep(jitter)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            query_count += 1
            with DDGS() as ddgs:
                # Using text search for job boards
                search_results = ddgs.text(keywords=query, region="wt-wt", safesearch="off", max_results=5)
                for res in search_results:
                    res['asset'] = ticker
                    res['source_type'] = "Labor"
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
                print(f"Error scouting labor for {ticker}: {error_msg}")
                
                if rate_limit_count >= max_rate_limit_tolerance:
                    print(f"⚠️  Rate limit threshold reached. Entering cooldown mode.")
                    return []
                
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries reached for {ticker}. Skipping.")
            else:
                print(f"Error scouting labor for {ticker}: {e}")
                break
        
    return results

def main():
    global rate_limit_count, query_count
    rate_limit_count = 0
    query_count = 0
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    portfolio = load_portfolio()
    all_signals = []
    
    for asset in portfolio:
        signals = scout_labor(asset)
        all_signals.extend(signals)
        
        # Early exit if rate limited
        if rate_limit_count >= max_rate_limit_tolerance:
            print(f"⚠️  Rate limit cooldown. Stopping labor scout early.")
            break
        
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

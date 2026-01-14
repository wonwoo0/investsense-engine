import feedparser
import yaml
import json
import os
import time
from datetime import datetime
import hashlib
import requests

def load_sources(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def quick_filter(entry):
    title = entry.get('title', '').lower()
    summary = entry.get('description', '').lower() if 'description' in entry else entry.get('summary', '').lower()
    url = entry.get('link', '')
    content = title + " " + summary
    
    # Negative Keywords
    NEGATIVE_KEYWORDS = ['tutorial', 'how to', 'review', 'podcast', 'video only', 'giveaway']
    if any(nw in content for nw in NEGATIVE_KEYWORDS):
        return False

    # Trusted Domains
    TRUSTED_DOMAINS = ['spacenews.com', 'eetimes.com', 'semiengineering.com', 'world-nuclear-news.org']
    if any(domain in url for domain in TRUSTED_DOMAINS):
        return True
    
    # Portfolio Keywords
    PORTFOLIO_KEYWORDS = ['rklb', 'rocket lab', 'tesla', 'tsla', 'poet', 'photonics', 'ondas']
    if any(kw in content for kw in PORTFOLIO_KEYWORDS):
        return True
    
    # Financial Signals
    FINANCIAL_SIGNALS = ['ipo', 'acquired', 'acquisition', 'partnership', 'raises $', 'closes $', 'announces']
    if any(signal in content for signal in FINANCIAL_SIGNALS):
        return True
    
    # Tech Signals
    TECH_SIGNALS = ['breakthrough', 'first ever', 'record', 'milestone']
    if any(signal in content for signal in TECH_SIGNALS):
        return True
    
    return False

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def scout_feed():
    sources_file = 'data/sources.yml'
    history_file = 'data/history_hashes.json'
    
    if not os.path.exists(sources_file):
        print(f"Sources file {sources_file} not found.")
        return

    sources = load_sources(sources_file)
    history = {}
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    all_entries = []
    # Only Tier 1 for now as per plan
    for source in sources.get('tier1', []):
        print(f"Fetching {source['name']}...")
        try:
            response = requests.get(source['url'], headers=headers, timeout=15)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            print(f"Found {len(feed.entries)} entries in {source['name']}")
            
            for entry in feed.entries:
                if quick_filter(entry):
                    entry_data = {
                        'title': entry.get('title'),
                        'link': entry.get('link'),
                        'summary': entry.get('summary') or entry.get('description'),
                        'source': source['name'],
                        'published': entry.get('published'),
                        'category': source['category']
                    }
                    
                    # Hash-based dedup
                    h = get_hash(entry_data['title'])
                    current_time = time.time()
                    
                    # Check history (48 hours = 172800 seconds)
                    if h in history:
                        if current_time - history[h] < 172800:
                            continue
                    
                    all_entries.append(entry_data)
                    history[h] = current_time
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")

    # Cleanup old history entries
    history = {k: v for k, v in history.items() if time.time() - v < 172800}
    
    with open(history_file, 'w') as f:
        json.dump(history, f)

    if all_entries:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'data/Incoming/rss_results_{timestamp}.json'
        os.makedirs('data/Incoming', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(all_entries, f, indent=2)
        print(f"Saved {len(all_entries)} entries to {output_file}")
    else:
        print("No new relevant entries found.")

if __name__ == "__main__":
    scout_feed()

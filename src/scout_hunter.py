import json
import time
import os
import random
import yaml
from datetime import datetime
from ddgs import DDGS

OUTPUT_DIR = "data/Incoming"
THEMES_PATH = "data/themes.yml"
MISSIONS_PATH = "data/active_missions.yml"

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

def save_yaml(path, data):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f)

def filter_active_missions(missions_data):
    """Removes expired missions based on current date."""
    if not missions_data or 'active_missions' not in missions_data:
        return []
    
    today = datetime.now().strftime("%Y-%m-%d")
    valid_missions = []
    
    for m in missions_data['active_missions']:
        if m.get('expires_at', '9999-12-31') >= today:
            valid_missions.append(m)
        else:
            print(f"Mission '{m.get('theme')}' expired. Removing.")
            
    return valid_missions

def hunt_theme(theme, keywords, depth=3):
    global rate_limit_count, query_count
    
    # Check query cap
    if query_count >= max_queries_per_run:
        print(f"⚠️  Query cap reached ({max_queries_per_run}). Skipping {theme}.")
        return []
    
    # Check rate limit tolerance
    if rate_limit_count >= max_rate_limit_tolerance:
        print(f"⚠️  Rate limit threshold reached. Cooldown active. Skipping {theme}.")
        return []
    
    results = []
    query_part = " OR ".join([f'"{k}"' for k in keywords])
    query = f'"{theme}" ({query_part})'
    
    print(f"Hunting: {theme}...")
    
    # Add jitter to prevent thundering herd
    jitter = random.uniform(5, 10)
    time.sleep(jitter)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            query_count += 1
            with DDGS() as ddgs:
                news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=depth)
            
                for res in news_results:
                    res['theme'] = theme
                    res['source_type'] = "Hunter"
                    results.append(res)
                
                # Reset rate limit count on success
                rate_limit_count = 0
                return results
        except Exception as e:
            error_msg = str(e)
            if "202" in error_msg or "Ratelimit" in error_msg or "rate" in error_msg.lower():
                rate_limit_count += 1
                wait_time = (2 ** attempt) * 5 + random.uniform(0, 3)  # Exponential backoff with jitter
                print(f"Error hunting {theme}: {query} {error_msg}")
                
                if rate_limit_count >= max_rate_limit_tolerance:
                    print(f"⚠️  Rate limit threshold reached. Entering cooldown mode.")
                    return []
                
                if attempt < max_retries - 1:
                    print(f"Rate limit hit. Retrying in {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries reached for {theme}. Skipping.")
            else:
                print(f"Error hunting {theme}: {e}")
                break
        
    return results

def main():
    global rate_limit_count, query_count
    rate_limit_count = 0
    query_count = 0
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    all_findings = []
    
    # 1. Load Static Themes
    themes_data = load_yaml(THEMES_PATH)
    static_themes = themes_data.get('themes', [])
    
    # 2. Load and Filter Dynamic Missions
    missions_data = load_yaml(MISSIONS_PATH)
    active_missions = filter_active_missions(missions_data)
    
    # Update missions file (remove expired ones)
    save_yaml(MISSIONS_PATH, {'active_missions': active_missions})
    
    print(f"Starting Hunter Protocol for {len(static_themes) + len(active_missions)} themes...")
    
    # Process Static Themes
    for t in static_themes:
        findings = hunt_theme(t['name'], t['keywords'], depth=3)
        all_findings.extend(findings)
        
        # Early exit if rate limited
        if rate_limit_count >= max_rate_limit_tolerance:
            print(f"⚠️  Rate limit cooldown. Stopping hunter protocol early.")
            break
        
    # Process Dynamic Missions (Greater Depth) if not rate limited
    if rate_limit_count < max_rate_limit_tolerance:
        for m in active_missions:
            findings = hunt_theme(m['theme'], m['keywords'], depth=m.get('depth', 15))
            all_findings.extend(findings)
            
            # Early exit if rate limited
            if rate_limit_count >= max_rate_limit_tolerance:
                print(f"⚠️  Rate limit cooldown. Stopping hunter protocol early.")
                break
        
    # Save results
    if all_findings:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"hunter_results_{timestamp}.json")
        with open(output_file, 'w') as f:
            json.dump(all_findings, f, indent=2)
        print(f"Captured {len(all_findings)} signals to {output_file}")
    else:
        print("No significant signals found.")

if __name__ == "__main__":
    main()

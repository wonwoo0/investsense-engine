import json
import time
import os
import yaml
from datetime import datetime
from duckduckgo_search import DDGS

OUTPUT_DIR = "data/Incoming"
THEMES_PATH = "data/themes.yml"
MISSIONS_PATH = "data/active_missions.yml"

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
    results = []
    query_part = " OR ".join([f'"{k}"' for k in keywords])
    query = f'"{theme}" ({query_part})'
    
    print(f"Hunting Theme: {theme} (Depth: {depth})...")
    
    try:
        # Add random sleep before making the request
        time.sleep(random.uniform(5, 10))

        if ddgs_session:
            news_results = ddgs_session.news(keywords=query, region="wt-wt", safesearch="off", max_results=depth)
        else:
            with DDGS() as ddgs:
                news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=depth)
        
        for res in news_results:
            res['theme'] = theme
            res['source_type'] = "Hunter"
            results.append(res)
    except Exception as e:
        print(f"Error hunting {theme}: {e}")
        
    return results

def main():
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
    
    print(f"Starting Hunter Protocol. Static: {len(static_themes)} | Dynamic: {len(active_missions)}")
    
    # Process Static Themes
    for t in static_themes:
        findings = hunt_theme(t['name'], t['keywords'], depth=3)
        all_findings.extend(findings)
        
    # Process Dynamic Missions (Greater Depth)
    for m in active_missions:
        findings = hunt_theme(m['theme'], m['keywords'], depth=m.get('depth', 15))
        all_findings.extend(findings)
        
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

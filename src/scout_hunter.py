import json
import time
import os
import yaml
import random
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

def hunt_cluster(cluster_name, keywords, depth=3):
    results = []
    # Query: "Primary" ("Sec1" OR "Sec2" ...)
    # If keywords list is flat, take first as primary, rest as secondary
    if not keywords: return []
    
    primary = keywords[0]
    secondary = keywords[1:]
    
    query_part = " OR ".join([f'"{k}"' for k in secondary])
    query = f'"{primary}" ({query_part})' if secondary else f'"{primary}"'
    
    print(f"Hunting Cluster: {cluster_name} (Depth: {depth})...")
    
    try:
        # Rate limit politeness
        time.sleep(random.uniform(3, 7))
        
        with DDGS() as ddgs:
            # Enforce time='d' (Past Day) to fix Stale Results
            news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=depth, timelimit="d")
            
            for res in news_results:
                res['theme'] = cluster_name
                res['source_type'] = "Hunter_Cluster"
                results.append(res)
                
    except Exception as e:
        print(f"Error hunting {cluster_name}: {e}")
        
    return results

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    all_findings = []
    
    # 1. Load Clusters from Themes
    themes_data = load_yaml(THEMES_PATH)
    clusters = themes_data.get('clusters', [])
    
    # 2. Load Missions (Keep as legacy support or specialized searches)
    missions_data = load_yaml(MISSIONS_PATH)
    active_missions = missions_data.get('active_missions', []) # Skipping filter logic for brevity, add back if needed

    print(f"Starting Hunter Protocol. Clusters: {len(clusters)} | Missions: {len(active_missions)}")
    
    # Process Clusters (High Efficiency)
    for c in clusters:
        # Use 'keywords' list from YAML if available, else construct from primary/secondary
        keys = c.get('keywords', [])
        if not keys and 'primary' in c:
            keys = [c['primary']] + c.get('secondary', [])
            
        findings = hunt_cluster(c['name'], keys, depth=5)
        all_findings.extend(findings)
        
    # Process Active Missions (Targeted)
    for m in active_missions:
        findings = hunt_cluster(m['theme'], m['keywords'], depth=m.get('depth', 5))
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

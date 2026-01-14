import json
import time
import os
from datetime import datetime
from duckduckgo_search import DDGS

OUTPUT_DIR = "data/Incoming"

# From README Section 8
MACRO_THEMES = {
    "Advanced Nuclear": ["SMR", "Uranium", "Kairos Power", "TerraPower"],
    "AI Infrastructure": ["Data Centers", "Liquid Cooling", "GPU Supply Chain"],
    "Autonomous Vehicles": ["FSD", "Robotaxi", "Waymo", "Regulation"],
    "Space Tech": ["Satellite Constellations", "Reusable Rockets", "Space Debris"],
    "Photonics": ["Optical Interconnects", "Silicon Photonics", "CPO"],
    "Solid State Battery": ["QuantumScape", "Energy Density", "EV Range"]
}

def hunt_theme(theme, keywords):
    results = []
    # Query: "Advanced Nuclear" (SMR OR Uranium OR ...)
    query_part = " OR ".join([f'"{k}"' for k in keywords])
    query = f'"{theme}" ({query_part})'
    
    print(f"Hunting: {theme}...")
    
    try:
        with DDGS() as ddgs:
            # broader search
            news_results = ddgs.news(keywords=query, region="wt-wt", safesearch="off", max_results=3)
            for res in news_results:
                res['theme'] = theme
                res['source_type'] = "Hunter"
                results.append(res)
            time.sleep(1)
    except Exception as e:
        print(f"Error hunting {theme}: {e}")
        
    return results

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    all_findings = []
    
    print(f"Starting Hunter Protocol for {len(MACRO_THEMES)} themes...")
    
    for theme, keywords in MACRO_THEMES.items():
        findings = hunt_theme(theme, keywords)
        all_findings.extend(findings)
        
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"hunter_results_{timestamp}.json")
    
    if all_findings:
        with open(output_file, 'w') as f:
            json.dump(all_findings, f, indent=2)
        print(f"Captured {len(all_findings)} signals to {output_file}")
    else:
        print("No significant signals found.")

if __name__ == "__main__":
    main()

import os
import json
import yaml
import logging
import requests
import random
import time
from datetime import datetime, timedelta
from duckduckgo_search import DDGS
from src.config import OPENROUTER_API_KEY, PATHS

# Constants
MODEL_NAME = "nvidia/nemotron-3-nano-30b-a3b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
PROCESSED_DIR = "data/Processed"
MISSIONS_FILE = "data/active_missions.yml"
LIBRARIAN_LOG = "data/Knowledge/librarian_log.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutLibrarian:
    def __init__(self):
        self.processed_dir = PROCESSED_DIR
        self.missions_file = MISSIONS_FILE
        
    def load_recent_signals(self):
        """Loads signals processed in the last 24 hours."""
        if not os.path.exists(self.processed_dir):
            return []
            
        files = [f for f in os.listdir(self.processed_dir) if f.endswith('.json')]
        recent_items = []
        
        # Simple Logic: Just load all current processed files 
        # (Assuming Archiver cleans up old ones or filenames contain dates)
        for f in files:
            path = os.path.join(self.processed_dir, f)
            try:
                with open(path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        recent_items.extend(data)
            except Exception as e:
                logger.error(f"Error loading {f}: {e}")
                
        return recent_items

    def generate_missions(self, signals):
        """Uses Nemotron to generate follow-up missions."""
        if not signals or not OPENROUTER_API_KEY:
            logger.warning("No signals to analyze or missing API Key.")
            return []

        # Summarize signals for context (Title + Gatekeeper Score)
        context = "\n".join([f"- {s.get('title')} (Score: {s.get('gatekeeper_score')}, Source: {s.get('source')})" for s in signals[:20]])

        prompt = f"""
        You are The Librarian, an autonomous intelligence strategist.
        Based on these recent high-relevance financial signals:
        
        {context}
        
        Identify 1-3 CRITICAL follow-up search missions for tomorrow.
        Focus on: 
        1. Verifying rumors (e.g., "Source X said Y, search for official filing").
        2. Finding specific numbers (e.g., "Deal announced, search for transaction value").
        3. Tracking immediate consequences (e.g., "CEO fired, search for interim CEO background").

        Output JSON ONLY:
        [
            {{
                "theme": "Short descriptive title",
                "keywords": ["specific keyword 1", "specific keyword 2"],
                "reason": "Why this needs immediate follow-up",
                "priority": "high",
                "depth": 10,
                "expires_at": "{ (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d') }" 
            }}
        ]
        """
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://investsense.ai",
            "X-Title": "Kazuha Librarian"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            
            # Handle potential markdown fencing
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            parsed = json.loads(content)
            
            # Robustness: Handle if LLM wrapped it in a dict key like "missions"
            if isinstance(parsed, dict):
                # Try to find a list value
                for key, value in parsed.items():
                    if isinstance(value, list):
                        return value
                # If no list found, maybe the dict IS the mission? (unlikely but possible)
                return [parsed]
            elif isinstance(parsed, list):
                return parsed
            else:
                logger.warning(f"Unexpected JSON format from Librarian: {type(parsed)}")
                return []
        except Exception as e:
            logger.error(f"Librarian AI Error: {e}")
            return []

    def save_mission(self, missions):
        """Appends missions to active_missions.yml and executes Hot Pursuit."""
        current_missions = {"active_missions": []}
        
        if os.path.exists(self.missions_file):
            try:
                with open(self.missions_file, 'r') as f:
                    current_missions = yaml.safe_load(f) or {"active_missions": []}
            except: pass
            
        existing_themes = {m.get('theme') for m in current_missions['active_missions']}
        
        new_added = []
        for m in missions:
            # Robustness: Skip malformed items
            if not isinstance(m, dict):
                logger.warning(f"Skipping invalid mission format: {m}")
                continue

            # Deduplication
            if m.get('theme') in existing_themes:
                continue
            
            m['source'] = 'cloud_librarian'
            m['created_at'] = datetime.now().strftime("%Y-%m-%d")
            m['expires_at'] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            
            current_missions['active_missions'].append(m)
            new_added.append(m)
            if m.get('theme'):
                existing_themes.add(m.get('theme'))
            
            # HOT PURSUIT: Execute immediate search
            if m.get('theme') and m.get('keywords'):
                self.hot_pursuit(m)

        if new_added:
            with open(self.missions_file, 'w') as f:
                yaml.dump(current_missions, f, sort_keys=False, allow_unicode=True)
            logger.info(f"📚 Librarian added {len(new_added)} new missions.")
            
    def hot_pursuit(self, mission):
        """Executes immediate search for a new mission."""
        logger.info(f"🔥 Hot Pursuit: {mission['theme']}...")
        results = []
        try:
            time.sleep(random.uniform(3, 7)) # Politeness
            
            # Search for the first keyword
            keyword = mission['keywords'][0] 
            
            with DDGS() as ddgs:
                ddg_results = ddgs.text(
                    keywords=keyword, 
                    region="wt-wt", 
                    safesearch="off", 
                    timelimit="d", # Past day
                    max_results=5
                )
                
                if ddg_results:
                    for res in ddg_results:
                        results.append({
                            "source": "Librarian_HotPursuit",
                            "keyword": keyword,
                            "title": res.get("title"),
                            "url": res.get("href"),
                            "content": res.get("body"),
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "category": "HotPursuit" 
                        })
        except Exception as e:
            logger.error(f"Hot Pursuit failed for {mission['theme']}: {e}")
            
        if results:
            self._save_hot_results(results)

    def _save_hot_results(self, results):
        if not results: return
        os.makedirs(PATHS["INCOMING"], exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PATHS['INCOMING']}/librarian_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} Hot Pursuit signals to Incoming.")

def main():
    librarian = ScoutLibrarian()
    signals = librarian.load_recent_signals()
    if signals:
        missions = librarian.generate_missions(signals)
        librarian.save_mission(missions)
    else:
        logger.info("No signals found for Librarian to analyze.")

if __name__ == "__main__":
    main()

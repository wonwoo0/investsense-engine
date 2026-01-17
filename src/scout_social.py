import time
import json
import logging
import requests
import yaml
import os
from datetime import datetime
import random
from src.config import REDDIT_USER_AGENT, PATHS, STRATEGY, REDDIT_USERNAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutSocial:
    def __init__(self):
        self.limit = STRATEGY.get("MAX_SCOUT_RESULTS", 5)

    def _get_target_keywords(self):
        keywords = set()
        # Portfolio
        try:
            with open(PATHS["PORTFOLIO"], 'r') as f:
                data = yaml.safe_load(f)
                if data and 'portfolio' in data:
                    for asset in data.get('portfolio', []):
                        keywords.update(asset.get('keywords', []))
        except: pass
        
        # Active Missions
        try:
            if os.path.exists(PATHS["MISSIONS"]):
                with open(PATHS["MISSIONS"], 'r') as f:
                    data = yaml.safe_load(f)
                    if data and 'active_missions' in data:
                        for m in data.get('active_missions', []):
                            keywords.update(m.get('keywords', []))
        except: pass
        
        return list(keywords)

    def fetch_reddit(self):
        keywords = self._get_target_keywords()
        logger.info(f"🛡️ Reddit Dorking for {len(keywords)} keywords...")
        
        results = []
        for keyword in keywords:
            # Self-healing loop: Attempt search with retries
            success = False
            for attempt in range(2):
                try:
                    logger.info(f"Reddit Dork: {keyword} (Attempt {attempt+1})...")
                    time.sleep(random.uniform(5, 10))
                    
                    query = f'site:reddit.com "{keyword}"'
                    from duckduckgo_search import DDGS
                    with DDGS() as ddgs:
                        ddg_results = ddgs.text(
                            keywords=query, 
                            region="wt-wt", 
                            safesearch="off", 
                            timelimit="d", 
                            max_results=self.limit
                        )
                        
                        if ddg_results:
                            for res in ddg_results:
                                results.append({
                                    "source": "Reddit_Dork",
                                    "keyword": keyword,
                                    "title": res.get("title"),
                                    "url": res.get("href"),
                                    "content": res.get("body"),
                                    "date": datetime.now().strftime("%Y-%m-%d")
                                })
                            break
                        else:
                            break
                except Exception as e:
                    logger.error(f"DDG Reddit Dork failed: {e}")
                    time.sleep(10)

        self._save_results(results)

    def _save_results(self, results):
        if not results: return
        os.makedirs(PATHS["INCOMING"], exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PATHS['INCOMING']}/social_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} social signals to Incoming.")

if __name__ == "__main__":
    scout = ScoutSocial()
    scout.fetch_reddit()

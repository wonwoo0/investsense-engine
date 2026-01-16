import time
import json
import logging
import requests
import yaml
import os
from datetime import datetime
from src.config import REDDIT_USER_AGENT, PATHS, STRATEGY, REDDIT_USERNAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutSocial:
    def __init__(self):
        # Professional User-Agent to avoid 403
        self.headers = {
            "User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KazuhaInvest/{REDDIT_USERNAME}"
        }
        self.search_url = "https://www.reddit.com/search.json"
        self.limit = STRATEGY.get("MAX_SCOUT_RESULTS", 5)
        self.circuit_breaker_threshold = 3  # Trip circuit after 3 consecutive 403s
        self.consecutive_403s = 0
        self.circuit_open = False

    def _get_target_keywords(self):
        keywords = set()
        # Portfolio
        try:
            with open(PATHS["PORTFOLIO"], 'r') as f:
                data = yaml.safe_load(f)
                for asset in data.get('portfolio', []):
                    keywords.update(asset.get('keywords', []))
        except: pass
        
        # Active Missions
        try:
            with open(PATHS["MISSIONS"], 'r') as f:
                data = yaml.safe_load(f)
                for m in data.get('active_missions', []):
                    keywords.update(m.get('keywords', []))
        except: pass
        
        return list(keywords)

    def fetch_reddit(self):
        keywords = self._get_target_keywords()
        logger.info(f"Scouting Reddit for keywords: {keywords}")
        
        results = []
        for i, keyword in enumerate(keywords):
            # Check circuit breaker
            if self.circuit_open:
                logger.warning(f"Reddit circuit breaker open. Skipping remaining {len(keywords) - i} keywords.")
                break
            
            time.sleep(2) # Politeness to avoid 403/429
            params = {"q": keyword, "sort": "new", "limit": 10}

            try:
                response = requests.get(self.search_url, headers=self.headers, params=params, timeout=20)
                if response.status_code == 200:
                    self.consecutive_403s = 0  # Reset on success
                    children = response.json().get("data", {}).get("children", [])
                    for post in children:
                        data = post.get("data", {})
                        results.append({
                            "source": "Reddit",
                            "keyword": keyword,
                            "title": data.get("title"),
                            "subreddit": data.get("subreddit"),
                            "url": f"https://www.reddit.com{data.get('permalink')}",
                            "content": data.get("selftext", "")[:300],
                            "score": data.get("score"),
                            "date": data.get("created_utc")
                        })
                elif response.status_code == 403:
                    self.consecutive_403s += 1
                    logger.warning(f"Reddit error 403 for '{keyword}' (consecutive: {self.consecutive_403s}/{self.circuit_breaker_threshold})")
                    
                    if self.consecutive_403s >= self.circuit_breaker_threshold:
                        self.circuit_open = True
                        logger.warning(f"Reddit circuit breaker tripped after {self.consecutive_403s} consecutive 403s. Stopping Reddit scout.")
                        break
                    
                    # Exponential backoff for 403s
                    wait_time = min(2 ** self.consecutive_403s, 32)  # Max 32 seconds
                    logger.info(f"Waiting {wait_time}s before next attempt...")
                    time.sleep(wait_time)
                elif response.status_code == 429:
                    logger.warning(f"Reddit Rate Limit hit. Backing off for 30s.")
                    time.sleep(30)
                else:
                    logger.warning(f"Reddit error {response.status_code} for '{keyword}'")
            except Exception as e:
                logger.error(f"Reddit failed for '{keyword}': {e}")

        self._save_results(results)

    def _save_results(self, results):
        if not results:
            logger.info("No social signals found today.")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PATHS['INCOMING']}/social_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} social signals.")

if __name__ == "__main__":
    scout = ScoutSocial()
    scout.fetch_reddit()

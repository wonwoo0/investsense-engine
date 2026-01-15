import time
import json
import logging
import requests
import re
from src.config import REDDIT_USER_AGENT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutSocial:
    def __init__(self):
        self.headers = {"User-Agent": REDDIT_USER_AGENT}
        self.portfolio_path = "data/portfolio.yml"
        self.output_dir = "data/Incoming"

    def _parse_portfolio_keywords(self):
        """Simple regex-based YAML parser to avoid dependencies."""
        keywords = []
        try:
            with open(self.portfolio_path, 'r') as f:
                content = f.read()
                matches = re.findall(r'keywords:\s*\[(.*?)\]', content)
                for match in matches:
                    keys = [k.strip().strip('"\'') for k in match.split(',')]
                    keywords.extend(keys)
        except Exception as e:
            logger.error(f"Failed to parse portfolio: {e}")
        return list(set(keywords))

    def fetch_reddit(self):
        keywords = self._parse_portfolio_keywords()
        logger.info(f"Scouting Reddit for keywords: {keywords}")
        
        results = []

        for keyword in keywords:
            # Rate limit compliance (Reddit is strict)
            time.sleep(2) 
            
            url = f"https://www.reddit.com/search.json"
            params = {
                "q": keyword,
                "sort": "new",
                "limit": 5,
                "restrict_sr": 0
            }

            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    children = data.get("data", {}).get("children", [])
                    
                    if children:
                        logger.info(f"Reddit: Found {len(children)} hits for '{keyword}'")
                        for post in children:
                            post_data = post.get("data", {})
                            results.append({
                                "source": "Reddit",
                                "keyword": keyword,
                                "title": post_data.get("title"),
                                "subreddit": post_data.get("subreddit"),
                                "url": f"https://www.reddit.com{post_data.get('permalink')}",
                                "content": post_data.get("selftext", "")[:300] + "...",
                                "score": post_data.get("score"),
                                "date": post_data.get("created_utc")
                            })
                elif response.status_code == 429:
                    logger.warning(f"Reddit Rate Limit hit for '{keyword}'. Sleeping 5s.")
                    time.sleep(5)
                else:
                    logger.warning(f"Reddit error {response.status_code} for '{keyword}'")
                    
            except Exception as e:
                logger.error(f"Failed to fetch Reddit for '{keyword}': {e}")

        self._save_results(results)

    def _save_results(self, results):
        if not results:
            logger.info("No social signals found today.")
            return

        timestamp = int(time.time())
        filename = f"{self.output_dir}/social_signals_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Saved {len(results)} signals to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

if __name__ == "__main__":
    scout = ScoutSocial()
    scout.fetch_reddit()

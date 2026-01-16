import os
import json
import time
import logging
import datetime
import requests
import yaml
from src.config import SAM_GOV_API_KEY, URLS, PATHS, STRATEGY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutGov:
    def __init__(self):
        self.api_key = SAM_GOV_API_KEY
        self.opps_url = URLS["SAM_OPPORTUNITIES"]
        self.awards_url = URLS["SAM_CONTRACTS"]
        self.us_spending_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        self.acq_gateway_url = "https://api.gsa.gov/acquisitiongateway/api/v4.0/listings"
        self.min_value = STRATEGY.get("MIN_CONTRACT_VALUE", 500000)
        self.sam_throttled = False
        self.sam_next_access_time = None
        self.cache = {}  # Simple in-memory cache for this run

    def _get_target_keywords(self):
        keywords = set()
        # Portfolio: Only use company names for Gov scouts, people names are usually noise here
        try:
            with open(PATHS["PORTFOLIO"], 'r') as f:
                data = yaml.safe_load(f)
                for asset in data.get('portfolio', []):
                    # We prioritize the asset Name over the Keywords list to save quota
                    keywords.add(asset.get('name'))
                    # Filter out obvious people names from sub-keywords if needed
                    # For now, let's keep it simple and just use the full list but deduplicated
                    keywords.update(asset.get('keywords', []))
        except: pass
        
        # Active Missions
        try:
            with open(PATHS["MISSIONS"], 'r') as f:
                data = yaml.safe_load(f)
                for m in data.get('active_missions', []):
                    keywords.add(m.get('theme'))
                    keywords.update(m.get('keywords', []))
        except: pass
        
        # REMOVE OBVIOUS NOISE (People typically don't get govt contracts)
        NOISE = ["Elon Musk", "Peter Beck", "Suresh Venkatesan"]
        clean_keywords = [k for k in keywords if k not in NOISE]
        
        return list(set(clean_keywords))

    def _request_with_backoff(self, url, params=None, method='GET', json_data=None, is_sam_api=False):
        """Helper to handle Rate Limiting (429) gracefully with caching and nextAccessTime awareness."""
        # Check if SAM.gov is already throttled
        if is_sam_api and self.sam_throttled:
            logger.info(f"SAM.gov throttled until {self.sam_next_access_time}. Skipping request.")
            return None
        
        # Check cache
        cache_key = f"{url}:{str(params)}:{str(json_data)}"
        if cache_key in self.cache:
            logger.debug(f"Returning cached response for {cache_key[:50]}...")
            return self.cache[cache_key]
        
        for attempt in range(3):
            try:
                if method == 'GET':
                    response = requests.get(url, params=params, timeout=30)
                else:
                    response = requests.post(url, json=json_data, timeout=30)
                
                if response.status_code == 200:
                    # Cache successful response
                    self.cache[cache_key] = response
                    return response
                elif response.status_code == 429:
                    # Parse 429 response for nextAccessTime
                    try:
                        error_data = response.json()
                        next_access = error_data.get("nextAccessTime")
                        if next_access and is_sam_api:
                            self.sam_throttled = True
                            self.sam_next_access_time = next_access
                            logger.warning(f"SAM.gov 429: Quota exceeded. Next access: {next_access}")
                            logger.info(f"Skipping remaining SAM.gov requests until {next_access}")
                            return None
                        logger.warning(f"Rate limited (429) for {url[:50]}...: {error_data}")
                    except:
                        logger.warning(f"Rate limited (429) for {url[:50]}...")
                    
                    wait_time = (2 ** attempt) * 5  # Exponential backoff: 5s, 10s, 20s
                    logger.info(f"Waiting {wait_time}s before retry (attempt {attempt + 1}/3)...")
                    time.sleep(wait_time)
                else:
                    logger.debug(f"Request failed with {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"Request error: {e}")
                break
        return None

    def fetch_us_spending(self, keywords, start_date, end_date):
        results = []
        for keyword in keywords:
            time.sleep(1) # Politeness
            payload = {
                "filters": {
                    "keywords": [keyword],
                    "time_period": [{"start_date": start_date, "end_date": end_date}],
                    "award_type_codes": ["A", "B", "C", "D"]
                },
                "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Action Date"],
                "limit": 5
            }
            resp = self._request_with_backoff(self.us_spending_url, method='POST', json_data=payload, is_sam_api=False)
            if resp:
                hits = resp.json().get("results", [])
                if hits:
                    logger.info(f"US Spending: Found {len(hits)} hits for '{keyword}'")
                for hit in hits:
                    if hit.get("Award Amount", 0) >= self.min_value:
                        results.append({
                            "source": "US Spending",
                            "keyword": keyword,
                            "title": f"Contract to {hit.get('Recipient Name')}",
                            "amount": hit.get("Award Amount"),
                            "date": hit.get("Action Date") or start_date,
                            "description": hit.get("Description", "")
                        })
        return results

    def fetch_opportunities(self):
        keywords = self._get_target_keywords()
        logger.info(f"Scouting SAM.gov for keywords: {keywords}")
        
        today = datetime.datetime.now()
        lookback = today - datetime.timedelta(days=30)
        posted_from = lookback.strftime("%m/%d/%Y")
        posted_to = today.strftime("%m/%d/%Y")

        all_results = []
        throttle_count = 0
        max_throttle_tolerance = 3  # Early exit after 3 consecutive throttles
        
        for keyword in keywords:
            # Early exit if SAM.gov is throttled
            if self.sam_throttled:
                logger.info(f"SAM.gov throttled. Skipping remaining {len(keywords) - len(all_results)} keywords.")
                break
            
            time.sleep(1)
            params = {
                "api_key": self.api_key,
                "postedFrom": posted_from,
                "postedTo": posted_to,
                "q": keyword,
                "active": "yes"
            }
            resp = self._request_with_backoff(self.opps_url, params=params, is_sam_api=True)
            if resp:
                throttle_count = 0  # Reset on success
                opps = resp.json().get("opportunitiesData", []) or resp.json().get("data", [])
                logger.info(f"Found {len(opps)} hits for '{keyword}'")
                for opp in opps:
                    all_results.append({
                        "source": "SAM.gov",
                        "keyword": keyword,
                        "title": opp.get("title"),
                        "agency": opp.get("organizationHierarchy", [{}])[0].get("name"),
                        "date": opp.get("postedDate"),
                        "url": opp.get("uiLink")
                    })
            else:
                throttle_count += 1
                if throttle_count >= max_throttle_tolerance:
                    logger.warning(f"SAM.gov consistently failing. Early exit after {throttle_count} failures.")
                    break

        # Only fetch contract awards if SAM.gov is not throttled
        if not self.sam_throttled:
            logger.info("Scouting SAM.gov Contract Awards...")
            # Contract awards logic would go here (not in the original code)
        else:
            logger.info("Skipping SAM.gov Contract Awards due to throttling.")

        # US Spending usually has higher quota or different limits
        logger.info(f"Scouting US Spending (No Key Required)...")
        all_results.extend(self.fetch_us_spending(keywords, lookback.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))

        # Acquisition Gateway
        logger.info("Scouting Acquisition Gateway...")
        # Acquisition gateway logic would go here (not in the original code)

        self._save_results(all_results)

    def _save_results(self, results):
        if not results:
            logger.info("No government signals found.")
            return
        timestamp = int(time.time())
        filename = f"{PATHS['INCOMING']}/gov_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} signals to {filename}")

if __name__ == "__main__":
    scout = ScoutGov()
    scout.fetch_opportunities()

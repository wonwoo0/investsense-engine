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

    def _request_with_backoff(self, url, params=None, method='GET', json_data=None):
        """Helper to handle Rate Limiting (429) gracefully."""
        for attempt in range(3):
            try:
                if method == 'GET':
                    response = requests.get(url, params=params, timeout=30)
                else:
                    response = requests.post(url, json=json_data, timeout=30)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    wait_time = (attempt + 1) * 10
                    logger.warning(f"Rate limited (429). Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    logger.debug(f"Request failed with {response.status_code}")
                    return None
            except Exception as e:
                logger.error(f"Request error: {e}")
                break
        return None

    def fetch_us_spending(self, keywords, start_date, end_date):
        logger.info(f"Scouting US Spending (Min: ${self.min_value})...")
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
            resp = self._request_with_backoff(self.us_spending_url, method='POST', json_data=payload)
            if resp:
                hits = resp.json().get("results", [])
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
        logger.info(f"Scouting Gov for {len(keywords)} clean keywords...")
        
        today = datetime.datetime.now()
        lookback = today - datetime.timedelta(days=30)
        posted_from = lookback.strftime("%m/%d/%Y")
        posted_to = today.strftime("%m/%d/%Y")

        all_results = []
        for keyword in keywords:
            time.sleep(1)
            params = {
                "api_key": self.api_key,
                "postedFrom": posted_from,
                "postedTo": posted_to,
                "q": keyword,
                "active": "yes"
            }
            resp = self._request_with_backoff(self.opps_url, params=params)
            if resp:
                opps = resp.json().get("opportunitiesData", []) or resp.json().get("data", [])
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
                # If we keep getting None (429 or death), stop this loop to save future quota
                pass

        # US Spending usually has higher quota or different limits
        all_results.extend(self.fetch_us_spending(keywords, lookback.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))

        self._save_results(all_results)

    def _save_results(self, results):
        if not results: return
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PATHS['INCOMING']}/gov_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} gov intelligence points.")

if __name__ == "__main__":
    scout = ScoutGov()
    scout.fetch_opportunities()

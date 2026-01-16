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

    def fetch_us_spending(self, keywords, start_date, end_date):
        logger.info(f"Scouting US Spending (Min: ${self.min_value})...")
        results = []
        for keyword in keywords:
            time.sleep(0.5)
            payload = {
                "filters": {
                    "keywords": [keyword],
                    "time_period": [{"start_date": start_date, "end_date": end_date}],
                    "award_type_codes": ["A", "B", "C", "D"]
                },
                "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Action Date"],
                "limit": 10
            }
            try:
                response = requests.post(self.us_spending_url, json=payload, timeout=30)
                if response.status_code == 200:
                    hits = response.json().get("results", [])
                    for hit in hits:
                        if hit.get("Award Amount", 0) >= self.min_value:
                            action_date = hit.get("Action Date")
                            if not action_date:
                                action_date = start_date
                                
                            results.append({
                                "source": "US Spending",
                                "keyword": keyword,
                                "title": f"Contract to {hit.get('Recipient Name')}",
                                "amount": hit.get("Award Amount"),
                                "date": action_date,
                                "description": hit.get("Description", "")
                            })
            except Exception as e:
                logger.error(f"US Spending failed: {e}")
        return results

    def fetch_acq_gateway(self, keywords):
        logger.info("Scouting Acquisition Gateway...")
        results = []
        headers = {"x-api-key": self.api_key}
        for keyword in keywords:
            time.sleep(0.5)
            try:
                response = requests.get(self.acq_gateway_url, headers=headers, params={"search": keyword}, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        for item in data:
                            results.append({
                                "source": "AcqGateway",
                                "keyword": keyword,
                                "title": item.get("title"),
                                "summary": item.get("summary"),
                                "type": item.get("type")
                            })
            except: pass
        return results

    def fetch_contract_awards(self, keywords):
        logger.info("Scouting SAM.gov Contract Awards...")
        results = []
        for keyword in keywords:
            time.sleep(0.5)
            try:
                response = requests.get(self.awards_url, params={"api_key": self.api_key, "q": keyword, "limit": 10}, timeout=30)
                if response.status_code == 200:
                    awards = response.json().get("awards", []) or response.json().get("results", [])
                    if isinstance(awards, list):
                        for award in awards:
                            results.append({
                                "source": "SAM.gov Awards",
                                "keyword": keyword,
                                "title": f"Award {award.get('piid')}",
                                "awardee": award.get("awardee", {}).get("name"),
                                "amount": award.get("ultimateContractValue"),
                                "date": award.get("dateSigned")
                            })
            except: pass
        return results

    def fetch_opportunities(self):
        keywords = self._get_target_keywords()
        today = datetime.datetime.now()
        lookback = today - datetime.timedelta(days=30)
        posted_from = lookback.strftime("%m/%d/%Y")
        posted_to = today.strftime("%m/%d/%Y")

        all_results = []
        # 1. Opportunities
        for keyword in keywords:
            time.sleep(0.5)
            try:
                response = requests.get(self.opps_url, params={"api_key": self.api_key, "postedFrom": posted_from, "postedTo": posted_to, "q": keyword, "active": "yes"}, timeout=30)
                if response.status_code == 200:
                    opps = response.json().get("opportunitiesData", []) or response.json().get("data", [])
                    for opp in opps:
                        all_results.append({"source": "SAM.gov", "keyword": keyword, "title": opp.get("title"), "agency": opp.get("organizationHierarchy", [{}])[0].get("name"), "date": opp.get("postedDate"), "url": opp.get("uiLink")})
            except: pass

        # 2. Add Awards, Spending, Gateway
        all_results.extend(self.fetch_contract_awards(keywords))
        all_results.extend(self.fetch_us_spending(keywords, lookback.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))
        all_results.extend(self.fetch_acq_gateway(keywords))

        self._save_results(all_results)

    def _save_results(self, results):
        if not results: return
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{PATHS['INCOMING']}/gov_signals_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved {len(results)} gov signals.")

if __name__ == "__main__":
    scout = ScoutGov()
    scout.fetch_opportunities()

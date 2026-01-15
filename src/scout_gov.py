import os
import json
import time
import logging
import datetime
import requests
import re
from src.config import SAM_GOV_API_KEY, URLS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutGov:
    def __init__(self):
        self.api_key = SAM_GOV_API_KEY
        self.opps_url = URLS["SAM_OPPORTUNITIES"]
        self.awards_url = URLS["SAM_CONTRACTS"]
        self.us_spending_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
        self.acq_gateway_url = "https://api.gsa.gov/acquisitiongateway/api/v4.0/listings"
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

    def fetch_us_spending(self, keywords, posted_from, posted_to):
        logger.info("Scouting US Spending (No Key Required)...")
        results = []
        
        # Format dates for US Spending (YYYY-MM-DD)
        try:
            start_date = datetime.datetime.strptime(posted_from, "%m/%d/%Y").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(posted_to, "%m/%d/%Y").strftime("%Y-%m-%d")
        except:
            start_date = posted_from
            end_date = posted_to

        for keyword in keywords:
            time.sleep(0.5)
            payload = {
                "filters": {
                    "keywords": [keyword],
                    "time_period": [{"start_date": start_date, "end_date": end_date}],
                    "award_type_codes": ["A", "B", "C", "D"] # Contracts
                },
                "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Action Date"],
                "limit": 10
            }
            
            try:
                response = requests.post(self.us_spending_url, json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    hits = data.get("results", [])
                    if hits:
                        logger.info(f"US Spending: Found {len(hits)} hits for '{keyword}'")
                        for hit in hits:
                            results.append({
                                "source": "US Spending",
                                "keyword": keyword,
                                "title": f"Contract to {hit.get('Recipient Name')}",
                                "amount": hit.get("Award Amount"),
                                "date": hit.get("Action Date"),
                                "description": hit.get("Description", "")
                            })
                else:
                    logger.warning(f"US Spending error: {response.text}")
            except Exception as e:
                logger.error(f"US Spending failed for '{keyword}': {e}")
                
        return results

    def fetch_acq_gateway(self, keywords):
        logger.info("Scouting Acquisition Gateway...")
        results = []
        headers = {"x-api-key": self.api_key}

        for keyword in keywords:
            time.sleep(1)
            params = {"search": keyword}
            try:
                response = requests.get(self.acq_gateway_url, headers=headers, params=params, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and data:
                        logger.info(f"Acq Gateway: Found {len(data)} hits for '{keyword}'")
                        for item in data:
                            results.append({
                                "source": "AcqGateway",
                                "keyword": keyword,
                                "title": item.get("title"),
                                "summary": item.get("summary"),
                                "pid": item.get("pid"),
                                "type": item.get("type")
                            })
                else:
                    logger.debug(f"Acq Gateway skip: {response.status_code}")
            except Exception as e:
                logger.debug(f"Acq Gateway failed: {e}")
        return results

    def fetch_contract_awards(self, keywords, posted_from, posted_to):
        logger.info("Scouting SAM.gov Contract Awards...")
        results = []
        # awards endpoint uses 'api_key' query param, not header (per RAW_US_GOV_API.md)
        
        for keyword in keywords:
            time.sleep(1)
            params = {
                "api_key": self.api_key,
                "q": keyword,
                "limit": 10
            }
            try:
                response = requests.get(self.awards_url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    # Per doc: "It returns ten records per page in the JSON format by default"
                    awards = data if isinstance(data, list) else data.get("awards", data.get("results", []))
                    
                    if awards:
                        logger.info(f"SAM Awards: Found {len(awards)} hits for '{keyword}'")
                        for award in awards:
                            results.append({
                                "source": "SAM.gov Awards",
                                "keyword": keyword,
                                "title": f"Award {award.get('piid')}",
                                "awardee": award.get("awardee", {}).get("name"),
                                "amount": award.get("ultimateContractValue"),
                                "date": award.get("dateSigned"),
                                "description": award.get("description", "")
                            })
                else:
                    logger.debug(f"SAM Awards skip: {response.status_code} {response.text[:100]}")
            except Exception as e:
                logger.debug(f"SAM Awards failed: {e}")
        return results

    def fetch_opportunities(self):
        keywords = self._parse_portfolio_keywords()
        logger.info(f"Scouting SAM.gov for keywords: {keywords}")
        
        today = datetime.datetime.now()
        # Look back 30 days to ensure data for testing (User requirement: ensure results)
        lookback = today - datetime.timedelta(days=30) 
        
        posted_from = lookback.strftime("%m/%d/%Y")
        posted_to = today.strftime("%m/%d/%Y")

        results = []

        for keyword in keywords:
            # Rate limit compliance
            time.sleep(1)  
            
            # Per RAW_US_GOV_API.md: api_key is a request parameter, not header
            params = {
                "api_key": self.api_key,
                "postedFrom": posted_from,
                "postedTo": posted_to,
                "limit": 10,
                "q": keyword,
                "active": "yes"
            }

            try:
                response = requests.get(self.opps_url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    opportunities = data.get("opportunitiesData", [])
                    if not opportunities:
                         opportunities = data.get("data", [])
                    
                    if opportunities:
                        logger.info(f"Found {len(opportunities)} hits for '{keyword}'")
                        for opp in opportunities:
                            results.append({
                                "source": "SAM.gov",
                                "keyword": keyword,
                                "title": opp.get("title"),
                                "solicitationNumber": opp.get("solicitationNumber"),
                                "agency": opp.get("organizationHierarchy", [{}])[0].get("name"),
                                "postedDate": opp.get("postedDate"),
                                "url": opp.get("uiLink"),
                                "description": opp.get("description", "")[:200] + "..."
                            })
                else:
                    logger.warning(f"SAM.gov error {response.status_code} for '{keyword}': {response.text}")
            except Exception as e:
                logger.error(f"Failed to fetch for '{keyword}': {e}")

        awards_results = self.fetch_contract_awards(keywords, posted_from, posted_to)
        results.extend(awards_results)

        us_spending_results = self.fetch_us_spending(keywords, posted_from, posted_to)
        results.extend(us_spending_results)

        acq_gateway_results = self.fetch_acq_gateway(keywords)
        results.extend(acq_gateway_results)

        self._save_results(results)

    def _save_results(self, results):
        if not results:
            logger.info("No government opportunities found today.")
            return

        timestamp = int(time.time())
        filename = f"{self.output_dir}/gov_signals_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Saved {len(results)} signals to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

if __name__ == "__main__":
    scout = ScoutGov()
    scout.fetch_opportunities()

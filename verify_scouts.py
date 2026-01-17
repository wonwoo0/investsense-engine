import os
import json
import time
from unittest.mock import patch, MagicMock

# 1. TEST REDDIT DORK logic
print("🧪 Testing Reddit Dork Logic...")
from src.scout_social import ScoutSocial

scout_s = ScoutSocial()
with patch("duckduckgo_search.DDGS.text") as mock_ddg:
    mock_ddg.return_value = [
        {"title": "Test Reddit Post", "href": "https://reddit.com/r/test", "body": "Test body"}
    ]
    scout_s._get_target_keywords = MagicMock(return_value=["RKLB"])
    scout_s.fetch_reddit()

# Check Incoming
incoming_files = os.listdir("data/Incoming")
social_files = [f for f in incoming_files if "social_signals" in f]
if social_files:
    print(f"✅ Reddit Logic: PASS (Found {len(social_files)} files)")
    # Cleanup
    for f in social_files: os.remove(f"data/Incoming/{f}")
else:
    print("❌ Reddit Logic: FAIL")

# 2. TEST GOV HISTORY logic
print("\n🧪 Testing Gov History Logic (Self-Healing)...")
from src.scout_gov import ScoutGov

scout_g = ScoutGov()
scout_g._get_target_keywords = MagicMock(return_value=["RKLB"])
# Mock SAM.gov response
mock_opp = {
    "noticeId": "GOV123",
    "title": "Satellite Build",
    "postedDate": "2026-01-01",
    "uiLink": "http://sam.gov/123"
}

with patch("src.scout_gov.ScoutGov._request_with_backoff") as mock_req:
    # First call: Returns 1 result
    mock_req.return_value.json.return_value = {"opportunitiesData": [mock_opp]}
    mock_req.return_value.status_code = 200
    
    # Run 1
    scout_g.fetch_opportunities()
    
    # Check history
    if "GOV123" in scout_g.history:
        print("✅ Run 1: Notice added to history.")
    else:
        print("❌ Run 1: Notice NOT in history.")

    # Run 2 (Same data)
    all_incoming_before = len(os.listdir("data/Incoming"))
    scout_g.fetch_opportunities()
    all_incoming_after = len(os.listdir("data/Incoming"))
    
    # It should not have saved a new file because all_results was empty (already in history)
    # WAIT: _save_results only saves if results exist.
    if all_incoming_after == all_incoming_before:
         print("✅ Run 2: Correctly skipped duplicate results (Smart History).")
    else:
         print("❌ Run 2: Saved duplicate results!")

# Cleanup gov_history for next real run if needed
if os.path.exists("data/Knowledge/gov_history.json"):
    os.remove("data/Knowledge/gov_history.json")

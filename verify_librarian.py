import os
import json
import yaml
import shutil
import time
from unittest.mock import patch, MagicMock
from datetime import datetime

# 1. SETUP ENVIRONMENT
if not os.path.exists("data/Processed"):
    os.makedirs("data/Processed")
if not os.path.exists("data/Incoming"):
    os.makedirs("data/Incoming")
    
# Mock Processed Signal
mock_signal = [{
    "title": "SpaceX Starship Launch Success",
    "gatekeeper_score": 10,
    "source": "SpaceNews"
}]
with open(f"data/Processed/test_signal_{int(time.time())}.json", "w") as f:
    json.dump(mock_signal, f)

# 2. TEST LIBRARIAN (Mocked AI & Search)
print("🧪 Testing Librarian (Cloud Reactive)...")
from src.scout_librarian import ScoutLibrarian

librarian = ScoutLibrarian()

# Mock OpenRouter Response
mock_missions = [{
    "theme": "Starship Impact Analysis",
    "keywords": ["Starship payload capacity", "Starship cost per kg"],
    "reason": "Verify impact on RKLB",
    "priority": "high",
    "depth": 10
}]
# Mock DDG Response
mock_search_results = [{
    "title": "Starship is cheap",
    "href": "http://spacex.com",
    "body": "It costs $10/kg."
}]

with patch("src.scout_librarian.ScoutLibrarian.generate_missions", return_value=mock_missions):
    with patch("duckduckgo_search.DDGS.text", return_value=mock_search_results):
        librarian.load_recent_signals() # Should load our test file
        librarian.save_mission(mock_missions)

# Verify Active Missions Update
with open("data/active_missions.yml", "r") as f:
    missions_data = yaml.safe_load(f)
    themes = [m['theme'] for m in missions_data['active_missions']]
    if "Starship Impact Analysis" in themes:
        print("✅ Librarian: Mission added to active_missions.yml")
    else:
        print("❌ Librarian: Mission NOT added!")

# Verify Hot Pursuit (Incoming file created)
incoming_files = os.listdir("data/Incoming")
librarian_files = [f for f in incoming_files if "librarian_signals" in f]
if librarian_files:
    print(f"✅ Librarian: Hot Pursuit executed (Found {len(librarian_files)} files)")
    # Cleanup Incoming
    for f in librarian_files: os.remove(f"data/Incoming/{f}")
else:
    print("❌ Librarian: Hot Pursuit failed!")


# 3. TEST ARCHIVER
print("\n🧪 Testing Archiver...")
from src.utils.archiver import Archiver

# Create an 'old' file
old_file = "data/Processed/old_test.json"
with open(old_file, "w") as f:
    json.dump({"old": True}, f)
# Set mtime to 31 days ago
old_time = time.time() - (31 * 86400)
os.utime(old_file, (old_time, old_time))

archiver = Archiver(retention_days=30)
archiver.run()

# Verify Move
# Check if gone from Processed
if not os.path.exists(old_file):
    print("✅ Archiver: Old file removed from Processed.")
else:
    print("❌ Archiver: Old file still in Processed!")

# Check if exists in Archive
today = datetime.now()
target_dir = f"data/Archive/{datetime.fromtimestamp(old_time).strftime('%Y-%m')}"
if os.path.exists(os.path.join(target_dir, "old_test.json")):
    print(f"✅ Archiver: Old file moved to {target_dir}")
else:
    print("❌ Archiver: Old file NOT found in Archive!")

# Cleanup
if os.path.exists("data/Processed/test_signal.json"):
    os.remove("data/Processed/test_signal.json")
# Clean Processed
for f in os.listdir("data/Processed"): 
    if f.startswith("test_signal"): os.remove(f"data/Processed/{f}")
# Clean Archiver test output
if os.path.exists(target_dir):
    shutil.rmtree(target_dir) # Be careful, only remove the test month folder

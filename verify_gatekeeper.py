import json
import os
import time
from dotenv import load_dotenv

# Force load real environment
load_dotenv(override=True)

from src.scout_gatekeeper import gatekeep_item

# Mock Input Data (One Garbage, One Gold)
MOCK_INPUT = [
    {
        "title": "Top 10 Ways to Cook Uranium - Tutorial",
        "summary": "This is a youtube video tutorial on how to cook uranium. Subscribe for more! This is just a test for garbage filtering.",
        "source": "YouTube"
    },
    {
        "title": "Rocket Lab Wins $515M Contract",
        "summary": "Rocket Lab USA has been awarded a $515 million contract by the Space Development Agency to build 18 satellites. This is a significant key fact.",
        "source": "SpaceNews"
    }
]

# Write Mock Input
if not os.path.exists("data/Incoming"):
    os.makedirs("data/Incoming")
    
with open("data/Incoming/test_input.json", "w") as f:
    json.dump(MOCK_INPUT, f)

print(f"🛡️ Running Gatekeeper with REAL OpenRouter (Nemotron)...")
kept_items = []

for item in MOCK_INPUT:
    print(f"Testing: {item['title']}...")
    keep, processed = gatekeep_item(item)
    if keep:
        print(f"✅ KEPT (Score: {processed.get('gatekeeper_score')}, Reason: {processed.get('gatekeeper_reason')})")
        kept_items.append(processed)
    else:
        print(f"🗑️ DISCARDED")
    time.sleep(2) # Politeness for free model

print("\n🔍 Verification Results:")

# 1. Check Filtering
if any(item['title'] == "Rocket Lab Wins $515M Contract" for item in kept_items):
    print("✅ Logic Check: Gold kept.")
else:
    print("❌ Logic Check: Gold discarded!")

# 2. Check Memory
try:
    with open("data/Knowledge/active_context.md", "r") as f:
        memory_content = f.read()
    if "Rocket Lab" in memory_content:
        print("✅ Memory Update: PASS")
    else:
        print("❌ Memory Update: Fact not found.")
except Exception as e:
    print(f"❌ Memory Update: Error reading file: {e}")

# Cleanup
if os.path.exists("data/Incoming/test_input.json"):
    os.remove("data/Incoming/test_input.json")

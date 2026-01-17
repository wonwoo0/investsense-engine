import google.generativeai as genai
from src.config import GEMINI_API_KEY, PATHS
import logging
import json
import yaml
import os
import asyncio
import argparse
from datetime import datetime
from src.notifier import send_telegram_message

# Configure Gemini for Local Brain
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
PROCESSED_DIR = "data/Processed"
MISSIONS_FILE = "data/active_missions.yml"

def load_data():
    """Search 2.1: Loads Processed signals (Cleaner than Incoming)."""
    if not os.path.exists(PROCESSED_DIR):
        logger.warning(f"No Processed directory found at {PROCESSED_DIR}")
        return [], None

    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    news_data = []
    
    for f in files:
        path = os.path.join(PROCESSED_DIR, f)
        try:
            with open(path, 'r') as file:
                content = json.load(file)
                if isinstance(content, list):
                    news_data.extend(content)
        except Exception as e:
            logger.error(f"Error reading {f}: {e}")

    # Load Active Context (Memory)
    memory_path = "data/Knowledge/active_context.md"
    memory_content = ""
    if os.path.exists(memory_path):
        with open(memory_path, 'r') as f:
            memory_content = f.read()

    # Load Portfolio
    with open(PATHS["PORTFOLIO"], 'r') as f:
        portfolio_data = yaml.safe_load(f)

    return news_data, portfolio_data, memory_content

def generate_strategic_missions(news_data, memory_content):
    """Phase 5: Local Brain Generates Strategic Missions."""
    if not news_data or not GEMINI_API_KEY:
        logger.warning("Skipping Strategic Mission Gen (No data or No Key).")
        return

    logger.info("🧠 Brain is thinking about Strategic Missions...")
    
    # Context Synthesis
    signals_summary = "\n".join([f"- {s.get('title')} ({s.get('source')})" for s in news_data[:30]])
    
    prompt = f"""
    You are the Strategic Brain of Kazuha Invest.
    
    Recent Signals:
    {signals_summary}
    
    Long-term Memory:
    {memory_content}
    
    Analyze the trends over the last 7 days.
    Identify 1-3 STRATEGIC, LONG-TERM search missions to add to our tracking list.
    Rules:
    1. Do NOT duplicate existing active missions.
    2. Focus on "What comes next?" (e.g., Regulatory approval after a tech breakthrough).
    3. Expiry should be 14-30 days.

    Output JSON ONLY:
    [
        {{
            "theme": "Title",
            "keywords": ["k1", "k2"],
            "reason": "Strategic rationale",
            "priority": "medium",
            "depth": 20,
            "expires_at": "YYYY-MM-DD"
        }}
    ]
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest") # Use a capable model
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        missions = json.loads(response.text)
        
        if missions:
            _append_missions(missions)
            
    except Exception as e:
        logger.error(f"Strategic Mission Gen Failed: {e}")

def _append_missions(missions):
    """Directly appends to active_missions.yml with deduplication."""
    current_missions = {"active_missions": []}
    
    if os.path.exists(MISSIONS_FILE):
        try:
            with open(MISSIONS_FILE, 'r') as f:
                current_missions = yaml.safe_load(f) or {"active_missions": []}
        except: pass
        
    existing_themes = {m.get('theme') for m in current_missions.get('active_missions', [])}
    
    added_count = 0
    for m in missions:
        if m['theme'] in existing_themes:
            continue
            
        m['source'] = 'local_brain'
        m['created_at'] = datetime.now().strftime("%Y-%m-%d")
        
        current_missions['active_missions'].append(m)
        existing_themes.add(m['theme'])
        added_count += 1
        
    if added_count > 0:
        with open(MISSIONS_FILE, 'w') as f:
            yaml.dump(current_missions, f, sort_keys=False, allow_unicode=True)
        logger.info(f"🧠 Added {added_count} Strategic Missions to active_missions.yml")
    else:
        logger.info("🧠 No new strategic missions added (Duplicates or Empty).")

def prepare_context_file(news_data, portfolio_data, memory_content):
    date_str = datetime.now().strftime("%Y%m%d")
    report_dir = os.path.join(PATHS["REPORTS"], date_str)
    os.makedirs(report_dir, exist_ok=True)
    
    context_str = f"""# Reasoning Context ({date_str})

## Portfolio Context
```yaml
{yaml.dump(portfolio_data)}
```

## Active Memory (Long-term)
{memory_content}

## News Intelligence (Fresh Signals)
```json
{json.dumps(news_data, indent=2, ensure_ascii=False)}
```
"""
    
    context_path = os.path.join(report_dir, "Context_Input.md")
    with open(context_path, 'w') as f:
        f.write(context_str)
    
    logger.info(f"Context saved to: {context_path}")
    return context_path

async def send_source_summary(news_data):
    if not news_data:
        # await send_telegram_message("⚠️ 今日搜尋未發現任何新資料。")
        pass
        return

    sources = set()
    for item in news_data:
        source = item.get("source", "Unknown")
        sources.add(source)
    
    source_list = "\n".join([f"✅ {s}" for s in sorted(sources)])
    message = f"🚀 *Kazuha 搜查完成 (Search 2.1)*\n\n有效來源：\n{source_list}\n\nLibrarian 已執行 Hot Pursuit。\nBrain 已生成策略任務。"
    await send_telegram_message(message)

def main():
    news_data, portfolio_data, memory = load_data()
    
    if news_data:
        prepare_context_file(news_data, portfolio_data, memory)
        asyncio.run(send_source_summary(news_data))
        
        # Phase 5: Strategic Mission Gen
        generate_strategic_missions(news_data, memory)
        
        # Note: Archive incoming is now handled by src/utils/archiver.py separately
    else:
        logger.error("No data available to process.")

if __name__ == "__main__":
    main()

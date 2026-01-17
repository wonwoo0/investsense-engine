import os
import json
import logging
import time
import requests
from datetime import datetime
from src.config import OPENROUTER_API_KEY, PATHS

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "nvidia/nemotron-3-nano-30b-a3b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
INPUT_DIR = "data/Incoming"
PROCESSED_DIR = "data/Processed"
MEMORY_FILE = "data/Knowledge/active_context.md"

def load_json_files(directory):
    if not os.path.exists(directory):
        return []
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    data = []
    for f in files:
        path = os.path.join(directory, f)
        try:
            with open(path, 'r') as file:
                content = json.load(file)
                if isinstance(content, list):
                    for item in content:
                        item['origin_file'] = f
                        data.append(item)
        except Exception as e:
            logger.error(f"Failed to load {f}: {e}")
    return data

def update_memory(fact):
    """Appends a high-importance fact to the long-term memory file."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        entry = f"\n- [{timestamp}] {fact}"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        
        with open(MEMORY_FILE, "a") as f:
            f.write(entry)
        
        logger.info(f"💾 Memory Updated: {fact[:50]}...")
    except Exception as e:
        logger.error(f"Failed to update memory: {e}")

def gatekeep_item(item):
    """
    Uses OpenRouter (NVIDIA Nemotron) to score relevance and identify key facts.
    Returns: (keep_boolean, modified_item)
    """
    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY not found. Skipping filtering.")
        return True, item

    title = item.get('title', 'No Title')
    summary = item.get('summary', '') or item.get('content', '') or item.get('description', '')
    source = item.get('source', 'Unknown')
    
    if len(summary) < 20: 
        return False, None

    prompt = f"""
    Analyze this financial news item.
    
    Title: {title}
    Source: {source}
    Content: {summary[:1000]}

    Task:
    1. Score relevance (0-10) to themes: Space Tech, AI Hardware, Nuclear Energy, Autonomous Vehicles.
    2. Identify if this is a "Key Fact" (e.g., Contract Award >$10M, Regulatory Approval, Factory Opening, CEO Change).
    3. Filter out: Tutorials, generic discussions, old news.

    Output EXACT JSON format:
    {{
        "relevance_score": <int>,
        "is_key_fact": <bool>,
        "key_fact_summary": "<string or null>",
        "reason": "<short explanation>"
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://investsense.ai", # Optional for OpenRouter
        "X-Title": "Kazuha Gatekeeper"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        content = data['choices'][0]['message']['content']
        result = json.loads(content)
        
        score = result.get('relevance_score', 0)
        is_key_fact = result.get('is_key_fact', False)
        
        if score >= 5 or is_key_fact:
            item['gatekeeper_score'] = score
            item['gatekeeper_reason'] = result.get('reason')
            
            if is_key_fact:
                item['is_key_fact'] = True
                fact_summary = result.get('key_fact_summary') or title
                update_memory(f"[{source}] {fact_summary}")
                
            return True, item
        else:
            logger.info(f"🗑️ Discarded (Score {score}): {title[:50]}...")
            return False, None
            
    except Exception as e:
        logger.error(f"Gatekeeper API Error: {e}. Keeping item safe.")
        return True, item

def main():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)
        
    logger.info(f"🛡️ Gatekeeper (OpenRouter - {MODEL_NAME}) Started...")
    
    raw_items = load_json_files(INPUT_DIR)
    logger.info(f"Loaded {len(raw_items)} raw items.")
    
    clean_items = []
    
    for item in raw_items:
        keep, processed_item = gatekeep_item(item)
        if keep and processed_item:
            clean_items.append(processed_item)
        time.sleep(0.5) # Slight sleep for rate efficiency
            
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(PROCESSED_DIR, f"clean_signals_{timestamp}.json")
    
    with open(output_path, 'w') as f:
        json.dump(clean_items, f, indent=2)
        
    logger.info(f"✅ Gatekeeper Finished. {len(clean_items)}/{len(raw_items)} kept. Saved to {output_path}")

if __name__ == "__main__":
    main()

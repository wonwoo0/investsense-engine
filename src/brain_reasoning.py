import sys
import os

# Add project root to path BEFORE importing local modules
sys.path.append(os.getcwd())

import json
import yaml
import logging
import argparse
import asyncio
import shutil
from datetime import datetime
from src.notifier import send_telegram_message
from src.config import PATHS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(signals_file=None):
    # 1. Load Signals (Latest consolidated file)
    incoming_dir = PATHS["INCOMING"]
    if not signals_file:
        files = [f for f in os.listdir(incoming_dir) if f.startswith('consolidated_')]
        if not files:
            # Fallback to any json
            files = [f for f in os.listdir(incoming_dir) if f.endswith('.json')]
        
        if not files:
            logger.warning(f"No signal files found in {incoming_dir}")
            return None, None
            
        files.sort(key=lambda x: os.path.getmtime(os.path.join(incoming_dir, x)))
        signals_file = os.path.join(incoming_dir, files[-1])
        logger.info(f"Auto-selected file for analysis: {signals_file}")

    if not os.path.exists(signals_file):
        logger.warning(f"No signals file found at {signals_file}")
        return None, None

    news_data = []
    try:
        with open(signals_file, 'r') as f:
            news_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse input file: {e}")
        return None, None

    # 2. Load Portfolio
    with open(PATHS["PORTFOLIO"], 'r') as f:
        portfolio_data = yaml.safe_load(f)

    return news_data, portfolio_data

def archive_incoming():
    """Moves processed files from Incoming to Archive to prevent stale data in next run."""
    incoming_dir = PATHS["INCOMING"]
    archive_dir = PATHS["ARCHIVE"]
    os.makedirs(archive_dir, exist_ok=True)
    
    files = [f for f in os.listdir(incoming_dir)]
    if not files:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sub_archive = os.path.join(archive_dir, timestamp)
    os.makedirs(sub_archive, exist_ok=True)
    
    for f in files:
        src = os.path.join(incoming_dir, f)
        dst = os.path.join(sub_archive, f)
        try:
            shutil.move(src, dst)
        except Exception as e:
            logger.error(f"Failed to archive {f}: {e}")
    
    logger.info(f"Processed signals archived to {sub_archive}")

def prepare_context_file(news_data, portfolio_data):
    date_str = datetime.now().strftime("%Y%m%d")
    report_dir = os.path.join(PATHS["REPORTS"], date_str)
    os.makedirs(report_dir, exist_ok=True)
    
    context_str = f"""# Reasoning Context ({date_str})

## Portfolio Context
```yaml
{yaml.dump(portfolio_data)}
```

## News Intelligence (Fresh Signals)
```json
{json.dumps(news_data, indent=2, ensure_ascii=False)}
```
"""
    
    context_path = os.path.join(report_dir, "Context_Input.md")
    with open(context_path, 'w') as f:
        f.write(context_str)
    
    logger.info(f"Context saved to: {context_path}")
    print(f"\n[Ready] Context prepared at: {context_path}")
    return context_path

async def send_source_summary(news_data):
    if not news_data:
        await send_telegram_message("⚠️ 今日搜尋未發現任何新資料。已整理存檔。")
        return

    sources = set()
    for item in news_data:
        source = item.get("source", "Unknown")
        sources.add(source)
    
    source_list = "\n".join([f"✅ {s}" for s in sorted(sources)])
    message = f"🚀 *Kazuha 搜查完成*\n\n有效來源：\n{source_list}\n\n報告及上下文已準備好。請執行 V7 Flow 進行手動分析。"
    await send_telegram_message(message)

def main():
    parser = argparse.ArgumentParser(description='InvestSense Brain Reasoning')
    parser.add_argument('input_file', nargs='?', help='Path to specific signal file')
    args = parser.parse_args()

    news_data, portfolio_data = load_data(args.input_file)
    if news_data and portfolio_data:
        prepare_context_file(news_data, portfolio_data)
        asyncio.run(send_source_summary(news_data))
        # Archive files so next run doesn't include today's noise
        archive_incoming()
    else:
        logger.error("No data available to process.")

if __name__ == "__main__":
    main()

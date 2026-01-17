import os
import sys
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Search2.1_Controller")

# Scripts to run in order
SCRIPTS = [
    # 1. SCOUTS (Search)
    {"name": "Scout Hunter (Web)", "cmd": ["python3", "src/scout_hunter.py"], "critical": False},
    {"name": "Scout Social (Reddit Dork)", "cmd": ["python3", "src/scout_social.py"], "critical": False},
    {"name": "Scout Gov (History)", "cmd": ["python3", "src/scout_gov.py"], "critical": False},
    
    # 2. GATEKEEPER (Filter)
    {"name": "Gatekeeper (OpenRouter)", "cmd": ["python3", "src/scout_gatekeeper.py"], "critical": True},
    
    # 3. LIBRARIAN (React & Hot Pursuit)
    {"name": "Librarian (Hot Pursuit)", "cmd": ["python3", "src/scout_librarian.py"], "critical": True},
    
    # 3.5 RE-RUN GATEKEEPER? 
    # Logic: Librarian puts stuff in Incoming, so next run catches it. 
    # But for this "Full Run", maybe we want to process it now?
    # Let's run Gatekeeper again to process "Hot Pursuit" results immediately.
    {"name": "Gatekeeper (Processing Hot Pursuit)", "cmd": ["python3", "src/scout_gatekeeper.py"], "critical": False},

    # 4. REASONING (Brain & Strategy)
    {"name": "Brain (Reasoning & Strategy)", "cmd": ["python3", "src/brain_reasoning.py"], "critical": True},
    
    # 5. ARCHIVER (Cleanup)
    {"name": "Archiver", "cmd": ["python3", "src/utils/archiver.py"], "critical": False}
]

def run_step(step, retries=2):
    """Executes a step with self-healing retries."""
    logger.info(f"▶️ Starting: {step['name']}")
    
    for attempt in range(retries + 1):
        try:
            # Fix PYTHONPATH so 'src' module can be found
            env = dict(os.environ)
            env["PYTHONPATH"] = os.getcwd()
            
            result = subprocess.run(step['cmd'], capture_output=True, text=True, check=True, env=env)
            logger.info(f"✅ {step['name']} Completed.")
            if result.stdout:
                print(f"[{step['name']} Output]:\n{result.stdout[:500]}...") # truncate for sanity
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {step['name']} Failed (Attempt {attempt+1}/{retries+1})")
            logger.error(f"Error Output: {e.stderr}")
            if attempt < retries:
                logger.info("Implementing Self-Healing: Retrying in 5 seconds...")
                time.sleep(5)
            else:
                logger.critical(f"💀 {step['name']} Permanently Failed.")
                if step['critical']:
                    return False
    return False

def main():
    logger.info("🚀 Kazuha Invest: Search 2.1 Full Cycle Execution")
    
    success = True
    for step in SCRIPTS:
        if not run_step(step):
            if step['critical']:
                logger.error("Critical step failed. Aborting pipeline.")
                sys.exit(1)
            else:
                logger.warning("Non-critical step failed. Continuing...")
    
    logger.info("🎉 Full Cycle Completed Successfully.")

if __name__ == "__main__":
    main()

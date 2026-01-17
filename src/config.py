import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys & Secrets ---
SAM_GOV_API_KEY = os.getenv("SAM_GOV_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- User Agents (Compliance & Rotation) ---
USER_AGENT_EMAIL = os.getenv("USER_AGENT_EMAIL", "kazuha_admin@gmail.com")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "KazuhaInvestBot")

SEC_USER_AGENT = f"KazuhaInvest/2.0 ({USER_AGENT_EMAIL})"
REDDIT_USER_AGENT = f"macos:KazuhaInvestV2:v1.0 (by /u/{REDDIT_USERNAME})"

# --- Strategy Settings (Type B: Precision/Hunter) ---
STRATEGY = {
    "RELEVANCE_THRESHOLD": 0.85,     # Semantic dedup threshold
    "MIN_CONTRACT_VALUE": 500000,    # Ignore gov contracts below $500k
    "MAX_DEDUP_WINDOW_HRS": 48,      # Hours to keep in dedup history
    "MISSION_LIFESPAN_HRS": 48,      # Default lifespan for dynamic missions
    "SHIELD_DEPTH": "competitors",   # Monitor competitors too
    "MAX_SCOUT_RESULTS": 10,         # Default results per keyword
    "BOOSTED_DEPTH": 20              # Depth for AI-driven missions
}

# --- File Paths ---
PATHS = {
    "INCOMING": "data/Incoming",
    "ARCHIVE": "data/Archive",
    "REPORTS": "data/Reports",
    "PORTFOLIO": "data/portfolio.yml",
    "THEMES": "data/themes.yml",
    "MISSIONS": "data/active_missions.yml"
}

# --- API Endpoints ---
URLS = {
    "SAM_OPPORTUNITIES": "https://api.sam.gov/opportunities/v2/search",
    "SAM_CONTRACTS": "https://api.sam.gov/contract-awards/v1/search"
}

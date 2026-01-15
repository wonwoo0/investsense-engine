import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys & Secrets ---
SAM_GOV_API_KEY = os.getenv("SAM_GOV_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- User Agents (Compliance) ---
USER_AGENT_EMAIL = os.getenv("USER_AGENT_EMAIL", "kazuha_admin@gmail.com")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "KazuhaInvestBot")

SEC_USER_AGENT = f"KazuhaInvest/2.0 ({USER_AGENT_EMAIL})"
REDDIT_USER_AGENT = f"macos:KazuhaInvestV2:v1.0 (by /u/{REDDIT_USERNAME})"

# --- Strategy Settings (Type B: Precision/Hunter) ---
STRATEGY = {
    "RELEVANCE_THRESHOLD": 8.0,      # Score < 8.0 ignored (Option 1B)
    "RECURSION_TRIGGER": 80.0,       # Impact Score > 80 triggers deep dive (Option 2B)
    "SHIELD_DEPTH": "competitors",   # Monitor competitors too (Option 3B - implied aggressive defense)
    "HIRING_TRIGGER": "signal",      # Triggered by news signals (Option 4B)
    "MAX_LOOPS": 2                   # Depth limit
}

# --- API Endpoints ---
URLS = {
    "SAM_OPPORTUNITIES": "https://api.sam.gov/opportunities/v2/search",
    "SAM_CONTRACTS": "https://api.sam.gov/contract-awards/v1/search",
    "OPENROUTER": "https://openrouter.ai/api/v1/chat/completions"
}

# --- Model Selection (OpenRouter Free Tier) ---
MODELS = {
    "SENSING": "google/gemini-2.0-flash-exp:free",      # 1M Context: Best for raw HTML/JSON reading
    "EXTRACTION": "qwen/qwen3-coder:free",              # Best for Structured JSON output
    "FILTERING": "z-ai/glm-4.5-air:free",               # Fast & Smart enough for scoring
    "REASONING": "tngtech/deepseek-r1t-chimera:free",   # Logic Monster (R1 based)
    "SYNTHESIS": "meta-llama/llama-3.1-405b-instruct:free"
}

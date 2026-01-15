import time
import requests
import json
import logging
from typing import Optional
from src.config import OPENROUTER_API_KEY, URLS, MODELS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelFactory:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://github.com/wonwoo0/investsense", 
            "X-Title": "Kazuha Invest 2.0"
        }

    def _get_model_id(self, stage: str) -> str:
        return MODELS.get(stage.upper(), MODELS["SENSING"])

    def call(self, stage: str, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        model = self._get_model_id(stage)
        logger.info(f"Calling OpenRouter Model: {model} for stage: {stage}")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2 if stage == "EXTRACTION" else 0.7
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            # Simple retry logic
            for attempt in range(3):
                response = requests.post(
                    URLS["OPENROUTER"],
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    return content
                elif response.status_code == 429:
                    logger.warning(f"Rate limited. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"API Error {response.status_code}: {response.text}")
                    break
                    
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            
        return ""

# Singleton instance
ai_factory = ModelFactory()

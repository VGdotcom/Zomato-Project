import json
import time
from groq import Groq
from src.models.recommendation import RecommendationResponse
from src.config import settings

class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            print("Warning: GROQ_API_KEY not set! Make sure to set it in your .env file.")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.fallback_model = settings.GROQ_FALLBACK_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        
    def get_recommendations(self, system_prompt: str, user_prompt: str, retries: int = 3) -> RecommendationResponse:
        temp = self.temperature
        current_model = self.model
        
        for attempt in range(retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=current_model,
                    temperature=temp,
                    response_format={"type": "json_object"}
                )
                
                content = chat_completion.choices[0].message.content
                data = json.loads(content)
                return RecommendationResponse(**data)
                
            except json.JSONDecodeError:
                temp = max(0.0, temp - 0.1) # Lower temp to get more deterministic JSON
                print(f"JSON Parse error. Retrying... (Attempt {attempt+1}/{retries})")
            except Exception as e:
                # Handle rate limits
                if "429" in str(e) or "rate limit" in str(e).lower():
                    sleep_time = (attempt + 1) * 2
                    print(f"Rate limit hit. Sleeping {sleep_time}s...")
                    time.sleep(sleep_time)
                    # Switch to fallback model on rate limit
                    current_model = self.fallback_model
                else:
                    print(f"LLM API Error: {e}")
                    raise e
                    
        raise Exception("Failed to get valid JSON from LLM after retries.")

from typing import Tuple, Dict
from src.models.preferences import UserPreferences
from src.data.repository import RestaurantRepository
from src.services.filter import filter_restaurants
from src.services.prompt_builder import build_system_prompt, build_user_prompt
from src.services.llm_client import GroqClient
from src.models.recommendation import RecommendationResponse
from src.config import settings

class RecommendationService:
    def __init__(self):
        self.repo = RestaurantRepository()
        self.repo.load_data()
        self.llm = GroqClient()
        
    def get_recommendations(self, prefs: UserPreferences) -> Tuple[RecommendationResponse, Dict[str, bool]]:
        # 1. Filter candidates
        all_restaurants = self.repo.get_all_restaurants()
        candidates, fallbacks = filter_restaurants(all_restaurants, prefs, top_n=settings.MAX_CANDIDATES_FOR_LLM)
        
        if not candidates:
            return RecommendationResponse(recommendations=[]), fallbacks
            
        # 2. Build Prompts
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(prefs, candidates)
        
        # 3. Call LLM
        try:
            response = self.llm.get_recommendations(system_prompt, user_prompt)
            # Ensure we only return up to TOP_K
            response.recommendations = response.recommendations[:settings.TOP_K_RECOMMENDATIONS]
        except Exception as e:
            print(f"LLM failed: {e}. Falling back to heuristic sort.")
            recs = []
            for i, c in enumerate(candidates[:settings.TOP_K_RECOMMENDATIONS]):
                recs.append({
                    "rank": i + 1,
                    "name": c.name,
                    "cuisine": c.cuisines[0] if c.cuisines else "Unknown",
                    "rating": c.rating,
                    "cost": c.cost_for_two,
                    "rationale": "Heuristic fallback recommendation."
                })
            response = RecommendationResponse(recommendations=recs)
            
        return response, fallbacks

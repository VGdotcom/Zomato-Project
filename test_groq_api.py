import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.models.preferences import UserPreferences
from src.services.recommendation import RecommendationService

def test_ai():
    print("Initializing Recommendation Service...")
    service = RecommendationService()
    
    prefs = UserPreferences(
        location="Bellandur",
        budget="medium",
        min_rating=4.2,
        cuisine=None,
        custom_notes=None
    )
    
    print(f"Requesting recommendations for: {prefs}")
    try:
        response, fallbacks = service.get_recommendations(prefs)
        
        print(f"\nFallbacks applied: {fallbacks}")
        print("\nRecommendations:")
        for rec in response.recommendations:
            print(f"#{rec.rank} - {rec.name} ({rec.rating}⭐) - {rec.cuisine}")
            print(f"Cost: ₹{rec.cost}")
            print(f"Rationale: {rec.rationale}")
            print("-" * 40)
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_ai()

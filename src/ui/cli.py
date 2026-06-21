import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.preferences import UserPreferences
from src.services.recommendation import RecommendationService

def run_cli():
    print("Welcome to the Zomato AI Restaurant Recommender!")
    print("-" * 50)
    
    location = input("Enter Location (e.g. Indiranagar, Banashankari): ").strip()
    budget = input("Enter Budget (low, medium, high): ").strip()
    min_rating = float(input("Enter Minimum Rating (0.0 - 5.0): ").strip())
    cuisine = input("Enter preferred Cuisine (optional, press enter to skip): ").strip()
    if not cuisine:
        cuisine = None
        
    prefs = UserPreferences(
        location=location,
        budget=budget,
        min_rating=min_rating,
        cuisine=cuisine
    )
    
    print("\nFetching recommendations...")
    service = RecommendationService()
    try:
        response, fallbacks = service.get_recommendations(prefs)
        
        if fallbacks.get("cuisine_dropped"):
            print("[Warning] Could not find exact cuisine matches, broadened search.")
        if fallbacks.get("rating_dropped"):
            print("[Warning] Could not meet minimum rating, lowered rating threshold.")
            
        print("\n--- TOP RECOMMENDATIONS ---")
        for rec in response.recommendations:
            print(f"\n#{rec.rank}: {rec.name} ({rec.rating} stars)")
            print(f"Cuisine: {rec.cuisine} | Cost: ₹{rec.cost}")
            print(f"Why: {rec.rationale}")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_cli()

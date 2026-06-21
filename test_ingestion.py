import sys
import os

# Add root directory to path to allow importing src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data.repository import RestaurantRepository

def test_ingestion():
    print("Initializing repository...")
    repo = RestaurantRepository()
    
    print("Loading data...")
    restaurants = repo.get_all_restaurants()
    
    print(f"\nSuccessfully loaded {len(restaurants)} restaurants!")
    
    if restaurants:
        print("\nSample Restaurant Data:")
        sample = restaurants[0]
        print(f"ID: {sample.id}")
        print(f"Name: {sample.name}")
        print(f"Location: {sample.location}")
        print(f"Cuisines: {sample.cuisines}")
        print(f"Rating: {sample.rating}")
        print(f"Votes: {sample.votes}")
        print(f"Cost for two: {sample.cost_for_two}")
        print(f"Budget Tier: {sample.budget_tier}")

if __name__ == "__main__":
    test_ingestion()

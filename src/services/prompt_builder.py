import json
from typing import List
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences

def build_system_prompt() -> str:
    return """You are an expert AI restaurant recommender. 
You will be provided with the user's preferences and a shortlist of candidates in JSON format.
Your job is to select the best restaurants from the candidates, rank them, and provide a convincing rationale for each based on the user's custom notes and preferences.
CRITICAL RULES:
1. DO NOT hallucinate or invent restaurants. You MUST ONLY recommend restaurants that are present in the `candidate_restaurants` list.
2. Use the EXACT `name`, `cuisine`, `rating`, and `cost_for_two` provided in the candidate list.
3. Write the rationale as a concise, punchy 2-sentence quote that specifically connects the restaurant to the user's preferences (e.g. 'Best-in-class handmade pasta. Perfectly matches your request for outdoor seating and premium ambiance.').
4. You MUST respond with pure, valid JSON matching the schema provided."""

def build_user_prompt(prefs: UserPreferences, candidates: List[Restaurant]) -> str:
    candidate_list = []
    for r in candidates:
        candidate_list.append({
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "cuisines": r.cuisines,
            "rating": r.rating,
            "votes": r.votes,
            "cost_for_two": r.cost_for_two
        })
        
    context = {
        "user_preferences": prefs.dict(),
        "candidate_restaurants": candidate_list
    }
    
    return f"""Please provide your recommendations based on the following context.
Output pure JSON matching this schema:
{{
  "recommendations": [
    {{
      "rank": 1,
      "name": "Restaurant Name",
      "cuisine": "Primary Cuisine",
      "rating": 4.5,
      "cost": 1000.0,
      "rationale": "Why this matches user preferences."
    }}
  ]
}}

Context:
{json.dumps(context, indent=2)}"""

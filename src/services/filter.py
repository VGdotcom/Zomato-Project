from typing import List, Tuple, Dict
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences

def filter_restaurants(restaurants: List[Restaurant], prefs: UserPreferences, top_n: int = 15) -> Tuple[List[Restaurant], Dict[str, bool]]:
    """
    Filters the list of restaurants based on user preferences.
    Returns the filtered list of top_n candidates, and a dictionary detailing if any fallbacks were applied.
    """
    candidates = restaurants
    fallbacks_applied = {
        "cuisine_dropped": False,
        "rating_dropped": False
    }

    # 1. Location constraint (strict)
    candidates = [r for r in candidates if prefs.location.lower() in r.location.lower()]

    # 2. Budget constraint (strict)
    candidates = [r for r in candidates if r.budget_tier == prefs.budget]

    # Check if empty early
    if not candidates:
        return [], fallbacks_applied

    # 3. Cuisine match
    cuisine_candidates = candidates
    if prefs.cuisine:
        cuisine_candidates = [
            r for r in candidates 
            if any(prefs.cuisine.lower() in c.lower() for c in r.cuisines)
        ]
        
    if not cuisine_candidates and prefs.cuisine:
        fallbacks_applied["cuisine_dropped"] = True
        # fallback to candidates without cuisine filter
    else:
        candidates = cuisine_candidates

    # 4. Rating constraint
    rating_candidates = [r for r in candidates if r.rating >= prefs.min_rating]
    
    if not rating_candidates and prefs.min_rating > 0.0:
        fallbacks_applied["rating_dropped"] = True
        # fallback to candidates without rating filter
    else:
        candidates = rating_candidates

    # 5. Order candidates by aggregate rating and review/vote count
    # Sorting by rating first (descending), then votes (descending)
    candidates.sort(key=lambda r: (r.rating, r.votes), reverse=True)

    # Deduplicate by name to prevent multiple branches of the same restaurant from dominating
    seen_names = set()
    unique_candidates = []
    for r in candidates:
        name_key = r.name.lower().strip()
        if name_key not in seen_names:
            seen_names.add(name_key)
            unique_candidates.append(r)

    # 6. Restrict list size
    return unique_candidates[:top_n], fallbacks_applied

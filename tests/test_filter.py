from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.services.filter import filter_restaurants

def test_filter_restaurants():
    r1 = Restaurant(id="1", name="R1", location="Indiranagar", cuisines=["Italian"], rating=4.5, votes=100, cost_for_two=400.0, budget_tier="low")
    r2 = Restaurant(id="2", name="R2", location="Indiranagar", cuisines=["Chinese"], rating=3.5, votes=50, cost_for_two=400.0, budget_tier="low")
    r3 = Restaurant(id="3", name="R3", location="Koramangala", cuisines=["Italian"], rating=4.8, votes=200, cost_for_two=1000.0, budget_tier="medium")
    
    prefs = UserPreferences(location="Indiranagar", budget="low", min_rating=4.0)
    
    results, fallbacks = filter_restaurants([r1, r2, r3], prefs)
    
    assert len(results) == 1
    assert results[0].id == "1"
    assert not fallbacks["cuisine_dropped"]
    assert not fallbacks["rating_dropped"]
    
def test_filter_fallbacks():
    r1 = Restaurant(id="1", name="R1", location="Indiranagar", cuisines=["Italian"], rating=4.5, votes=100, cost_for_two=400.0, budget_tier="low")
    
    prefs = UserPreferences(location="Indiranagar", budget="low", min_rating=4.8, cuisine="Chinese")
    
    results, fallbacks = filter_restaurants([r1], prefs)
    
    assert len(results) == 1
    assert results[0].id == "1"
    assert fallbacks["cuisine_dropped"] == True
    assert fallbacks["rating_dropped"] == True

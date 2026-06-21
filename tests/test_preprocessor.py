import pandas as pd
from src.data.preprocessor import preprocess_dataframe, clean_cuisines, get_budget_tier

def test_clean_cuisines():
    assert clean_cuisines("Italian, Chinese") == ["Italian", "Chinese"]
    assert clean_cuisines(None) == []

def test_get_budget_tier():
    assert get_budget_tier(400) == "low"
    assert get_budget_tier(1000) == "medium"
    assert get_budget_tier(2000) == "high"

def test_preprocess_dataframe():
    df = pd.DataFrame({
        "name": ["Test Rest"],
        "cuisines": ["Italian, Chinese"],
        "location": [" indiranagar "],
        "rate": ["4.1/5"],
        "votes": ["100"],
        "approx_cost(for two people)": ["1,200"]
    })
    
    clean_df = preprocess_dataframe(df)
    
    assert clean_df["cuisines_list"].iloc[0] == ["Italian", "Chinese"]
    assert clean_df["location_clean"].iloc[0] == "Indiranagar"
    assert clean_df["rating_clean"].iloc[0] == 4.1
    assert clean_df["votes_clean"].iloc[0] == 100
    assert clean_df["cost_clean"].iloc[0] == 1200.0
    assert clean_df["budget_tier"].iloc[0] == "medium"

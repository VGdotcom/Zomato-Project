import pandas as pd
import numpy as np
from src.config import BUDGET_LOW_MAX, BUDGET_MEDIUM_MAX

def clean_cuisines(cuisine_str) -> list:
    if pd.isna(cuisine_str):
        return []
    return [c.strip() for c in str(cuisine_str).split(",")]

def clean_location(loc_str) -> str:
    if pd.isna(loc_str):
        return "unknown"
    return str(loc_str).strip().title()

def get_budget_tier(cost: float) -> str:
    if pd.isna(cost):
        return "unknown"
    if cost <= BUDGET_LOW_MAX:
        return "low"
    elif cost <= BUDGET_MEDIUM_MAX:
        return "medium"
    return "high"

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and normalizes the dataframe columns.
    """
    df_clean = df.copy()
    
    # Remove duplicates that occur due to multiple listing types in Zomato dataset
    if 'url' in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=['url'])
    elif 'name' in df_clean.columns and 'location' in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=['name', 'location'])
        
    # Clean garbled characters from names (Mojibake)
    if 'name' in df_clean.columns:
        df_clean['name'] = df_clean['name'].astype(str)
        # Fix specific highly garbled names
        df_clean['name'] = df_clean['name'].str.replace(r'SantÃ.*Spa Cuisine', 'Sante Spa Cuisine', regex=True)
        df_clean['name'] = df_clean['name'].str.replace(r'CafÃ.*', 'Cafe', regex=True)
        # Strip remaining non-ascii safely
        df_clean['name'] = df_clean['name'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
        
    # 1. Parse cuisines
    if 'cuisines' in df_clean.columns:
        df_clean['cuisines_list'] = df_clean['cuisines'].apply(clean_cuisines)
    else:
        df_clean['cuisines_list'] = [[] for _ in range(len(df_clean))]
        
    # 2. Clean location
    if 'location' in df_clean.columns:
        df_clean['location_clean'] = df_clean['location'].apply(clean_location)
    else:
        df_clean['location_clean'] = "Unknown"
        
    # 3. Coerce rating
    if 'rate' in df_clean.columns:
        df_clean['rating_clean'] = df_clean['rate'].astype(str).str.extract(r'([0-9\.]+)')[0]
        df_clean['rating_clean'] = pd.to_numeric(df_clean['rating_clean'], errors='coerce').fillna(0.0)
    elif 'rating' in df_clean.columns:
         df_clean['rating_clean'] = pd.to_numeric(df_clean['rating'], errors='coerce').fillna(0.0)
    else:
        df_clean['rating_clean'] = 0.0
        
    # 4. Coerce votes
    if 'votes' in df_clean.columns:
        df_clean['votes_clean'] = pd.to_numeric(df_clean['votes'], errors='coerce').fillna(0).astype(int)
    else:
        df_clean['votes_clean'] = 0

    # 5. Coerce cost
    cost_col = None
    for col in df_clean.columns:
        if 'cost' in col.lower() or 'price' in col.lower():
            cost_col = col
            break
            
    if cost_col:
        df_clean['cost_clean'] = df_clean[cost_col].astype(str).str.replace(',', '')
        df_clean['cost_clean'] = pd.to_numeric(df_clean['cost_clean'], errors='coerce').fillna(0.0)
    else:
        df_clean['cost_clean'] = 0.0
        
    # 6. Derive budget tier
    df_clean['budget_tier'] = df_clean['cost_clean'].apply(get_budget_tier)
    
    return df_clean

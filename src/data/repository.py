import pandas as pd
from typing import List
from src.models.restaurant import Restaurant
from src.data.loader import load_or_download_dataset
from src.data.preprocessor import preprocess_dataframe

class RestaurantRepository:
    def __init__(self):
        self._df: pd.DataFrame = None
        self._restaurants: List[Restaurant] = []
        
    def load_data(self):
        """Loads and preprocesses data into memory."""
        raw_df = load_or_download_dataset()
        self._df = preprocess_dataframe(raw_df)
        self._build_models()
        
    def _build_models(self):
        """Builds domain models from the cleaned dataframe."""
        self._restaurants = []
        for idx, row in self._df.iterrows():
            name = row.get('name', f"Restaurant_{idx}")
            url = row.get('url', None)
            rest_id = str(url) if url else str(idx)
            
            r = Restaurant(
                id=rest_id,
                name=str(name),
                location=row.get('location_clean', 'Unknown'),
                cuisines=row.get('cuisines_list', []),
                rating=row.get('rating_clean', 0.0),
                votes=row.get('votes_clean', 0),
                cost_for_two=row.get('cost_clean', 0.0),
                budget_tier=row.get('budget_tier', 'unknown'),
                url=url
            )
            self._restaurants.append(r)
            
    def get_all_restaurants(self) -> List[Restaurant]:
        if not self._restaurants:
            self.load_data()
        return self._restaurants

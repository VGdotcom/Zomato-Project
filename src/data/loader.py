import os
import pandas as pd
from datasets import load_dataset
from src.config import DATASET_ID, CACHE_FILE, DATA_DIR

def load_or_download_dataset() -> pd.DataFrame:
    """
    Loads the Zomato dataset from the local parquet cache if it exists.
    Otherwise, downloads it from Hugging Face and saves it to the cache.
    """
    if CACHE_FILE.exists():
        print(f"Loading dataset from cache: {CACHE_FILE}")
        return pd.read_parquet(CACHE_FILE)
    
    print(f"Downloading dataset '{DATASET_ID}' from Hugging Face...")
    # The dataset has a 'train' split by default. Limit to 5000 rows to save memory on free tiers.
    dataset = load_dataset(DATASET_ID, split="train[:5000]")
    df = dataset.to_pandas()
    
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving dataset to cache: {CACHE_FILE}")
    df.to_parquet(CACHE_FILE, index=False)
    
    return df

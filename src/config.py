import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    # Groq Settings
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL: str = "llama-3.1-8b-instant"
    GROQ_TEMPERATURE: float = 0.3
    
    # Dataset
    HF_DATASET_NAME: str = "ManikaSaini/zomato-restaurant-recommendation"
    DATA_CACHE_PATH: str = "./data/zomato_cache.parquet"
    
    # Recommendation
    MAX_CANDIDATES_FOR_LLM: int = 15
    TOP_K_RECOMMENDATIONS: int = 5
    
    # Budget Thresholds
    BUDGET_LOW_MAX: int = 500
    BUDGET_MEDIUM_MAX: int = 1500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Backwards compatibility for other modules
DATASET_ID = settings.HF_DATASET_NAME
# Resolve cache path relative to BASE_DIR if it's relative
_cache_path = Path(settings.DATA_CACHE_PATH)
if not _cache_path.is_absolute():
    CACHE_FILE = settings.BASE_DIR / _cache_path
else:
    CACHE_FILE = _cache_path

DATA_DIR = settings.DATA_DIR
BUDGET_LOW_MAX = settings.BUDGET_LOW_MAX
BUDGET_MEDIUM_MAX = settings.BUDGET_MEDIUM_MAX

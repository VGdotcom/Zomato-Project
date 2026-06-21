import os
import sys
from fastapi import FastAPI, HTTPException

# Ensure root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.preferences import UserPreferences
from src.services.recommendation import RecommendationService

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Zomato AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = RecommendationService()

@app.post("/api/recommend")
def recommend_restaurants(prefs: UserPreferences):
    try:
        response, fallbacks = service.get_recommendations(prefs)
        return {
            "recommendations": response.recommendations,
            "fallbacks": fallbacks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Zomato AI API is running. Go to /docs for Swagger UI."}

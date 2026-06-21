import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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

# Configure static frontend mounting
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend")
os.makedirs(frontend_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not built yet. Go to /docs for API."}

from pydantic import BaseModel
from typing import List

class RecommendationNode(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    cost: float
    rationale: str

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationNode]

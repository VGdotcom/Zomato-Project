from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationNode(BaseModel):
    rank: int
    name: Optional[str] = Field(default="Unknown")
    cuisine: Optional[str] = Field(default="Various")
    rating: Optional[float] = Field(default=0.0)
    cost: Optional[float] = Field(default=0.0)
    rationale: Optional[str] = Field(default="Recommended based on your preferences.")

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationNode]

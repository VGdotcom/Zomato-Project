from pydantic import BaseModel, Field, validator
from typing import Optional

class UserPreferences(BaseModel):
    location: str
    budget: str
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    cuisine: Optional[str] = None
    custom_notes: Optional[str] = None

    @validator("budget")
    def validate_budget(cls, v):
        allowed = ["low", "medium", "high"]
        v_lower = v.lower().strip()
        if v_lower not in allowed:
            raise ValueError(f"budget must be one of {allowed}")
        return v_lower
        
    @validator("min_rating")
    def validate_rating(cls, v):
        if not (0.0 <= v <= 5.0):
            raise ValueError("min_rating must be between 0.0 and 5.0")
        return v

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Restaurant:
    id: str
    name: str
    location: str
    cuisines: List[str]
    rating: float
    votes: int
    cost_for_two: float
    budget_tier: str  # 'low', 'medium', 'high'
    url: Optional[str] = None

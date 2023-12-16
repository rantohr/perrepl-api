from pydantic import BaseModel
from typing import List, Dict

class SubscriptionValidator(BaseModel):
    plan: List[Dict[str, int]]
    monthly: bool = False
    yearly: bool = False

    class Config:
        extra = 'forbid'
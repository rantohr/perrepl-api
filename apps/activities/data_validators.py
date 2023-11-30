from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IDValidator(BaseModel):
    id: int

class ActivityValidator(BaseModel):
    name: str
    description: str
    location: List[IDValidator]

class ActivityPricingValidator(BaseModel):
    supplier: List[IDValidator]
    price: float
    currency: str
    

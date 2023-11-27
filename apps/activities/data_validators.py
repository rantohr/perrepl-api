from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CountryIDValitor(BaseModel):
    id: int

class ActivityValidator(BaseModel):
    name: str
    description: str
    location: List[CountryIDValitor]

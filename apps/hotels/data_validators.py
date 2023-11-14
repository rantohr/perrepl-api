from pydantic import BaseModel
from typing import List

class CountryIDValitor(BaseModel):
    id: int

class HotelValidator(BaseModel):
    name: str
    description: str
    location: List[CountryIDValitor]

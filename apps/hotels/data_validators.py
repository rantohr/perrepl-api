from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CountryIDValitor(BaseModel):
    id: int

class RoomValidator(BaseModel):
    room_number: int
    bed_type: str
    is_available: bool = True
class HotelValidator(BaseModel):
    name: str
    description: str
    locations: List[CountryIDValitor]
    rooms: List[RoomValidator]

class RoomPriceValidator(BaseModel):
    id: int
    hotel: int
    price: float
    currency: Optional[str] = 'EUR'
    season: Optional[str] = None
    start_season: Optional[datetime] = None
    end_season: Optional[datetime] = None

class HotelPricingValidator(BaseModel):
    supplier: List[int]
    rooms: List[RoomPriceValidator]

from pydantic import BaseModel
from typing import List

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
from pydantic import Field, BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ItinerarySegmentValidator(BaseModel):
    description: str
    duration: int
    start_location: int
    end_location: int # = Field(default=None)
    departure_time_utc: Optional[datetime]
    arrival_time_utc: Optional[datetime]
    distance: Optional[int] = Field(default=0)
    hotels: List[Dict[str, int]] = Field(default_factory=list)
    activities: List[Dict[str, int]] = Field(default_factory=list)

class ItineraryValidator(BaseModel):
    title: str
    description: str
    duration: int
    availability: str
    segments: List[ItinerarySegmentValidator]
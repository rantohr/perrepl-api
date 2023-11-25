from pydantic import Field, BaseModel, field_validator, validator
from typing import List, Dict, Optional
from datetime import datetime

class ItinerarySegmentValidator(BaseModel):
    description: str
    duration: int
    start_location: List[Dict[str, int]] = Field(default_factory=list)
    end_location: List[Dict[str, int]] = Field(default_factory=list)
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
    client_id: int = None
    order_id: int = None
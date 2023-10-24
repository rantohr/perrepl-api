from datetime import datetime
from typing import Annotated, List
from .choices import *

from pydantic import BaseModel, field_validator

class TravelerValidator(BaseModel):
    email: str
    first_name: str
    last_name: str
    gender: str
    phone_number: str = None

class OrderValidator(BaseModel):
    departure_datetime: datetime
    arrival_datetime: datetime
    trip_duration: int
    client_type: Annotated[str, str]
    room_type: Annotated[str, str]
    pax_type: str # TODO: Validate format using regular expressions
    travelers: List[TravelerValidator]
    trip_interest: Annotated[str, str] = None
    custom_trip_reason: str = None
    trip_reason: Annotated[str, str] = None

    @field_validator('client_type', 'room_type', 'trip_interest', 'trip_reason')
    def client_type_in_allowed_value(cls, v, info):
        if v not in ALLOWED_VALUES[info.field]:
            raise ValueError(f"Invalid {info.field}. Allowed values are: {', '.join( ALLOWED_VALUES[info.field])}")
        return v

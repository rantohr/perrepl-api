from datetime import datetime
import re
from typing import List, Optional
from .choices import *

from pydantic import (
    BaseModel,
    field_validator,
    EmailStr
)

class OrderStatusValidator(BaseModel):
    order_status: str

    @field_validator("order_status")
    def check_status_allowed_value(cls, v, info):
        if v.capitalize() not in ORDER_STATUS:
            raise ValueError(f"Expected values are in: [{', '.join(ORDER_STATUS)}]. Given [{v}]")
        return v.capitalize()
    
    class Config:
        extra = 'forbid'

class TravelerValidator(BaseModel):
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str] = "UNK"
    traveler_type: str = "ADT"
    phone_number: str = None
    lead_traveler: bool = True
    
    @field_validator('gender')
    def check_allowed_value(cls, v, info):
        if v not in ALLOWED_VALUES[info.field_name]:
            raise ValueError(f"Invalid {info.field_name}. Allowed values are: {', '.join(ALLOWED_VALUES[info.field_name])}")
        return v
    
    @field_validator('traveler_type')
    def check_traveler_type(cls, v):
        if v not in PAX_TYPES:
            raise ValueError(f"Code {v} doesn't exist. Allowed values are: {', '.join(PAX_TYPES)}")
        return v

class OrderValidator(BaseModel):
    departure_datetime: datetime
    arrival_datetime: datetime
    trip_duration: int
    client_type: str # Annotated[str, str]
    room_type: str # Annotated[str, str]
    pax_type: str # TODO: Validate format using regular expressions
    travelers: List[TravelerValidator]
    trip_interest: str # Annotated[str, str] = None
    custom_trip_reason: str = None
    trip_reason: str # Annotated[str, str] = None
    description: str
    
    @field_validator('client_type', 'room_type', 'trip_interest', 'trip_reason')
    def choices_allowed_value(cls, v, info):
        if v not in ALLOWED_VALUES[info.field_name]:
            raise ValueError(f"Invalid {info.field_name}. Allowed values are: {', '.join( ALLOWED_VALUES[info.field_name])}")
        return v
    
    @field_validator('pax_type')
    def validate_pax_type_format(cls, v):
        pax_type = v.replace(' ', '').upper()

        # Check pax codes
        pattern = r'[A-Z]+'
        pax_codes = re.findall(pattern, pax_type)
        for code in pax_codes:
            if code not in PAX_TYPES:
                raise ValueError(f"Code {code} doesn't exist. Allowed values are: {', '.join(PAX_TYPES)}")
            
        # Check general format
        pattern = r'[a-zA-Z]{3}:\d+(,[a-zA-Z]{3}:\d+)*'
        if re.fullmatch(pattern, pax_type) is None:
            raise ValueError(f"Expected pax_code format is (CODE:Number)+ (Ex: ADT:1,CNN:1,INF:1). Given --> {pax_type}")
        
        # Check number of passengers
        pattern = r'\d+'
        if sum(map(int, re.findall(pattern, pax_type))) == 0:
            raise ValueError(f"At least one passenger is specified")
        return pax_type


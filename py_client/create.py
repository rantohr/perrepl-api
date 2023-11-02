import requests
from setting import *
from urllib.parse import urljoin
import json

uri = "/api/v2/order/"
endpoint = urljoin(BASE_URL, uri)

data = {
    "departure_datetime": "2023-11-06T15:30:44",
    "arrival_datetime": "2023-11-20T10:45:22",
    "trip_duration": 6,
    "client_type": "Direct Client",
    "room_type": "1 Person",
    "pax_type": "ADT:1,CNN:0,INF:0",
    "travelers": [
        {
            "email": "solen.test29@yahoo.fr",
            "first_name": "Frederic",
            "last_name": "Andrianarivony",
            "gender": "Male",
            "phone_number": "+261 34 77 161 84"
        }
    ],
    "trip_interest": "Beach",
    "trip_reason": "Anniversary",
    "custom_trip_reason": "Funerary"
}

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4ODcwOTc2LCJpYXQiOjE2OTg4NjczNzYsImp0aSI6IjIwZjYxYTMzYjA2YzQ1YmQ4MmUxNzA2MmZmMGI0ODUwIiwidXNlcl9pZCI6MX0._PFSLN6_S3rTgRP5cuUe00mbaSi4RsRlJXhPfJIv76c'
}
response = requests.post(endpoint, json=data, headers=headers)
print(response.json())



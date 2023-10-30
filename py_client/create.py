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
            "email": "solen.test@yahoo.fr",
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
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4NjkyOTQwLCJpYXQiOjE2OTg2ODkzNDAsImp0aSI6IjVkYWE1NDhkZWE5MDRjY2U4YjI3ZmRjN2M5NGJhMjEyIiwidXNlcl9pZCI6MX0.WsXi3WKjJ3VF3bHdHb6_7awO-0uPLtmVnzYFt9mmnQI'
}
response = requests.post(endpoint, json=data, headers=headers)
print(response.json())



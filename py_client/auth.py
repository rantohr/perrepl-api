import requests
from urllib.parse import urljoin
from setting import *

auth_uri = "/api/v1/auth/token/"

auth_endpoint = urljoin(BASE_URL, auth_uri)

auth_response = requests.post(auth_endpoint, json={"email": "pereepl@example.com", "password": "pereepl_password"})
# {"email": "frederic.andrianarivo@gmail.com", "password": "Fr3d3r!c"}
print(auth_response.json()["access"])
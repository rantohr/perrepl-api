import requests
from setting import *
from urllib.parse import urljoin

auth_uri = "/api/v1/auth/token/"
auth_endpoint = urljoin(BASE_URL, auth_uri)
auth_response = requests.post(auth_endpoint, json={"email": "pereepl@example.com", "password": "pereepl_password"})

if auth_response.status_code == 200:
    token = auth_response.json()['access']
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "order_status": "Confirmed",
    }

    endpoint = urljoin(BASE_URL, "/api/v2/order/2/change_status/")
    response = requests.post(endpoint, headers=headers, json=data)
    print(response.json())
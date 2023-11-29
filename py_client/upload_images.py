import requests
from setting import *
from urllib.parse import urljoin
import json
from PIL import Image
import io

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

uri = "/api/v2/hotel/"
endpoint = urljoin(BASE_URL, uri)

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# URL of the API endpoint

# Define the FormData-like object
form_data = {
    "json_data": '{"key1": "value1", "key2": "value2"}',
    "file": ("example.jpg", open("to_upload.png", "rb"), "image/png"),
    # "file": ("example.jpg", Image.open("to_upload.png"), "image/png")
}

# Build the multipart form-data payload using MultipartEncoder
multipart_encoder = MultipartEncoder(fields=form_data)

# Set the Content-Type header with the boundary from the encoder
headers = {
    "Content-Type": multipart_encoder.content_type,
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxMjgzOTUwLCJpYXQiOjE3MDExOTc1NTAsImp0aSI6ImY3OWUzZjc0MDQ4ODQ1Njk5NTg4ODI1MDAxYmJkNmFiIiwidXNlcl9pZCI6MX0.D8m3qRtQFfKH-TzvzzxO2whHsb-0sBsEabb__5sRXHg'
}

# Make the POST request
response = requests.post(endpoint, headers=headers, data=multipart_encoder)

# Print the response
print(response.status_code)
print(response.text)
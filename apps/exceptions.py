from rest_framework.exceptions import APIException
from rest_framework import status

class WrongURL(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not Found"

class MissingClienOROrder(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "At least one of client or order must be specified"

class NoImageDataProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No image data provided"
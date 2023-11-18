from rest_framework import exceptions

class ActiveRecordSetNotFound(exceptions.APIException):
    status_code = 404
    default_detail = "Not Found"

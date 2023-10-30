from rest_framework import permissions

class PermissionMixin:
    permission_classes = [
        permissions.IsAuthenticated
    ]
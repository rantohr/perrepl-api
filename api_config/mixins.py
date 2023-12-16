import json
import uuid
from apps.exceptions import NoImageDataProvided, WrongURL
from apps.images.models import Image
from rest_framework import permissions
from rest_framework import status
from rest_framework import exceptions
from django.utils import timezone

class PermissionCheckMixin:
    def check_permissions(self, request):
        super().check_permissions(request)
        user = request.user
        user_subscription = user.subscriptions.all().order_by('-end_date')
        path_basename = request.path.split('/')[-2]
        if path_basename == 'plan' and self.action == 'list':
            print('All authenticated user can view plan')

        elif user_subscription:
            u_subsc = user_subscription.first()
            start_date = u_subsc.start_date
            end_date = u_subsc.end_date
            today = timezone.now()
            if not (start_date <= today <= end_date):
                raise exceptions.PermissionDenied(detail="Subscription expired")
        else:
            if not user.is_superuser:
                raise exceptions.PermissionDenied(detail="No subscription found")

class PermissionMixin(PermissionCheckMixin):
    permission_classes = [
        permissions.IsAuthenticated
    ]

class AdminPermissionMixin(PermissionCheckMixin):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    ]

class SerializerContextMixin:
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        return {**context, **kwargs}

class ImageMixin:
    def create_image(self, app_name):
        if app_name and app_name in [
            "hotel",
            "activity",
            "room",
            "supplier",
            "client",
            "user"
        ]:
            img = self.request.data.get('image')
            if not img:
                raise NoImageDataProvided(detail="No image data provided")
            
            file_names = Image.objects.values_list('file_name', flat=True)
            f_name = str(uuid.uuid4())
            while f_name in file_names:
                f_name = str(uuid.uuid4())
            image = Image.objects.create(folder_name=app_name, file_name=f_name, image_url=img)
            return image
        else:
            raise WrongURL(detail="Not Found")

class ValidatorMixin:
    def _validate_data(self, validator):
        try:
            validated_data_obj = validator(**self.request.data)
        except ValueError as error:
            error_message = json.loads(error.json())[0]
            error_message.pop('url', None)
            error_message.pop('ctx', None)
            return dict(error_message=error_message, status=status.HTTP_400_BAD_REQUEST)
        return validated_data_obj
    

class UserQuerySetMixin:
    user_field = 'user'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = dict()
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(**lookup_data)
        return qs

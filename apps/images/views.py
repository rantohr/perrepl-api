import uuid
from rest_framework.response import Response
from rest_framework import (
    parsers,
    viewsets,
    decorators,
    status
)
from api_config import mixins

from .models import Image
from .serializers import ImageSerializer

class ImageViewset(mixins.PermissionMixin, mixins.ImageMixin, viewsets.GenericViewSet):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @decorators.action(methods=['post'], detail=False, url_path='upload/(?P<app_name>\S+)')
    def upload(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name', None)
        if app_name:
            image_obj = self.create_image(app_name)
            serialized_data = self.get_serializer(image_obj).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

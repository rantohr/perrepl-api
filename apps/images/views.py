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

class ImageViewset(mixins.PermissionMixin, viewsets.GenericViewSet):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @decorators.action(methods=['post'], detail=False, url_path='upload/(?P<app_name>\S+)')
    def upload(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name', None)
        if app_name and app_name in [
            "hotel",
            "activity",
            "room",
            "supplier",
            "client",
            "user"
        ]:
            img = request.data.get('image')
            if not img:
                return Response({"errorMessage": "No image data provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            file_names = Image.objects.values_list('file_name', flat=True)
            f_name = str(uuid.uuid4())
            while f_name in file_names:
                f_name = str(uuid.uuid4())
            image = Image.objects.create(folder_name=kwargs.get('app_name'), file_name=f_name, image_url=img)
            return Response(self.get_serializer(image).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

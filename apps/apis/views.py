from .serializers import CustomTokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api_config import mixins

# Create your views here.

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
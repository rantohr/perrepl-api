from django.urls import path, include
from .views import CustomTokenObtainView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/token/', CustomTokenObtainView.as_view(), name='token-authentication'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

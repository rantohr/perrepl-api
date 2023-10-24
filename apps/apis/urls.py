from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token-authentication'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
    )

urlpatterns=[
    path('auth/', TokenObtainPairView.as_view(), name='token-auth'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('logout/', TokenBlacklistView.as_view(), name='token-logout'),
]
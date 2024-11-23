from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.urls import path
from .. import views


urlpatterns = [
    path("registration/", views.RegistrationAPIView.as_view(), name="registration"),
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="token-access"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path("test-email", views.TestEmailSend.as_view(), name="test-email"),
    path(
        "activation/confirm/<str:token>",
        views.ActivationAPIView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
]

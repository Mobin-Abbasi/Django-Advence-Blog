from django.urls import path
from . import views


app_name = "api-v1"


urlpatterns = [
    path("registration/", views.RegistrationAPIView.as_view(), name="registration"),
    path("tokrn/login", views.CustomObtainAuthToken.as_view(), name="token-login"),
]

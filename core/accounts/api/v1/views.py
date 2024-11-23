from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

from mail_templated import EmailMessage
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt

from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivateResendSerializer,
)
from ...models import Profile
from ..utils import EmailThread
from ...models import User


# getting user model object
# User = get_user_model


class RegistrationAPIView(generics.GenericAPIView):
    """Serializer for registration"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Registering a new user"""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}

            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)

            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """Generate tokens for a user"""

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    """Obtain authentication token"""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Overriding the post method to handle authentication"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    """Discards the current authentication token"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Discards the current authentication token"""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Obtain authentication token"""

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    """Change password for authenticated user"""

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the authenticated user"""
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """Change the password for the authenticated user"""
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {
                    "details": "password change successfully",
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve profile for authenticated user"""

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):
    """Test email sending using template"""

    def get(self, request, *args, **kwargs):
        """Send email using template"""

        self.email = "user@example.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/hello.tpl",
            {"token": token},
            "admin@admin.com",
            to=[self.email],
        )
        EmailThread(email_obj).start()
        return Response("sent mail")

    def get_tokens_for_user(self, user):
        """Generate tokens for a user"""

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationAPIView(APIView):
    """Activate user account using token"""

    def get(self, request, token, *args, **kwargs):
        """Activate user account using token"""
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"details": "token has been expired"})
        except InvalidTokenError:
            return Response({"details": "token is not valid"})

        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_verified:
            return Response({"details": "your account has already been verified"})

        user_obj.is_verified = True
        user_obj.save()

        return Response({"details": "account has been successfully verified"})


class ActivationResendApiView(generics.GenericAPIView):
    """Resend activation email to user"""

    serializer_class = ActivateResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivateResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        """Generate tokens for a user"""

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

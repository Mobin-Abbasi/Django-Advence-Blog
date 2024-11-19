from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer, CustomAuthTokenSerializer


class RegistrationAPIView(generics.GenericAPIView):
    """Serializer for registration"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Registering a new user"""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"email": serializer.validated_data["email"]}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

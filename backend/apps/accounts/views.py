from rest_framework import permissions

from apps.common.responses import success_response
from .serializers import LoginSerializer, LogoutSerializer
from .services import login_user, logout_user

from rest_framework.views import APIView


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_data = login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        user = auth_data["user"]

        return success_response(
            message="Login successful.",
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "access": auth_data["access"],
                    "refresh": auth_data["refresh"],
                },
            },
        )


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return success_response(
            message="Authenticated user retrieved successfully.",
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logout_user(
            refresh_token=serializer.validated_data["refresh"],
        )

        return success_response(
            message="Logout successful.",
            data=None,
        )
from rest_framework import permissions
from rest_framework.views import APIView

from apps.common.responses import success_response

from .presenters import present_current_user, present_login
from .serializers import LoginSerializer, LogoutSerializer
from .services import login_user, logout_user

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)

from .services import (
    confirm_password_reset,
    login_user,
    logout_user,
    request_password_reset,
)


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_data = login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return success_response(
            message="Login successful.",
            data=present_login(auth_data),
        )


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(
            message="Authenticated user retrieved successfully.",
            data=present_current_user(request.user),
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

class PasswordResetRequestAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_reset(
            email=serializer.validated_data["email"],
        )

        return success_response(
            message="If the email exists, password reset instructions will be sent.",
            data=None,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirm_password_reset(
            token=serializer.validated_data["token"],
            password=serializer.validated_data["password"],
        )

        return success_response(
            message="Password has been reset successfully.",
            data=None,
        )
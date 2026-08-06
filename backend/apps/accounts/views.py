from rest_framework import permissions
from rest_framework.views import APIView

from apps.common.responses import success_response

from .presenters import present_current_user, present_login
from .serializers import LoginSerializer, LogoutSerializer
from .services import login_user, logout_user


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
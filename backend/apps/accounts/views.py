from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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

        user = auth_data["user"]

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": {
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
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "success": True,
                "message": "Authenticated user retrieved successfully.",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logout_user(
            refresh_token=serializer.validated_data["refresh"],
        )

        return Response(
            {
                "success": True,
                "message": "Logout successful.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
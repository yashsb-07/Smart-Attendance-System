from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer
from .services import login_user


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
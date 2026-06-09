from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from .serializers import (
    UserSerializer,
    LogoutSerializer,
    CustomTokenObtainPairSerializer
)


class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    permission_classes = [AllowAny]

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Logout successful"
            },
            status=status.HTTP_200_OK
        )


class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
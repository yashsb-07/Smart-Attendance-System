from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        ]

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def save(self):

        refresh_token = self.validated_data['refresh']

        token = RefreshToken(refresh_token)

        token.blacklist()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):

        data = super().validate(attrs)

        data['user'] = UserSerializer(self.user).data

        return data
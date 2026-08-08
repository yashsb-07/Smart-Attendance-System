from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        min_length=8,
        style={"input_type": "password"},
    )

    def validate_password(self, value):
        validate_password(value)
        return value


class EmailVerificationConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmailVerificationRequestSerializer(serializers.Serializer):
    pass

class SessionValidationSerializer(serializers.Serializer):
    """
    Validate an access token and confirm that the session is valid.
    """

    token = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_token(self, value):
        try:
            AccessToken(value)
        except TokenError:
            raise AuthenticationFailed(
                "Invalid or expired access token."
            )

        return value
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .models import Role, User


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


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        )

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
        )

    def validate_email(self, value):
        queryset = User.objects.filter(
            email__iexact=value,
        ).exclude(
            pk=self.instance.pk,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_username(self, value):
        queryset = User.objects.filter(
            username__iexact=value,
        ).exclude(
            pk=self.instance.pk,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        queryset = User.objects.filter(
            email__iexact=value,
        ).exclude(
            pk=self.instance.pk,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value

    def validate_username(self, value):
        queryset = User.objects.filter(
            username__iexact=value,
        ).exclude(
            pk=self.instance.pk,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )

        return value


class UserStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class UserRoleSerializer(serializers.Serializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
    )
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.responses import success_response

from .models import User
from .permissions import IsSuperAdministrator
from .presenters import (
    present_current_user,
    present_login,
    present_managed_user,
)
from .selectors import list_users
from .serializers import (
    EmailVerificationConfirmSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    SessionValidationSerializer,
    UserCreateSerializer,
    UserProfileUpdateSerializer,
    UserRoleSerializer,
    UserStatusSerializer,
    UserUpdateSerializer,
)
from .services import (
    confirm_email_verification,
    confirm_password_reset,
    delete_user,
    login_user,
    logout_user,
    request_email_verification,
    request_password_reset,
    update_user,
    update_user_profile,
    update_user_role,
    update_user_status,
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
        serializer = PasswordResetRequestSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        request_password_reset(
            email=serializer.validated_data["email"],
        )

        return success_response(
            message=(
                "If the email exists, password reset instructions "
                "will be sent."
            ),
            data=None,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        confirm_password_reset(
            token=serializer.validated_data["token"],
            password=serializer.validated_data["password"],
        )

        return success_response(
            message="Password has been reset successfully.",
            data=None,
        )


class EmailVerificationRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request_email_verification(
            user=request.user,
        )

        return success_response(
            message="Email verification instructions have been sent.",
            data=None,
        )


class EmailVerificationConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        confirm_email_verification(
            token=serializer.validated_data["token"],
        )

        return success_response(
            message="Email address verified successfully.",
            data=None,
        )


class SessionValidationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SessionValidationSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Session is valid.",
            data=None,
        )


class UserListCreateAPIView(APIView):
    """
    Administrative User Management endpoint.

    GET:
        List users.

    POST:
        Create a user.
    """

    permission_classes = [IsSuperAdministrator]

    def get(self, request):
        users = list_users()

        data = [
            present_managed_user(user)
            for user in users
        ]

        return success_response(
            message="Users retrieved successfully.",
            data=data,
        )

    def post(self, request):
        serializer = UserCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return success_response(
            message="User created successfully.",
            data=present_managed_user(user),
            status_code=status.HTTP_201_CREATED,
        )


class UserDetailAPIView(APIView):
    """
    Administrative User Management endpoint for a single user.
    """

    permission_classes = [IsSuperAdministrator]

    def get_user(self, user_id):
        return get_object_or_404(
            User.objects.select_related("role"),
            pk=user_id,
        )

    def get(self, request, user_id):
        user = self.get_user(user_id)

        return success_response(
            message="User retrieved successfully.",
            data=present_managed_user(user),
        )

    def patch(self, request, user_id):
        user = self.get_user(user_id)

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        user = update_user(
            user=user,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="User updated successfully.",
            data=present_managed_user(user),
        )

    def delete(self, request, user_id):
        user = self.get_user(user_id)

        delete_user(user=user)

        return success_response(
            message="User deleted successfully.",
            data=None,
        )


class UserStatusAPIView(APIView):
    """
    Activate or deactivate a user account.
    """

    permission_classes = [IsSuperAdministrator]

    def patch(self, request, user_id):
        user = get_object_or_404(
            User.objects.select_related("role"),
            pk=user_id,
        )

        serializer = UserStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = update_user_status(
            user=user,
            is_active=serializer.validated_data["is_active"],
        )

        return success_response(
            message="User status updated successfully.",
            data=present_managed_user(user),
        )


class UserRoleAPIView(APIView):
    """
    Assign exactly one role to a user.
    """

    permission_classes = [IsSuperAdministrator]

    def patch(self, request, user_id):
        user = get_object_or_404(
            User.objects.select_related("role"),
            pk=user_id,
        )

        serializer = UserRoleSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = update_user_role(
            user=user,
            role=serializer.validated_data["role"],
        )

        return success_response(
            message="User role updated successfully.",
            data=present_managed_user(user),
        )


class UserProfileAPIView(APIView):
    """
    Self-service profile management.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(
            message="Profile retrieved successfully.",
            data=present_current_user(request.user),
        )

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        user = update_user_profile(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Profile updated successfully.",
            data=present_current_user(user),
        )
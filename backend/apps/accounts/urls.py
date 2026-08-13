from django.urls import path

from .views import (
    CurrentUserAPIView,
    EmailVerificationConfirmAPIView,
    EmailVerificationRequestAPIView,
    LoginAPIView,
    LogoutAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    SessionValidationAPIView,
    UserDetailAPIView,
    UserListCreateAPIView,
    UserProfileAPIView,
    UserRoleAPIView,
    UserStatusAPIView,
)


app_name = "accounts"


urlpatterns = [
    # Authentication
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),
    path(
        "password-reset/",
        PasswordResetRequestAPIView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "email-verification/",
        EmailVerificationRequestAPIView.as_view(),
        name="email-verification",
    ),
    path(
        "email-verification/confirm/",
        EmailVerificationConfirmAPIView.as_view(),
        name="email-verification-confirm",
    ),
    path(
        "session/validate/",
        SessionValidationAPIView.as_view(),
        name="session-validate",
    ),

    # User Management
    path(
        "users/",
        UserListCreateAPIView.as_view(),
        name="user-list-create",
    ),
    path(
        "users/<int:user_id>/",
        UserDetailAPIView.as_view(),
        name="user-detail",
    ),
    path(
        "users/<int:user_id>/status/",
        UserStatusAPIView.as_view(),
        name="user-status",
    ),
    path(
        "users/<int:user_id>/role/",
        UserRoleAPIView.as_view(),
        name="user-role",
    ),
    path(
        "users/profile/",
        UserProfileAPIView.as_view(),
        name="user-profile",
    ),
]
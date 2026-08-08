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
)


app_name = "accounts"


urlpatterns = [
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
]
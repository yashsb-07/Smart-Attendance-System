from django.urls import path

from .views import (
    CurrentUserAPIView,
    LoginAPIView,
    LogoutAPIView,
)

from .views import (
    CurrentUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
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
]
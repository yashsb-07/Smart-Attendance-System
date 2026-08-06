from django.urls import path

from .views import LoginAPIView, CurrentUserAPIView

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),
]
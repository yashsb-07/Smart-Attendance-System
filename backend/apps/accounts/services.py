from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def login_user(*, email: str, password: str) -> dict:
    user = authenticate(
        username=email,
        password=password,
    )

    if user is None:
        raise AuthenticationFailed("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationFailed("This account is inactive.")

    refresh = RefreshToken.for_user(user)

    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def logout_user(*, refresh_token: str) -> None:
    token = RefreshToken(refresh_token)
    token.blacklist()

def request_password_reset(*, email: str) -> None:
    """
    Password reset request service.

    Token generation and email delivery will be implemented
    in the next steps.
    """
    pass


def confirm_password_reset(*, token: str, password: str) -> None:
    """
    Password reset confirmation service.

    Token validation and password update will be implemented
    in the next steps.
    """
    pass
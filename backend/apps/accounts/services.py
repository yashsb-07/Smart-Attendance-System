from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def login_user(*, email: str, password: str) -> dict:
    """
    Authenticate a user and generate JWT tokens.

    Returns:
        dict: Authenticated user and JWT tokens.
    """

    user = authenticate(
        username=email,
        password=password,
    )

    if user is None:
        raise AuthenticationFailed(
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise AuthenticationFailed(
            detail="This account is inactive."
        )

    refresh = RefreshToken.for_user(user)

    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
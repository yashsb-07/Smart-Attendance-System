from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from .models import User


password_reset_token_generator = PasswordResetTokenGenerator()


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
    Generate a password reset token and send it to the user's email.

    The service intentionally does not expose whether the supplied
    email address exists in the system.
    """
    user = User.objects.filter(
        email__iexact=email,
        is_active=True,
    ).first()

    if user is None:
        return

    uid = urlsafe_base64_encode(
        force_bytes(user.pk),
    )

    token = password_reset_token_generator.make_token(user)

    reset_token = f"{uid}:{token}"

    send_mail(
        subject="Password Reset Request",
        message=(
            "A password reset was requested for your account.\n\n"
            "Use the following password reset token to continue:\n\n"
            f"{reset_token}\n\n"
            "If you did not request this password reset, "
            "you can safely ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def confirm_password_reset(*, token: str, password: str) -> None:
    """
    Validate the password reset token and update the user's password.
    """
    try:
        uid, reset_token = token.split(":", 1)
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(
            pk=user_id,
            is_active=True,
        )
    except (
        ValueError,
        TypeError,
        UnicodeDecodeError,
        User.DoesNotExist,
    ):
        raise ValidationError(
            {"token": "Invalid or expired password reset token."}
        )

    if not password_reset_token_generator.check_token(
        user,
        reset_token,
    ):
        raise ValidationError(
            {"token": "Invalid or expired password reset token."}
        )

    user.set_password(password)
    user.save(
        update_fields=["password"],
    )
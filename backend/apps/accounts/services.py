from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


password_reset_token_generator = PasswordResetTokenGenerator()
email_verification_token_generator = PasswordResetTokenGenerator()


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


def request_email_verification(*, user: User) -> None:
    """
    Generate an email verification token and send it to the
    authenticated user's email address.
    """
    if user.email_verified:
        return

    uid = urlsafe_base64_encode(
        force_bytes(user.pk),
    )

    token = email_verification_token_generator.make_token(user)

    verification_token = f"{uid}:{token}"

    send_mail(
        subject="Verify Your Email Address",
        message=(
            "Please verify your email address for your "
            "Smart Campus account.\n\n"
            "Use the following verification token to continue:\n\n"
            f"{verification_token}\n\n"
            "If you did not request this verification, "
            "you can safely ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def confirm_email_verification(*, token: str) -> None:
    """
    Validate the email verification token and mark the user's
    email address as verified.
    """
    try:
        uid, verification_token = token.split(":", 1)

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
            {"token": "Invalid or expired email verification token."}
        )

    if user.email_verified:
        raise ValidationError(
            {"token": "Email address is already verified."}
        )

    if not email_verification_token_generator.check_token(
        user,
        verification_token,
    ):
        raise ValidationError(
            {"token": "Invalid or expired email verification token."}
        )

    user.email_verified = True

    user.save(
        update_fields=["email_verified"],
    )


@transaction.atomic
def update_user(*, user: User, validated_data: dict) -> User:
    """
    Update an administratively managed user.
    """
    email_changed = (
        "email" in validated_data
        and validated_data["email"].lower() != user.email.lower()
    )

    for field, value in validated_data.items():
        setattr(user, field, value)

    if email_changed:
        user.email_verified = False

    update_fields = list(validated_data.keys())

    if email_changed:
        update_fields.append("email_verified")

    user.save(
        update_fields=update_fields,
    )

    return user


@transaction.atomic
def update_user_profile(*, user: User, validated_data: dict) -> User:
    """
    Update the authenticated user's own profile.
    """
    email_changed = (
        "email" in validated_data
        and validated_data["email"].lower() != user.email.lower()
    )

    for field, value in validated_data.items():
        setattr(user, field, value)

    if email_changed:
        user.email_verified = False

    update_fields = list(validated_data.keys())

    if email_changed:
        update_fields.append("email_verified")

    user.save(
        update_fields=update_fields,
    )

    return user


def update_user_status(*, user: User, is_active: bool) -> User:
    user.is_active = is_active

    user.save(
        update_fields=["is_active"],
    )

    return user


def update_user_role(*, user: User, role) -> User:
    user.role = role

    user.save(
        update_fields=["role"],
    )

    return user


def delete_user(*, user: User) -> None:
    user.delete()
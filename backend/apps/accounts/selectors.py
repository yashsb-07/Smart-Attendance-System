from django.db.models import QuerySet

from .models import User


def get_user_by_id(*, user_id: int) -> User:
    return User.objects.select_related("role").get(
        pk=user_id,
    )


def list_users() -> QuerySet:
    return (
        User.objects
        .select_related("role")
        .order_by("id")
    )
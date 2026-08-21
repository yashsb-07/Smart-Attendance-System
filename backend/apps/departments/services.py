from django.db import transaction
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import ValidationError

from .models import Department


@transaction.atomic
def create_department(*, validated_data: dict) -> Department:
    return Department.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_department(
    *,
    department: Department,
    validated_data: dict,
) -> Department:
    for field, value in validated_data.items():
        setattr(
            department,
            field,
            value,
        )

    department.save()

    return department


@transaction.atomic
def delete_department(
    *,
    department: Department,
) -> None:
    try:
        department.delete()
    except ProtectedError:
        raise ValidationError(
            {
                "department": (
                    "This department cannot be deleted because "
                    "dependent records exist."
                )
            }
        )
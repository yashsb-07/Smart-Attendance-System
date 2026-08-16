from django.db import transaction
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import ValidationError

from .models import Institution


@transaction.atomic
def create_institution(*, validated_data: dict) -> Institution:
    return Institution.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_institution(
    *,
    institution: Institution,
    validated_data: dict,
) -> Institution:
    for field, value in validated_data.items():
        setattr(
            institution,
            field,
            value,
        )

    institution.save()

    return institution


@transaction.atomic
def delete_institution(
    *,
    institution: Institution,
) -> None:
    try:
        institution.delete()
    except ProtectedError:
        raise ValidationError(
            {
                "institution": (
                    "This institution cannot be deleted because "
                    "dependent records exist."
                )
            }
        )
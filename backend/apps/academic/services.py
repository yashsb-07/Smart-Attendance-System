from django.db import transaction

from .models import AcademicYear


@transaction.atomic
def create_academic_year(
    *,
    validated_data: dict,
) -> AcademicYear:
    return AcademicYear.objects.create(
        **validated_data,
    )


@transaction.atomic
def update_academic_year(
    *,
    academic_year: AcademicYear,
    validated_data: dict,
) -> AcademicYear:
    for field, value in validated_data.items():
        setattr(
            academic_year,
            field,
            value,
        )

    academic_year.save()

    return academic_year
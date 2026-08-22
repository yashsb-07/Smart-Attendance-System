from django.db import models
from django.db.models import F, Q

from apps.institutions.models import Institution


class AcademicYear(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="academic_years",
    )

    name = models.CharField(
        max_length=50,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_current = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "academic_years"
        ordering = [
            "institution_id",
            "start_date",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "institution",
                    "name",
                ],
                name="academic_year_institution_name_uniq",
            ),
            models.CheckConstraint(
                condition=Q(
                    end_date__gt=F("start_date"),
                ),
                name="academic_year_valid_dates",
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.institution.name}"
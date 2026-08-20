from django.db import models

from apps.institutions.models import Institution


class Department(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="departments",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
        null=True,
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
        db_table = "departments"
        ordering = [
            "institution_id",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "institution",
                    "code",
                ],
                name="department_institution_code_uniq",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "institution",
                ],
                name="department_institution_idx",
            ),
            models.Index(
                fields=[
                    "institution",
                    "is_active",
                ],
                name="dept_institution_active_idx",
            ),
            models.Index(
                fields=[
                    "institution",
                    "name",
                ],
                name="dept_institution_name_idx",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
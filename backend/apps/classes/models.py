from django.db import models
from apps.departments.models import Department

# Create your models here
class Class(models.Model):

    department = models.ForeignKey(  #Each class belongs to one department.
        Department,
        on_delete=models.CASCADE,
        related_name="classes"
    )

    name = models.CharField(
        max_length=100
    )

    section = models.CharField(
        max_length=50
    )

    academic_year = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.name} - {self.section}"
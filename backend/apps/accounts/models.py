from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class Role(models.Model):
    class RoleName(models.TextChoices):
        SUPER_ADMINISTRATOR = (
            "super_administrator",
            "Super Administrator",
        )
        INSTITUTION_ADMINISTRATOR = (
            "institution_administrator",
            "Institution Administrator",
        )
        FACULTY = "faculty", "Faculty"
        STUDENT = "student", "Student"

    name = models.CharField(
        max_length=50,
        choices=RoleName.choices,
        unique=True,
    )

    class Meta:
        db_table = "roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["id"]

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    email = models.EmailField(unique=True)

    email_verified = models.BooleanField(
        default=False,
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
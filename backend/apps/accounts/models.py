from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model.

    Additional fields will be added in future modules
    (Institution, Role, Profile, etc.).
    """

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
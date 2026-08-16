from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

    description = models.TextField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "institutions"
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=["is_active"],
                name="institution_active_idx",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
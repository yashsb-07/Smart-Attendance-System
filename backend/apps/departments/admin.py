from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "institution",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "institution",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "institution__name",
    )

    ordering = (
        "institution",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
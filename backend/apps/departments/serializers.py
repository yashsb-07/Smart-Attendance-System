from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "institution",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

        validators = []

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Department name cannot be empty."
            )

        return value

    def validate_code(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Department code cannot be empty."
            )

        return value

    def validate_description(self, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            return None

        return value

    def validate(self, attrs):
        institution = attrs.get(
            "institution",
            getattr(
                self.instance,
                "institution",
                None,
            ),
        )

        code = attrs.get(
            "code",
            getattr(
                self.instance,
                "code",
                None,
            ),
        )

        if institution is not None and code:
            queryset = Department.objects.filter(
                institution=institution,
                code=code,
            )

            if self.instance is not None:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "code": (
                            "A department with this code "
                            "already exists in this institution."
                        )
                    }
                )

        return attrs
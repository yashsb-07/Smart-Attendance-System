from rest_framework import serializers

from .models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            "id",
            "name",
            "code",
            "description",
            "email",
            "phone",
            "address",
            "website",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Institution name cannot be empty."
            )

        return value

    def validate_code(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Institution code cannot be empty."
            )

        queryset = Institution.objects.filter(
            code__iexact=value,
        )

        if self.instance is not None:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "An institution with this code already exists."
            )

        return value
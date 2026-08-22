from rest_framework import serializers

from .models import AcademicYear


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "institution",
            "name",
            "start_date",
            "end_date",
            "is_current",
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
                "Academic year name cannot be empty."
            )

        return value

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(
                self.instance,
                "start_date",
                None,
            ),
        )

        end_date = attrs.get(
            "end_date",
            getattr(
                self.instance,
                "end_date",
                None,
            ),
        )

        if (
            start_date is not None
            and end_date is not None
            and end_date <= start_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "End date must be later than start date."
                    )
                }
            )

        institution = attrs.get(
            "institution",
            getattr(
                self.instance,
                "institution",
                None,
            ),
        )

        name = attrs.get(
            "name",
            getattr(
                self.instance,
                "name",
                None,
            ),
        )

        if institution is not None and name:
            queryset = AcademicYear.objects.filter(
                institution=institution,
                name=name,
            )

            if self.instance is not None:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "name": (
                            "An academic year with this name "
                            "already exists in this institution."
                        )
                    }
                )

        return attrs
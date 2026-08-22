from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from apps.common.responses import success_response

from .models import AcademicYear
from .permissions import CanManageAcademicYears
from .presenters import present_academic_year
from .selectors import list_academic_years
from .serializers import AcademicYearSerializer
from .services import (
    create_academic_year,
    update_academic_year,
)


class AcademicYearListCreateAPIView(APIView):
    permission_classes = [CanManageAcademicYears]

    def get(self, request):
        academic_years = list_academic_years()

        data = [
            present_academic_year(
                academic_year,
            )
            for academic_year in academic_years
        ]

        return success_response(
            message="Academic years retrieved successfully.",
            data=data,
        )

    def post(self, request):
        serializer = AcademicYearSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        academic_year = create_academic_year(
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Academic year created successfully.",
            data=present_academic_year(
                academic_year,
            ),
            status_code=status.HTTP_201_CREATED,
        )


class AcademicYearDetailAPIView(APIView):
    permission_classes = [CanManageAcademicYears]

    def get_academic_year(self, academic_year_id):
        return get_object_or_404(
            AcademicYear,
            pk=academic_year_id,
        )

    def get(self, request, academic_year_id):
        academic_year = self.get_academic_year(
            academic_year_id,
        )

        return success_response(
            message="Academic year retrieved successfully.",
            data=present_academic_year(
                academic_year,
            ),
        )

    def put(self, request, academic_year_id):
        academic_year = self.get_academic_year(
            academic_year_id,
        )

        serializer = AcademicYearSerializer(
            academic_year,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        academic_year = update_academic_year(
            academic_year=academic_year,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Academic year updated successfully.",
            data=present_academic_year(
                academic_year,
            ),
        )

    def patch(self, request, academic_year_id):
        academic_year = self.get_academic_year(
            academic_year_id,
        )

        serializer = AcademicYearSerializer(
            academic_year,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        academic_year = update_academic_year(
            academic_year=academic_year,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Academic year updated successfully.",
            data=present_academic_year(
                academic_year,
            ),
        )
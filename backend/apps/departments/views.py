from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.responses import success_response

from .models import Department
from .presenters import present_department
from .selectors import list_departments
from .serializers import DepartmentSerializer
from .services import (
    create_department,
    delete_department,
    update_department,
)


class DepartmentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = list_departments()

        data = [
            present_department(department)
            for department in departments
        ]

        return success_response(
            message="Departments retrieved successfully.",
            data=data,
        )

    def post(self, request):
        serializer = DepartmentSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        department = create_department(
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Department created successfully.",
            data=present_department(department),
            status_code=status.HTTP_201_CREATED,
        )


class DepartmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_department(self, department_id):
        return get_object_or_404(
            Department,
            pk=department_id,
        )

    def get(self, request, department_id):
        department = self.get_department(
            department_id,
        )

        return success_response(
            message="Department retrieved successfully.",
            data=present_department(department),
        )

    def put(self, request, department_id):
        department = self.get_department(
            department_id,
        )

        serializer = DepartmentSerializer(
            department,
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        department = update_department(
            department=department,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Department updated successfully.",
            data=present_department(department),
        )

    def patch(self, request, department_id):
        department = self.get_department(
            department_id,
        )

        serializer = DepartmentSerializer(
            department,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        department = update_department(
            department=department,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Department updated successfully.",
            data=present_department(department),
        )

    def delete(self, request, department_id):
        department = self.get_department(
            department_id,
        )

        delete_department(
            department=department,
        )

        return success_response(
            message="Department deleted successfully.",
            data=None,
        )
from django.db import IntegrityError
from django.test import TestCase

from apps.institutions.models import Institution

from .models import Department
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import Role, User



class DepartmentModelTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

    def test_create_department(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
            description="Computer Science Department",
        )

        self.assertEqual(
            department.name,
            "Computer Science",
        )

        self.assertEqual(
            department.code,
            "CSE",
        )

        self.assertEqual(
            department.institution,
            self.institution,
        )

        self.assertTrue(
            department.is_active,
        )

    def test_department_code_is_unique_within_institution(self):
        Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        with self.assertRaises(IntegrityError):
            Department.objects.create(
                institution=self.institution,
                name="Information Technology",
                code="CSE",
            )

    def test_same_code_is_allowed_for_different_institutions(self):
        second_institution = Institution.objects.create(
            name="Second Institution",
            code="TEST002",
        )

        Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        department = Department.objects.create(
            institution=second_institution,
            name="Computer Science",
            code="CSE",
        )

        self.assertEqual(
            department.code,
            "CSE",
        )

    def test_department_is_active_by_default(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        self.assertTrue(
            department.is_active,
        )

    def test_department_string_representation(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        self.assertEqual(
            str(department),
            "Computer Science (CSE)",
        )

class DepartmentAPITests(APITestCase):
    def setUp(self):
        self.role = Role.objects.get(
            name=Role.RoleName.SUPER_ADMINISTRATOR,
        )

        self.user = User.objects.create_user(
            email="superadmin@example.com",
            password="TestPassword123!",
            username="superadmin",
            role=self.role,
        )

        refresh = RefreshToken.for_user(self.user)

        self.access_token = str(
            refresh.access_token,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {self.access_token}"
            ),
        )

        self.institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

    def create_department(self, **overrides):
        data = {
            "institution": self.institution.id,
            "name": "Computer Science",
            "code": "CSE",
            "description": "Computer Science Department",
            "is_active": True,
        }

        data.update(overrides)

        response = self.client.post(
            "/api/v1/departments/",
            data,
            format="json",
        )

        return response

    def test_create_department(self):
        response = self.create_department()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["name"],
            "Computer Science",
        )

        self.assertEqual(
            response.data["data"]["code"],
            "CSE",
        )

    def test_list_departments(self):
        Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            len(response.data["data"]),
            1,
        )

    def test_retrieve_department(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        response = self.client.get(
            f"/api/v1/departments/{department.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["id"],
            department.id,
        )

    def test_update_department(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        response = self.client.put(
            f"/api/v1/departments/{department.id}/",
            {
                "institution": self.institution.id,
                "name": "Information Technology",
                "code": "IT",
                "description": "IT Department",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        department.refresh_from_db()

        self.assertEqual(
            department.name,
            "Information Technology",
        )

        self.assertEqual(
            department.code,
            "IT",
        )

    def test_partial_update_department(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        response = self.client.patch(
            f"/api/v1/departments/{department.id}/",
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        department.refresh_from_db()

        self.assertFalse(
            department.is_active,
        )

    def test_delete_department(self):
        department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        response = self.client.delete(
            f"/api/v1/departments/{department.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            Department.objects.filter(
                pk=department.id,
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class DepartmentPermissionTests(APITestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

        self.department = Department.objects.create(
            institution=self.institution,
            name="Computer Science",
            code="CSE",
        )

        self.super_admin_role = Role.objects.get(
            name=Role.RoleName.SUPER_ADMINISTRATOR,
        )

        self.institution_admin_role = Role.objects.get(
            name=Role.RoleName.INSTITUTION_ADMINISTRATOR,
        )

        self.faculty_role = Role.objects.get(
            name=Role.RoleName.FACULTY,
        )

        self.student_role = Role.objects.get(
            name=Role.RoleName.STUDENT,
        )

    def authenticate_as(self, role):
        user = User.objects.create_user(
            email=f"{role.name}@example.com",
            password="TestPassword123!",
            username=role.name,
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

    def test_super_administrator_can_list_departments(self):
        self.authenticate_as(
            self.super_admin_role,
        )

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_institution_administrator_cannot_manage_departments_yet(self):
        self.authenticate_as(
            self.institution_admin_role,
        )

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_faculty_cannot_manage_departments(self):
        self.authenticate_as(
            self.faculty_role,
        )

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_cannot_manage_departments(self):
        self.authenticate_as(
            self.student_role,
        )

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_manage_departments(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/departments/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
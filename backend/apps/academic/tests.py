from datetime import date

from django.db import IntegrityError
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Role, User
from apps.institutions.models import Institution

from .models import AcademicYear


class AcademicYearModelTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

    def test_create_academic_year(self):
        academic_year = AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        self.assertEqual(
            academic_year.name,
            "2026-2027",
        )

        self.assertEqual(
            academic_year.institution,
            self.institution,
        )

        self.assertTrue(
            academic_year.is_active,
        )

        self.assertFalse(
            academic_year.is_current,
        )

    def test_academic_year_name_is_unique_within_institution(self):
        AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        with self.assertRaises(IntegrityError):
            AcademicYear.objects.create(
                institution=self.institution,
                name="2026-2027",
                start_date=date(2026, 7, 1),
                end_date=date(2027, 6, 30),
            )

    def test_same_name_is_allowed_for_different_institutions(self):
        second_institution = Institution.objects.create(
            name="Second Institution",
            code="TEST002",
        )

        AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        academic_year = AcademicYear.objects.create(
            institution=second_institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        self.assertEqual(
            academic_year.name,
            "2026-2027",
        )

    def test_invalid_date_range_is_rejected_by_database(self):
        with self.assertRaises(IntegrityError):
            AcademicYear.objects.create(
                institution=self.institution,
                name="2026-2027",
                start_date=date(2027, 5, 31),
                end_date=date(2026, 6, 1),
            )

    def test_academic_year_string_representation(self):
        academic_year = AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        self.assertEqual(
            str(academic_year),
            "2026-2027 - Test Institution",
        )


class AcademicYearAPITests(APITestCase):
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

        refresh = RefreshToken.for_user(
            self.user,
        )

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

    def create_academic_year(self, **overrides):
        data = {
            "institution": self.institution.id,
            "name": "2026-2027",
            "start_date": "2026-06-01",
            "end_date": "2027-05-31",
            "is_current": False,
            "is_active": True,
        }

        data.update(overrides)

        return self.client.post(
            "/api/v1/academic-years/",
            data,
            format="json",
        )

    def test_create_academic_year(self):
        response = self.create_academic_year()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["name"],
            "2026-2027",
        )

    def test_list_academic_years(self):
        AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        response = self.client.get(
            "/api/v1/academic-years/",
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

    def test_retrieve_academic_year(self):
        academic_year = AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        response = self.client.get(
            f"/api/v1/academic-years/{academic_year.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["id"],
            academic_year.id,
        )

    def test_update_academic_year(self):
        academic_year = AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        response = self.client.put(
            f"/api/v1/academic-years/{academic_year.id}/",
            {
                "institution": self.institution.id,
                "name": "2026-2028",
                "start_date": "2026-06-01",
                "end_date": "2028-05-31",
                "is_current": True,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        academic_year.refresh_from_db()

        self.assertEqual(
            academic_year.name,
            "2026-2028",
        )

        self.assertTrue(
            academic_year.is_current,
        )

    def test_partial_update_academic_year(self):
        academic_year = AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        response = self.client.patch(
            f"/api/v1/academic-years/{academic_year.id}/",
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        academic_year.refresh_from_db()

        self.assertFalse(
            academic_year.is_active,
        )

    def test_create_academic_year_rejects_invalid_date_range(self):
        response = self.create_academic_year(
            start_date="2027-05-31",
            end_date="2026-06-01",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            response.data["success"],
        )

        self.assertIn(
            "end_date",
            response.data["errors"],
        )

    def test_create_academic_year_rejects_duplicate_name(self):
        AcademicYear.objects.create(
            institution=self.institution,
            name="2026-2027",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 5, 31),
        )

        response = self.create_academic_year()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            response.data["success"],
        )

        self.assertIn(
            "name",
            response.data["errors"],
        )

    def test_create_academic_year_rejects_invalid_institution(self):
        response = self.create_academic_year(
            institution=999999,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            response.data["success"],
        )

        self.assertIn(
            "institution",
            response.data["errors"],
        )

    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/academic-years/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_institution_administrator_cannot_manage_academic_years_yet(
        self,
    ):
        role = Role.objects.get(
            name=Role.RoleName.INSTITUTION_ADMINISTRATOR,
        )

        user = User.objects.create_user(
            email="institutionadmin@example.com",
            password="TestPassword123!",
            username="institutionadmin",
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

        response = self.client.get(
            "/api/v1/academic-years/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_faculty_cannot_manage_academic_years(self):
        role = Role.objects.get(
            name=Role.RoleName.FACULTY,
        )

        user = User.objects.create_user(
            email="faculty@example.com",
            password="TestPassword123!",
            username="faculty",
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

        response = self.client.get(
            "/api/v1/academic-years/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_cannot_manage_academic_years(self):
        role = Role.objects.get(
            name=Role.RoleName.STUDENT,
        )

        user = User.objects.create_user(
            email="student@example.com",
            password="TestPassword123!",
            username="student",
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

        response = self.client.get(
            "/api/v1/academic-years/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nonexistent_academic_year_returns_not_found(self):
        response = self.client.get(
            "/api/v1/academic-years/999999/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertFalse(
            response.data["success"],
        )
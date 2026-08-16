from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Role, User

from .models import Institution


class InstitutionAPITests(APITestCase):
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

    def create_institution(self, **overrides):
        data = {
            "name": "Test Institution",
            "code": "TEST001",
            "description": "Test institution",
            "email": "admin@test.edu",
            "phone": "+911234567890",
            "address": "Test Address",
            "website": "https://test.edu",
            "is_active": True,
        }

        data.update(overrides)

        response = self.client.post(
            "/api/v1/institutions/",
            data,
            format="json",
        )

        return response

    def test_create_institution(self):
        response = self.create_institution()

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            response.data["success"],
        )

        self.assertEqual(
            response.data["data"]["code"],
            "TEST001",
        )

        self.assertEqual(
            Institution.objects.count(),
            1,
        )

    def test_list_institutions(self):
        Institution.objects.create(
            name="Institution One",
            code="INST001",
        )

        Institution.objects.create(
            name="Institution Two",
            code="INST002",
        )

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data["data"]),
            2,
        )

    def test_get_specific_institution(self):
        institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

        response = self.client.get(
            f"/api/v1/institutions/{institution.id}/",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["data"]["id"],
            institution.id,
        )

    def test_update_institution(self):
        institution = Institution.objects.create(
            name="Old Institution",
            code="OLD001",
        )

        response = self.client.patch(
            f"/api/v1/institutions/{institution.id}/",
            {
                "name": "Updated Institution",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        institution.refresh_from_db()

        self.assertEqual(
            institution.name,
            "Updated Institution",
        )

    def test_delete_institution(self):
        institution = Institution.objects.create(
            name="Delete Institution",
            code="DELETE001",
        )

        response = self.client.delete(
            f"/api/v1/institutions/{institution.id}/",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse(
            Institution.objects.filter(
                pk=institution.id,
            ).exists()
        )

    def test_duplicate_code_is_rejected(self):
        Institution.objects.create(
            name="Institution One",
            code="DUP001",
        )

        response = self.create_institution(
            code="dup001",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_non_super_administrator_is_rejected(self):
        faculty_role = Role.objects.get(
            name=Role.RoleName.FACULTY,
        )

        faculty = User.objects.create_user(
            email="faculty@example.com",
            password="TestPassword123!",
            username="faculty",
            role=faculty_role,
        )

        refresh = RefreshToken.for_user(faculty)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_unauthenticated_request_is_rejected(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            401,
        )


class InstitutionModelConstraintTests(TestCase):
    def test_institution_code_is_unique(self):
        Institution.objects.create(
            name="Institution One",
            code="INST001",
        )

        with self.assertRaises(Exception):
            Institution.objects.create(
                name="Institution Two",
                code="INST001",
            )
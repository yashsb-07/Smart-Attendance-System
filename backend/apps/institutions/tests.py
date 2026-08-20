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

class InstitutionPermissionTests(APITestCase):
    def create_user_with_role(self, role_name, email, username):
        role = Role.objects.get(
            name=role_name,
        )

        return User.objects.create_user(
            email=email,
            password="TestPassword123!",
            username=username,
            role=role,
        )

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

    def test_super_administrator_can_manage_institutions(self):
        user = self.create_user_with_role(
            Role.RoleName.SUPER_ADMINISTRATOR,
            "superadmin-rbac@example.com",
            "superadmin_rbac",
        )

        self.authenticate_user(user)

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_institution_administrator_cannot_manage_institutions(self):
        user = self.create_user_with_role(
            Role.RoleName.INSTITUTION_ADMINISTRATOR,
            "institutionadmin-rbac@example.com",
            "institutionadmin_rbac",
        )

        self.authenticate_user(user)

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_faculty_cannot_manage_institutions(self):
        user = self.create_user_with_role(
            Role.RoleName.FACULTY,
            "faculty-rbac@example.com",
            "faculty_rbac",
        )

        self.authenticate_user(user)

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_student_cannot_manage_institutions(self):
        user = self.create_user_with_role(
            Role.RoleName.STUDENT,
            "student-rbac@example.com",
            "student_rbac",
        )

        self.authenticate_user(user)

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_unauthenticated_user_cannot_manage_institutions(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/institutions/",
        )

        self.assertEqual(
            response.status_code,
            401,
        )

class InstitutionValidationTests(APITestCase):
    def setUp(self):
        role = Role.objects.get(
            name=Role.RoleName.SUPER_ADMINISTRATOR,
        )

        user = User.objects.create_user(
            email="validation-superadmin@example.com",
            password="TestPassword123!",
            username="validation_superadmin",
            role=role,
        )

        refresh = RefreshToken.for_user(user)

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {refresh.access_token}"
            ),
        )

    def test_empty_name_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "   ",
                "code": "VALID001",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_empty_code_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Valid Institution",
                "code": "   ",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_missing_name_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "code": "VALID002",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_missing_code_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Valid Institution",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_duplicate_code_is_rejected_case_insensitively(self):
        Institution.objects.create(
            name="Existing Institution",
            code="UNIQUE001",
        )

        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Another Institution",
                "code": "unique001",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Valid Institution",
                "code": "VALID003",
                "email": "not-an-email",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_invalid_website_is_rejected(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Valid Institution",
                "code": "VALID004",
                "website": "not-a-url",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_invalid_institution_id_returns_not_found(self):
        response = self.client.get(
            "/api/v1/institutions/999999/",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertFalse(
            response.data["success"],
        )

    def test_empty_optional_text_values_are_normalized(self):
        response = self.client.post(
            "/api/v1/institutions/",
            {
                "name": "Normalized Institution",
                "code": "VALID005",
                "description": "   ",
                "email": "   ",
                "phone": "   ",
                "address": "   ",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        institution = Institution.objects.get(
            code="VALID005",
        )

        self.assertIsNone(
            institution.description,
        )

        self.assertIsNone(
            institution.email,
        )

        self.assertIsNone(
            institution.phone,
        )

        self.assertIsNone(
            institution.address,
        )
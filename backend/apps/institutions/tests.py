from django.test import TestCase

from .models import Institution


class InstitutionModelTests(TestCase):
    def test_create_institution(self):
        institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
            email="admin@testinstitution.edu",
        )

        self.assertEqual(institution.name, "Test Institution")
        self.assertEqual(institution.code, "TEST001")
        self.assertTrue(institution.is_active)

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

    def test_institution_string_representation(self):
        institution = Institution.objects.create(
            name="Test Institution",
            code="TEST001",
        )

        self.assertEqual(
            str(institution),
            "Test Institution (TEST001)",
        )
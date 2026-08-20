from django.db import IntegrityError
from django.test import TestCase

from apps.institutions.models import Institution

from .models import Department


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
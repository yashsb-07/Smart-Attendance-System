from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .models import Role, User
from .permissions import (
    IsFaculty,
    IsInstitutionAdministrator,
    IsStudent,
    IsSuperAdministrator,
)


class RolePermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.roles = {
            Role.RoleName.SUPER_ADMINISTRATOR: Role.objects.get(
                name=Role.RoleName.SUPER_ADMINISTRATOR,
            ),
            Role.RoleName.INSTITUTION_ADMINISTRATOR: Role.objects.get(
                name=Role.RoleName.INSTITUTION_ADMINISTRATOR,
            ),
            Role.RoleName.FACULTY: Role.objects.get(
                name=Role.RoleName.FACULTY,
            ),
            Role.RoleName.STUDENT: Role.objects.get(
                name=Role.RoleName.STUDENT,
            ),
        }

    def create_user(self, role_name, **extra_fields):
        return User.objects.create_user(
            email=f"{role_name}@example.com",
            password="TestPassword123!",
            username=role_name,
            role=self.roles[role_name],
            **extra_fields,
        )

    def build_request(self, user):
        request = Request(
            self.factory.get("/"),
        )
        request.user = user
        return request

    def test_super_administrator_permission(self):
        user = self.create_user(
            Role.RoleName.SUPER_ADMINISTRATOR,
        )
        request = self.build_request(user)

        self.assertTrue(
            IsSuperAdministrator().has_permission(request, None)
        )

    def test_institution_administrator_permission(self):
        user = self.create_user(
            Role.RoleName.INSTITUTION_ADMINISTRATOR,
        )
        request = self.build_request(user)

        self.assertTrue(
            IsInstitutionAdministrator().has_permission(request, None)
        )

    def test_faculty_permission(self):
        user = self.create_user(
            Role.RoleName.FACULTY,
        )
        request = self.build_request(user)

        self.assertTrue(
            IsFaculty().has_permission(request, None)
        )

    def test_student_permission(self):
        user = self.create_user(
            Role.RoleName.STUDENT,
        )
        request = self.build_request(user)

        self.assertTrue(
            IsStudent().has_permission(request, None)
        )

    def test_role_permission_rejects_wrong_role(self):
        user = self.create_user(
            Role.RoleName.STUDENT,
        )
        request = self.build_request(user)

        self.assertFalse(
            IsFaculty().has_permission(request, None)
        )

        self.assertFalse(
            IsInstitutionAdministrator().has_permission(request, None)
        )

        self.assertFalse(
            IsSuperAdministrator().has_permission(request, None)
        )

    def test_role_permission_rejects_unauthenticated_user(self):
        request = self.build_request(
            AnonymousUser(),
        )

        self.assertFalse(
            IsStudent().has_permission(request, None)
        )

    def test_role_permission_rejects_inactive_user(self):
        user = self.create_user(
            Role.RoleName.STUDENT,
            is_active=False,
        )
        request = self.build_request(user)

        self.assertFalse(
            IsStudent().has_permission(request, None)
        )
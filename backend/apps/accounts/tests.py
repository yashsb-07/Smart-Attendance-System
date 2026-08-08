from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.test import TestCase, override_settings
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .models import Role, User
from .permissions import (
    IsFaculty,
    IsInstitutionAdministrator,
    IsStudent,
    IsSuperAdministrator,
)
from .services import (
    confirm_email_verification,
    confirm_password_reset,
    request_email_verification,
    request_password_reset,
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


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class PasswordResetTests(TestCase):
    def setUp(self):
        self.role = Role.objects.get(
            name=Role.RoleName.STUDENT,
        )

        self.user = User.objects.create_user(
            email="password-reset@example.com",
            password="OldPassword123!",
            username="password_reset_user",
            role=self.role,
        )

    def test_password_reset_request_sends_email(self):
        request_password_reset(
            email=self.user.email,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        self.assertEqual(
            mail.outbox[0].to,
            [self.user.email],
        )

        self.assertIn(
            "Password Reset Request",
            mail.outbox[0].subject,
        )

    def test_password_reset_request_does_not_reveal_unknown_email(self):
        request_password_reset(
            email="unknown@example.com",
        )

        self.assertEqual(
            len(mail.outbox),
            0,
        )

    def test_password_reset_confirmation_changes_password(self):
        request_password_reset(
            email=self.user.email,
        )

        reset_token = (
            mail.outbox[0]
            .body
            .split(
                "Use the following password reset token to continue:\n\n",
                1,
            )[1]
            .split("\n\n", 1)[0]
        )

        confirm_password_reset(
            token=reset_token,
            password="NewPassword123!",
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password("NewPassword123!")
        )

        self.assertFalse(
            self.user.check_password("OldPassword123!")
        )

    def test_password_reset_token_cannot_be_reused(self):
        request_password_reset(
            email=self.user.email,
        )

        reset_token = (
            mail.outbox[0]
            .body
            .split(
                "Use the following password reset token to continue:\n\n",
                1,
            )[1]
            .split("\n\n", 1)[0]
        )

        confirm_password_reset(
            token=reset_token,
            password="NewPassword123!",
        )

        with self.assertRaises(Exception):
            confirm_password_reset(
                token=reset_token,
                password="AnotherPassword123!",
            )


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class EmailVerificationTests(TestCase):
    def setUp(self):
        self.role = Role.objects.get(
            name=Role.RoleName.STUDENT,
        )

        self.user = User.objects.create_user(
            email="verification@example.com",
            password="TestPassword123!",
            username="verification_user",
            role=self.role,
        )

    def test_user_email_is_unverified_by_default(self):
        self.assertFalse(
            self.user.email_verified,
        )

    def test_email_verification_request_sends_email(self):
        request_email_verification(
            user=self.user,
        )

        self.assertEqual(
            len(mail.outbox),
            1,
        )

        self.assertEqual(
            mail.outbox[0].to,
            [self.user.email],
        )

        self.assertIn(
            "Verify Your Email Address",
            mail.outbox[0].subject,
        )

    def test_email_verification_confirmation_verifies_user(self):
        request_email_verification(
            user=self.user,
        )

        verification_token = (
            mail.outbox[0]
            .body
            .split(
                "Use the following verification token to continue:\n\n",
                1,
            )[1]
            .split("\n\n", 1)[0]
        )

        confirm_email_verification(
            token=verification_token,
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.email_verified,
        )

    def test_email_verification_token_cannot_be_reused(self):
        request_email_verification(
            user=self.user,
        )

        verification_token = (
            mail.outbox[0]
            .body
            .split(
                "Use the following verification token to continue:\n\n",
                1,
            )[1]
            .split("\n\n", 1)[0]
        )

        confirm_email_verification(
            token=verification_token,
        )

        with self.assertRaises(Exception):
            confirm_email_verification(
                token=verification_token,
            )

    def test_invalid_email_verification_token_is_rejected(self):
        with self.assertRaises(Exception):
            confirm_email_verification(
                token="invalid-token",
            )

    def test_verification_email_is_not_sent_again_after_verification(self):
        self.user.email_verified = True
        self.user.save(
            update_fields=["email_verified"],
        )

        request_email_verification(
            user=self.user,
        )

        self.assertEqual(
            len(mail.outbox),
            0,
        )
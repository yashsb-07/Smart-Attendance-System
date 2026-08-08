"""
Custom RBAC permissions for the Accounts module.
"""

from rest_framework.permissions import BasePermission

from .models import Role


class BaseRolePermission(BasePermission):
    """
    Base permission for role-based authorization.
    """

    allowed_roles = ()

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not user.is_active:
            return False

        if not user.role:
            return False

        return user.role.name in self.allowed_roles


class IsSuperAdministrator(BaseRolePermission):
    """
    Allows access only to Super Administrators.
    """

    allowed_roles = (
        Role.RoleName.SUPER_ADMINISTRATOR,
    )

    message = "Super Administrator role required."


class IsInstitutionAdministrator(BaseRolePermission):
    """
    Allows access only to Institution Administrators.
    """

    allowed_roles = (
        Role.RoleName.INSTITUTION_ADMINISTRATOR,
    )

    message = "Institution Administrator role required."


class IsFaculty(BaseRolePermission):
    """
    Allows access only to Faculty users.
    """

    allowed_roles = (
        Role.RoleName.FACULTY,
    )

    message = "Faculty role required."


class IsStudent(BaseRolePermission):
    """
    Allows access only to Student users.
    """

    allowed_roles = (
        Role.RoleName.STUDENT,
    )

    message = "Student role required."
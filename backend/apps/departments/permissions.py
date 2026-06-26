from rest_framework.permissions import BasePermission, SAFE_METHODS


class DepartmentPermission(
    BasePermission
):

    def has_permission(
        self,
        request,
        view
    ):

        if not request.user.is_authenticated:
            return False

        # Admin full access
        if request.user.role == "admin":
            return True

        # Teacher read only
        if (
            request.user.role == "teacher"
            and request.method in SAFE_METHODS
        ):
            return True

        # Student no access
        return False
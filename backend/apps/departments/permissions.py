from apps.accounts.permissions import IsSuperAdministrator


class CanManageDepartments(IsSuperAdministrator):
    """
    Permission for Department Management.

    Department Management is currently restricted to
    Super Administrators because the current User model
    does not contain an institution relationship required
    for institution-scoped authorization.
    """

    message = (
        "Super Administrator role required to manage departments."
    )
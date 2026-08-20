from apps.accounts.permissions import IsSuperAdministrator


class CanManageInstitutions(IsSuperAdministrator):
    """
    Permission for Institution Management.

    Institution Management is currently restricted to
    Super Administrators because the current User model
    does not contain an institution relationship for
    institution-scoped authorization.
    """

    message = "Super Administrator role required to manage institutions."
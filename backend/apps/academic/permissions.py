from apps.accounts.permissions import IsSuperAdministrator


class CanManageAcademicYears(IsSuperAdministrator):
    """
    Academic Year Management permission.

    Academic Year management is currently restricted to
    Super Administrators because the current User model
    does not provide the institution relationship required
    for institution-scoped authorization.
    """

    message = (
        "Super Administrator role required to manage academic years."
    )
from apps.accounts.permissions import IsSuperAdministrator


class CanManageInstitutions(IsSuperAdministrator):
    """
    Institution CRUD is currently restricted to
    Super Administrators.

    Institution-scoped administrator access will be introduced
    only when the approved institution-user relationship exists.
    """

    message = "Super Administrator role required to manage institutions."
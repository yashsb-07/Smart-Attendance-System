def present_user(user):
    """
    Convert a User model instance into a standard API representation.
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_verified": user.email_verified,
    }


def present_managed_user(user):
    """
    Format a User Management API representation.
    """
    data = present_user(user)

    data.update(
        {
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
                "label": user.role.get_name_display(),
            },
            "date_joined": user.date_joined,
            "last_login": user.last_login,
        }
    )

    return data


def present_login(auth_data):
    """
    Format the login response payload.
    """
    return {
        "user": present_user(auth_data["user"]),
        "tokens": {
            "access": auth_data["access"],
            "refresh": auth_data["refresh"],
        },
    }


def present_current_user(user):
    """
    Format the authenticated user response payload.
    """
    data = present_user(user)

    data.update(
        {
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
                "label": user.role.get_name_display(),
            },
        }
    )

    return data
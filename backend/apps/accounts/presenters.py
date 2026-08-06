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
    }


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
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
    )

    return data
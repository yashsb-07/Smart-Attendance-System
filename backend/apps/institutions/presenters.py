def present_institution(institution):
    return {
        "id": institution.id,
        "name": institution.name,
        "code": institution.code,
        "description": institution.description,
        "email": institution.email,
        "phone": institution.phone,
        "address": institution.address,
        "website": institution.website,
        "is_active": institution.is_active,
        "created_at": institution.created_at,
        "updated_at": institution.updated_at,
    }
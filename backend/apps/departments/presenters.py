def present_department(department):
    return {
        "id": department.id,
        "institution": department.institution_id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "is_active": department.is_active,
        "created_at": department.created_at,
        "updated_at": department.updated_at,
    }
def present_academic_year(academic_year):
    return {
        "id": academic_year.id,
        "institution": academic_year.institution_id,
        "name": academic_year.name,
        "start_date": academic_year.start_date,
        "end_date": academic_year.end_date,
        "is_current": academic_year.is_current,
        "is_active": academic_year.is_active,
        "created_at": academic_year.created_at,
        "updated_at": academic_year.updated_at,
    }
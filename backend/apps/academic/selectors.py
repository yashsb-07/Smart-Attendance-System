from .models import AcademicYear


def list_academic_years():
    return AcademicYear.objects.select_related(
        "institution",
    ).all()


def get_academic_year(*, academic_year_id: int):
    return AcademicYear.objects.select_related(
        "institution",
    ).get(
        pk=academic_year_id,
    )
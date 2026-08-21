from .models import Department


def list_departments():
    return Department.objects.select_related(
        "institution",
    ).all()


def get_department(*, department_id: int):
    return Department.objects.select_related(
        "institution",
    ).get(
        pk=department_id,
    )
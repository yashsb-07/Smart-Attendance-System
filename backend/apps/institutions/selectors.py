from .models import Institution


def list_institutions():
    return Institution.objects.all()


def get_institution(*, institution_id: int):
    return Institution.objects.get(
        pk=institution_id,
    )
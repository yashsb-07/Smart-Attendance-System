from django.urls import path

from .views import (
    InstitutionDetailAPIView,
    InstitutionListCreateAPIView,
)


app_name = "institutions"


urlpatterns = [
    path(
        "",
        InstitutionListCreateAPIView.as_view(),
        name="institution-list-create",
    ),
    path(
        "<int:institution_id>/",
        InstitutionDetailAPIView.as_view(),
        name="institution-detail",
    ),
]
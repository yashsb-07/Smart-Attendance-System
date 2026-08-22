from django.urls import path

from .views import (
    AcademicYearDetailAPIView,
    AcademicYearListCreateAPIView,
)


urlpatterns = [
    path(
        "",
        AcademicYearListCreateAPIView.as_view(),
        name="academic-year-list-create",
    ),
    path(
        "<int:academic_year_id>/",
        AcademicYearDetailAPIView.as_view(),
        name="academic-year-detail",
    ),
]
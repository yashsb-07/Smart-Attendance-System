from django.urls import path

from .views import (
    DepartmentDetailAPIView,
    DepartmentListCreateAPIView,
)


app_name = "departments"


urlpatterns = [
    path(
        "",
        DepartmentListCreateAPIView.as_view(),
        name="department-list-create",
    ),
    path(
        "<int:department_id>/",
        DepartmentDetailAPIView.as_view(),
        name="department-detail",
    ),
]
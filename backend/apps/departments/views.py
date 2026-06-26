from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Department
from .serializers import DepartmentSerializer
from .permissions import DepartmentPermission

# Create your views here.

class DepartmentViewSet(
    ModelViewSet
):

    queryset = Department.objects.all().order_by("id")

    serializer_class = DepartmentSerializer

    permission_classes = [
        DepartmentPermission
    ]
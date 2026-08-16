from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from apps.common.responses import success_response

from .models import Institution
from .permissions import CanManageInstitutions
from .presenters import present_institution
from .selectors import list_institutions
from .serializers import InstitutionSerializer
from .services import (
    create_institution,
    delete_institution,
    update_institution,
)


class InstitutionListCreateAPIView(APIView):
    permission_classes = [CanManageInstitutions]

    def get(self, request):
        institutions = list_institutions()

        data = [
            present_institution(institution)
            for institution in institutions
        ]

        return success_response(
            message="Institutions retrieved successfully.",
            data=data,
        )

    def post(self, request):
        serializer = InstitutionSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        institution = create_institution(
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Institution created successfully.",
            data=present_institution(institution),
            status_code=status.HTTP_201_CREATED,
        )


class InstitutionDetailAPIView(APIView):
    permission_classes = [CanManageInstitutions]

    def get_institution(self, institution_id):
        return get_object_or_404(
            Institution,
            pk=institution_id,
        )

    def get(self, request, institution_id):
        institution = self.get_institution(
            institution_id,
        )

        return success_response(
            message="Institution retrieved successfully.",
            data=present_institution(institution),
        )

    def put(self, request, institution_id):
        institution = self.get_institution(
            institution_id,
        )

        serializer = InstitutionSerializer(
            institution,
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        institution = update_institution(
            institution=institution,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Institution updated successfully.",
            data=present_institution(institution),
        )

    def patch(self, request, institution_id):
        institution = self.get_institution(
            institution_id,
        )

        serializer = InstitutionSerializer(
            institution,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        institution = update_institution(
            institution=institution,
            validated_data=serializer.validated_data,
        )

        return success_response(
            message="Institution updated successfully.",
            data=present_institution(institution),
        )

    def delete(self, request, institution_id):
        institution = self.get_institution(
            institution_id,
        )

        delete_institution(
            institution=institution,
        )

        return success_response(
            message="Institution deleted successfully.",
            data=None,
        )
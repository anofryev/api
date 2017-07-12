from rest_framework.permissions import BasePermission

from ..models import PatientConsent


class HasPatientValidConsent(BasePermission):
    def has_permission(self, request, view):
        return PatientConsent.objects.valid().filter(
            patient=view.kwargs['patient_pk']).exists()

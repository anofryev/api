from rest_framework.permissions import BasePermission

from ..models import Patient


class HasPatientValidConsent(BasePermission):
    def has_permission(self, request, view):
        try:
            patient = Patient.objects.get(pk=view.kwargs['patient_pk'])
        except Patient.DoesNotExist:
            return False

        return patient.valid_consent is not None

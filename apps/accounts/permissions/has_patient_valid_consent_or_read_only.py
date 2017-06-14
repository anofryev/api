from rest_framework.permissions import SAFE_METHODS

from .is_doctor_of_patient import IsDoctorOfPatient


class HasPatientValidConsentOrReadOnly(IsDoctorOfPatient):
    """
    Allows to use safe methods for this view but forbids to create/update/delete
    if user isn't a doctor of patient or patient doesn't have valid consent
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not super(HasPatientValidConsentOrReadOnly, self).has_permission(
                request, view):
            return False

        doctor = request.user.doctor_role
        patient = doctor.patients.get(pk=view.kwargs['patient_pk'])

        return patient.valid_consent is not None

from rest_framework.permissions import SAFE_METHODS

from .is_doctor_of_patient import IsDoctorOfPatient


class HasPatientValidConsentOrDoctorOfPatientCanEdit(IsDoctorOfPatient):
    def has_permission(self, request, view):
        if not super(HasPatientValidConsentOrDoctorOfPatientCanEdit, self).has_permission(
                request, view):
            return False

        doctor = request.user.doctor_role
        patient = doctor.patients.get(pk=view.kwargs['patient_pk'])

        return patient.valid_consent is not None or request.method != 'POST'

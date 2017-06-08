from .is_doctor import IsDoctor


class IsDoctorOfPatient(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsDoctorOfPatient, self).has_permission(request, view):
            return False

        doctor = request.user.doctor_role

        return doctor.patients.filter(pk=view.kwargs['patient_pk']).exists()

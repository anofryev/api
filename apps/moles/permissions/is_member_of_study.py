from apps.accounts.permissions import IsDoctor


class IsMemberOfStudy(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsMemberOfStudy, self).has_permission(request, view):
            return False

        doctor = request.user.doctor_role

        return doctor.patients.filter(pk=view.kwargs['patient_pk']).exists()

    def has_object_permission(self, request, view, obj):
        if not super(IsMemberOfStudy, self).has_object_permission(
                request, view, obj):
            return False

        doctor = request.user.doctor_role
        return obj.doctors.filter(pk=doctor.pk).exists()

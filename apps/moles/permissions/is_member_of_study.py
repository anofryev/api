from apps.accounts.permissions import IsDoctor


class IsMemberOfStudy(IsDoctor):
    def has_object_permission(self, request, view, obj):
        if not super(IsMemberOfStudy, self).has_object_permission(
                request, view, obj):
            return False

        doctor = request.user.doctor_role
        return obj.doctors.filter(pk=doctor.pk).exists()

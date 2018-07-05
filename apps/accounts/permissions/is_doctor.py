from rest_framework.permissions import IsAuthenticated

from apps.accounts.models.coordinator import is_coordinator
from apps.accounts.models.participant import is_participant


class IsDoctor(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(IsDoctor, self).has_permission(request, view):
            return False

        return hasattr(request.user, 'doctor_role')


class IsOnlyDoctor(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsOnlyDoctor, self).has_permission(request, view):
            return False

        doctor = request.user.doctor_role
        return not is_participant(doctor) and not is_coordinator(doctor)

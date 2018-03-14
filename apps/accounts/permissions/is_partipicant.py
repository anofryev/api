from .is_doctor import IsDoctor
from ..models import Participant


class IsParticipant(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsParticipant, self).has_permission(request, view):
            return False

        return Participant.objects.filter(doctor_ptr=request.user).exists()

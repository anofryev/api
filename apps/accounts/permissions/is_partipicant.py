from .is_doctor import IsDoctor
from ..models.participant import is_participant


class IsParticipant(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsParticipant, self).has_permission(request, view):
            return False

        return is_participant(request.user)

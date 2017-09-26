from .is_doctor import IsDoctor
from ..models import Coordinator


class IsCoordinator(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsCoordinator, self).has_permission(request, view):
            return False

        return Coordinator.objects.filter(
            doctor_ptr_id=request.user.id).exists()

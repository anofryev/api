from .is_doctor import IsDoctor
from ..models.coordinator import is_coordinator


class IsCoordinator(IsDoctor):
    def has_permission(self, request, view):
        if not super(IsCoordinator, self).has_permission(request, view):
            return False

        return is_coordinator(request.user) is not None

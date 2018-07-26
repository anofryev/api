from rest_framework.generics import get_object_or_404

from .is_coordinator import IsCoordinator
from ..models import Doctor


class IsCoordinatorOfDoctor(IsCoordinator):
    def has_permission(self, request, view):
        if not super(IsCoordinatorOfDoctor, self).has_permission(request, view):
            return False

        coordinator = request.user.doctor_role
        if 'doctor_pk' not in view.request.data or \
                not view.request.data['doctor_pk']:
            # lets pass to view, because error will be processed by serializer
            # it's because permissions works earlier, than required=True
            return True

        doctor_pk = view.request.data['doctor_pk']
        if doctor_pk == coordinator.pk:
            return True

        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        return doctor.my_coordinator == coordinator.coordinator_role

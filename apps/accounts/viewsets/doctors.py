from rest_framework import viewsets, mixins
from ..serializers import DoctorRegistrationRequestSerializer
from ..permissions import IsCoordinator
from ..models import Doctor


class DoctorRegistrationRequestViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin):
    serializer_class = DoctorRegistrationRequestSerializer
    permission_classes = (IsCoordinator, )
    queryset = Doctor.objects.none()

    def get_queryset(self):
        return Doctor.objects.filter(
            approved_by_coordinator=False,
            my_coordinator_id=self.request.user.id)

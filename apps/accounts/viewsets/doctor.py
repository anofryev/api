from rest_framework import viewsets, mixins

from ..serializers import DoctorSerializer
from ..models import Doctor
from ..permissions import IsCoordinator


class DoctorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.filter(
        coordinator_role__isnull=True,
        participant_role__isnull=True
    )
    permission_classes = (IsCoordinator, )

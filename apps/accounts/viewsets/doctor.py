from rest_framework import viewsets, mixins

from ..serializers import DoctorWithSitesSerializer
from ..models import Doctor
from ..permissions import IsCoordinator


class DoctorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    serializer_class = DoctorWithSitesSerializer
    queryset = Doctor.objects.filter(
        coordinator_role__isnull=True,
        participant_role__isnull=True
    )
    permission_classes = (IsCoordinator, )

    def get_queryset(self):
        return super(DoctorViewSet, self)\
            .get_queryset()\
            .annotate_sites()

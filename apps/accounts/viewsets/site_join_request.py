from rest_framework import viewsets, mixins

from apps.main.viewsets import add_transition_actions

from ..serializers import (
    SiteJoinRequestSerializer, CreateSiteJoinRequestSerializer, )
from ..permissions import IsCoordinator, IsDoctor, C
from ..models import SiteJoinRequest
from ..models.coordinator import is_coordinator


@add_transition_actions
class SiteJoinRequestViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin):
    serializer_class = SiteJoinRequestSerializer
    permission_classes = (
        C(IsCoordinator) | C(IsDoctor),
    )
    queryset = SiteJoinRequest.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateSiteJoinRequestSerializer
        return self.serializer_class

    def get_queryset(self):
        doctor = self.request.user.doctor_role
        coordinator = is_coordinator(doctor)
        if coordinator:
            return SiteJoinRequest.objects.filter(
                site=coordinator.site)
        return SiteJoinRequest.objects.filter(
            doctor=doctor
        )

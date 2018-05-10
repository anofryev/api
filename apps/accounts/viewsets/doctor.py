from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from ..serializers import DoctorWithSitesSerializer, DoctorKeySerializer
from ..models import Doctor
from ..permissions import IsCoordinator


class DoctorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    serializer_class = DoctorWithSitesSerializer
    queryset = Doctor.objects.filter(
        participant_role__isnull=True
    )
    permission_classes = (IsCoordinator, )

    def get_queryset(self):
        return super(DoctorViewSet, self)\
            .get_queryset()\
            .annotate_sites()

    @detail_route(methods=['GET'])
    def public_key(self, request, *args, **kwargs):
        return Response(DoctorKeySerializer(self.get_object()).data)

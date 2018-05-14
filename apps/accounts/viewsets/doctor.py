from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route

from ..serializers import DoctorWithSitesSerializer, DoctorKeySerializer
from ..models import Doctor
from ..permissions import IsCoordinator, IsDoctor


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

    @list_route(methods=['GET'], permission_classes=(IsDoctor,))
    def public_keys(self, request, *args, **kwargs):
        doctor_pks = request.GET.get('doctors').split(',')
        return Response(DoctorKeySerializer(
            Doctor.objects.filter(pk__in=doctor_pks),
            many=True
        ).data)

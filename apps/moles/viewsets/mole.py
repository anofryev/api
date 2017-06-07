from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route

from apps.accounts.permissions import IsDoctorOfPatient
from apps.accounts.viewsets.mixins import PatientInfoMixin
from ..models import Mole
from ..serializers import MoleListSerializer, MoleDetailSerializer


class MoleViewSet(viewsets.GenericViewSet, PatientInfoMixin,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin):
    queryset = Mole.objects.all()
    serializer_class = MoleListSerializer
    permission_classes = (IsDoctorOfPatient, )

    def get_queryset(self):
        qs = super(MoleViewSet, self).get_queryset()
        qs = qs.prefetch_related('images')

        return qs.filter(patient=self.get_patient_pk())

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MoleDetailSerializer

        return self.serializer_class

    @detail_route(methods=['POST'])
    def images(self):
        pass

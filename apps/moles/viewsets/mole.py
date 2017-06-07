from django.db import transaction
from rest_framework import viewsets, mixins, response, status
from rest_framework.decorators import detail_route

from apps.accounts.permissions import IsDoctorOfPatient
from apps.accounts.viewsets.mixins import PatientInfoMixin
from ..models import Mole, MoleImage
from ..serializers import (
    MoleListSerializer, MoleDetailSerializer, MoleCreateSerializer,
    MoleUpdateSerializer, MoleImageCreateSerializer)


class MoleViewSet(viewsets.GenericViewSet, PatientInfoMixin,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
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
        elif self.action == 'create':
            return MoleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MoleUpdateSerializer
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(patient=self.get_patient())

        return response.Response(
            MoleDetailSerializer(instance=instance).data,
            status=status.HTTP_201_CREATED)

    @detail_route(methods=['POST'], serializer_class=MoleImageCreateSerializer)
    def images(self, request, *args, **kwargs):
        mole = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        serializer.save(mole=mole)

        return response.Response(
            data=serializer.data, status=status.HTTP_201_CREATED)

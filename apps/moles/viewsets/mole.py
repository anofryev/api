from django.db import transaction
from rest_framework import viewsets, mixins, response, status

from apps.accounts.permissions import (
    CompositeOr, IsDoctorOfPatient, HasPatientValidConsent, ForbidCreation)
from apps.accounts.viewsets.mixins import PatientInfoMixin
from ..models import Mole
from ..serializers import (
    MoleListSerializer, MoleDetailSerializer, MoleCreateSerializer,
    MoleUpdateSerializer)


class MoleViewSet(viewsets.GenericViewSet, PatientInfoMixin,
                  mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    queryset = Mole.objects.all()
    serializer_class = MoleListSerializer
    permission_classes = (
        IsDoctorOfPatient,
        CompositeOr(HasPatientValidConsent, ForbidCreation)
    )

    def get_queryset(self):
        qs = super(MoleViewSet, self).get_queryset()
        qs = qs.prefetch_related('images')

        qs = qs.annotate_last_upload().order_by(
            '-last_upload')

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
        headers = self.get_success_headers(serializer.data)

        return response.Response(
            MoleDetailSerializer(instance=instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

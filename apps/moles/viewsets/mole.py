from django.db import transaction
from django.db.models import Count, Case, When, F, Q
from rest_framework import viewsets, mixins, response, status

from apps.accounts.permissions import (
    C, IsDoctorOfPatient, HasPatientValidConsent, AllowAllExceptCreation)
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
        C(HasPatientValidConsent) | C(AllowAllExceptCreation)
    )

    def get_queryset(self):
        return super(MoleViewSet, self)\
            .get_queryset()\
            .prefetch_related('images')\
            .annotate_last_upload()\
            .annotate_clinical_diagnosis_required()\
            .annotate_pathological_diagnosis_required()\
            .annotate_biopsy_count()\
            .annotate_approve_required()\
            .filter(patient=self.get_patient_pk())\
            .order_by('-last_upload')

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

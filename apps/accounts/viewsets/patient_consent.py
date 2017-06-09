from rest_framework import viewsets, mixins

from ..serializers import PatientConsentSerializer
from ..models import PatientConsent
from ..permissions import IsDoctorOfPatient
from .mixins import PatientInfoMixin


class PatientConsentViewSet(viewsets.GenericViewSet,
                            PatientInfoMixin,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    serializer_class = PatientConsentSerializer
    queryset = PatientConsent.objects.all()
    permission_classes = (IsDoctorOfPatient, )

    def get_queryset(self):
        qs = super(PatientConsentViewSet, self).get_queryset()

        qs = qs.filter(patient=self.get_patient_pk())

        return qs

    def perform_create(self, serializer):
        return serializer.save(patient=self.get_patient())

from rest_framework import viewsets, mixins

from apps.accounts.permissions import (
    C, IsDoctorOfPatient, HasPatientValidConsent, AllowAllExceptCreation)
from apps.accounts.viewsets.mixins import PatientInfoMixin
from ..models import PatientAnatomicalSite
from ..serializers import PatientAnatomicalSiteSerializer


class PatientAnatomicalSiteViewSet(viewsets.GenericViewSet,
                                   PatientInfoMixin,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.CreateModelMixin):
    serializer_class = PatientAnatomicalSiteSerializer
    queryset = PatientAnatomicalSite.objects.all()
    permission_classes = (
        IsDoctorOfPatient,
        C(HasPatientValidConsent) | C(AllowAllExceptCreation)
    )

    def get_queryset(self):
        qs = super(PatientAnatomicalSiteViewSet, self).get_queryset()

        return qs.filter(patient=self.get_patient_pk())

    def perform_create(self, serializer):
        return serializer.save(patient=self.get_patient())

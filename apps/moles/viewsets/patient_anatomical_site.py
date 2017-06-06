from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import IsDoctorOfPatient
from ..models import PatientAnatomicalSite
from ..serializers import PatientAnatomicalSiteSerializer


class PatientAnatomicalSiteViewSet(ModelViewSet):
    serializer_class = PatientAnatomicalSiteSerializer
    queryset = PatientAnatomicalSite.objects.all()
    permission_classes = (IsDoctorOfPatient, )

    def get_queryset(self):
        qs = super(PatientAnatomicalSiteViewSet, self).get_queryset()

        patient_pk = self.kwargs['patient_pk']

        return qs.filter(patient=patient_pk)

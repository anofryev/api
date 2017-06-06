from rest_framework.viewsets import ModelViewSet

from ..serializers import PatientSerializer
from ..models import Patient


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

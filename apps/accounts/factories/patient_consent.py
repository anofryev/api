from factory import DjangoModelFactory, SubFactory

from ..models import PatientConsent
from .patient import PatientFactory


class PatientConsentFactory(DjangoModelFactory):
    patient = SubFactory(PatientFactory)

    class Meta:
        model = PatientConsent

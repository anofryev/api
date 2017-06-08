from factory import SubFactory, DjangoModelFactory

from apps.accounts.factories import PatientFactory
from ..models import PatientAnatomicalSite
from .anatomical_site import AnatomicalSiteFactory


class PatientAnatomicalSiteFactory(DjangoModelFactory):
    patient = SubFactory(PatientFactory)
    anatomical_site = SubFactory(AnatomicalSiteFactory)

    class Meta:
        model = PatientAnatomicalSite

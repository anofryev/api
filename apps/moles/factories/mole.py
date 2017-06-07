from factory import SubFactory, DjangoModelFactory

from apps.accounts.factories import PatientFactory
from ..models import Mole
from .anatomical_site import AnatomicalSiteFactory


class MoleFactory(DjangoModelFactory):
    patient = SubFactory(PatientFactory)
    anatomical_site = SubFactory(AnatomicalSiteFactory)
    position_x = 0
    position_y = 0

    class Meta:
        model = Mole

from factory import Faker, DjangoModelFactory

from ..models import AnatomicalSite


class AnatomicalSiteFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = AnatomicalSite

from factory import DjangoModelFactory, SubFactory
from ..models import Site
from .coordinator import CoordinatorFactory


class SiteFactory(DjangoModelFactory):
    site_coordinator = SubFactory(CoordinatorFactory)

    class Meta:
        model = Site

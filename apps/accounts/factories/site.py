from factory import DjangoModelFactory
from ..models import Site


class SiteFactory(DjangoModelFactory):
    class Meta:
        model = Site

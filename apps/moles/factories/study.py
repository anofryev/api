from factory import DjangoModelFactory

from ..models import ConsentDoc


class ConsentDocFactory(DjangoModelFactory):
    class Meta:
        model = ConsentDoc

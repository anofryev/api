from factory import SubFactory, DjangoModelFactory

from ..models import MoleImage
from .mole import MoleFactory


class MoleImageFactory(DjangoModelFactory):
    mole = SubFactory(MoleFactory)

    class Meta:
        model = MoleImage

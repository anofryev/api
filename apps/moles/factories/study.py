from factory import DjangoModelFactory, fuzzy

from ..models import ConsentDoc
from apps.moles.models.study import Study


class ConsentDocFactory(DjangoModelFactory):
    class Meta:
        model = ConsentDoc


class StudyFactory(DjangoModelFactory):
    class Meta:
        model = Study

    title = fuzzy.FuzzyText()

from factory import DjangoModelFactory, SubFactory, fuzzy

from ..models import ConsentDoc
from apps.moles.models.study import Study, StudyToPatient
from apps.accounts.factories import PatientFactory, DoctorFactory


class ConsentDocFactory(DjangoModelFactory):
    class Meta:
        model = ConsentDoc


class StudyFactory(DjangoModelFactory):
    class Meta:
        model = Study

    title = fuzzy.FuzzyText()

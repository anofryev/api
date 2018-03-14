from factory import Faker

from factory import DjangoModelFactory, SubFactory
from apps.accounts.factories import DoctorFactory
from apps.moles.models.study_invitation import StudyInvitation
from apps.moles.factories.study import StudyFactory


class StudyInvitationFactory(DjangoModelFactory):
    class Meta:
        model = StudyInvitation

    email = Faker('email')
    doctor = SubFactory(DoctorFactory)
    study = SubFactory(StudyFactory)

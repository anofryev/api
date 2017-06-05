from factory import Faker, SubFactory

from ..models import Patient, SexEnum, RaceEnum
from .user import UserFactory
from .doctor import DoctorFactory


class PatientFactory(UserFactory):
    doctor = SubFactory(DoctorFactory)
    date_of_birth = Faker('date')
    sex = SexEnum.MALE
    race = RaceEnum.ASIAN

    class Meta:
        model = Patient

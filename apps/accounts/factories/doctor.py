from factory import Faker

from ..models import Doctor
from .user import UserFactory


class DoctorFactory(UserFactory):
    email = Faker('email')

    class Meta:
        model = Doctor

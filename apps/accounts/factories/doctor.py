from factory import Faker

from ..models import Doctor, Coordinator
from .user import UserFactory


class DoctorFactory(UserFactory):
    email = Faker('email')

    class Meta:
        model = Doctor

    @classmethod
    def create(self, coordinator=False, **kwargs):
        doctor = super(DoctorFactory, self).create(**kwargs)
        if coordinator:
            Coordinator.objects.create(doctor_ptr_id=doctor.id)
        return doctor

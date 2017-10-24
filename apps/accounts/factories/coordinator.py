from factory import DjangoModelFactory, SubFactory
from ..models import Coordinator
from .doctor import DoctorFactory


class CoordinatorFactory(DjangoModelFactory):
    doctor_ptr = SubFactory(DoctorFactory)

    class Meta:
        model = Coordinator

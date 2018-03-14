from factory import DjangoModelFactory, SubFactory
from ..models import Participant
from .doctor import DoctorFactory


class ParticipantFactory(DjangoModelFactory):
    doctor_ptr = SubFactory(DoctorFactory)

    class Meta:
        model = Participant

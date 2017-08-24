from factory import DjangoModelFactory, fuzzy

from ..models import Patient, SexEnum, RaceEnum, DoctorToPatient
from .doctor import DoctorFactory


class PatientFactory(DjangoModelFactory):
    sex = SexEnum.MALE
    race = RaceEnum.ASIAN

    class Meta:
        model = Patient

    @classmethod
    def create(self, doctor=None, **kwargs):
        doctor = doctor or DoctorFactory.create()
        patient = super(PatientFactory, self).create(**kwargs)
        DoctorToPatient.objects.create(
            patient=patient,
            doctor=doctor,
            encrypted_key=fuzzy.FuzzyText().fuzz()
        )
        return patient

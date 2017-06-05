import datetime
from django.test import TestCase

from apps.accounts.models.patient import RaceEnum, SexEnum
from ..models import Doctor, Patient
from ..factories import DoctorFactory


class ModelsTestCase(TestCase):
    def test_create_doctor(self):
        doctor = Doctor.objects.create(
            first_name='first', last_name='last', email='doctor@email.org')

        self.assertEqual(doctor.username, 'doctor@email.org')

    def test_create_patient_with_mrn(self):
        doctor = DoctorFactory.create()

        patient = Patient.objects.create(
            first_name='first', last_name='last',
            date_of_birth=datetime.date.today(),
            race=RaceEnum.ASIAN,
            sex=SexEnum.MALE,
            doctor=doctor,
            mrn=1234567)

        self.assertEqual(patient.username, '1234567')

    def test_create_patient_without_mrn(self):
        doctor = DoctorFactory.create()

        patient = Patient.objects.create(
            first_name='first', last_name='last',
            date_of_birth=datetime.date.today(),
            race=RaceEnum.ASIAN,
            sex=SexEnum.MALE,
            doctor=doctor
        )

        self.assertTrue(patient.username.startswith('first_last_'))

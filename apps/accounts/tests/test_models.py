import datetime
from django.test import TestCase

from ..models import User, Doctor, Patient, RaceEnum, SexEnum
from ..factories import DoctorFactory


class ModelsTestCase(TestCase):
    def test_create_user_failed(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'first name', 'last name')

        with self.assertRaises(ValueError):
            User.objects.create_user('username', '', 'last name')

        with self.assertRaises(ValueError):
            User.objects.create_user('username', 'first name', '')

    def test_create_user(self):
        user = User.objects.create_user(
            username='username',
            first_name='first name',
            last_name='last name',
            password='qwertyuiop')
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.first_name, 'first name')
        self.assertEqual(user.last_name, 'last name')
        self.assertTrue(user.check_password('qwertyuiop'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.get_full_name(), 'first name last name')
        self.assertEqual(user.get_short_name(), 'first name')

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='username',
            first_name='first name',
            last_name='last name',
            password='qwertyuiop')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

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

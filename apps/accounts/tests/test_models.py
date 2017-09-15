import datetime

from django.test import TestCase
from django.utils import timezone

from apps.main.tests.mixins import FileTestMixin
from ..models import User, Doctor, Patient, RaceEnum, SexEnum
from ..factories import DoctorFactory, PatientFactory, PatientConsentFactory


class ModelsTestCase(FileTestMixin, TestCase):
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
        with self.fake_media():
            doctor = Doctor.objects.create(
                photo=self.get_sample_image_file(),
                first_name='first',
                last_name='last',
                email='doctor@email.org')

        self.assertEqual(doctor.username, 'doctor@email.org')

    def test_patient_does_not_have_valid_consent_without_consents(self):
        patient = PatientFactory.create()
        self.assertIsNone(patient.valid_consent)

    def test_patient_has_valid_consent(self):
        patient = PatientFactory.create()
        consent = PatientConsentFactory.create(patient=patient)
        self.assertEqual(patient.valid_consent, consent)

    def test_patient_does_not_have_valid_consent_if_expired(self):
        patient = PatientFactory.create()
        consent = PatientConsentFactory.create(patient=patient)
        consent.date_expired = timezone.now() - datetime.timedelta(hours=1)
        consent.save()
        self.assertIsNone(patient.valid_consent)

from apps.main.tests import APITestCase

from ..factories import PatientFactory
from ..models import Patient, RaceEnum, SexEnum


class ViewSetsTest(APITestCase):
    def setUp(self):
        super(ViewSetsTest, self).setUp()

        self.first_patient = PatientFactory.create(doctor=self.doctor)
        self.second_patient = PatientFactory.create(doctor=self.doctor)
        self.another_patient = PatientFactory.create()

    def test_get_patients_failed_for_unauthorized(self):
        resp = self.client.get('/api/v1/patient/')
        self.assertForbidden(resp)

    def test_get_patients_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/patient/')
        self.assertSuccessResponse(resp)

        self.assertEqual(len(resp.data), 2)

    def test_get_own_patient_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/patient/{0}/'.format(
            self.first_patient.pk))
        self.assertSuccessResponse(resp)

    def test_get_not_own_patient_failed(self):
        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/patient/{0}/'.format(
            self.another_patient.pk))
        self.assertNotFound(resp)

    def test_create_patient_success(self):
        self.authenticate_as_doctor()

        patient_data = {
            'first_name': 'first name',
            'last_name': 'first name',
            'sex': SexEnum.MALE,
            'race': RaceEnum.ASIAN,
            'date_of_birth': '1990-01-01',
            'address': 'address',
            'photo': self.get_sample_image_file('photo.jpg'),
        }

        with self.fake_media():
            resp = self.client.post('/api/v1/patient/', patient_data)

        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertIsNotNone(data['pk'])
        patient = Patient.objects.get(pk=data['pk'])

        self.assertEqual(patient.doctor, self.doctor)
        self.assertEqual(patient.first_name, patient_data['first_name'])
        self.assertEqual(patient.last_name, patient_data['last_name'])
        self.assertEqual(patient.sex, patient_data['sex'])
        self.assertEqual(patient.race, patient_data['race'])
        self.assertEqual(patient.address, patient_data['address'])
        self.assertEqual(
            str(patient.date_of_birth), patient_data['date_of_birth'])
        self.assertTrue(
            patient.photo.name.startswith(
                'users/{0}/patients/{1}/'
                'profile_picture/{1}_profile_pic_'.format(
                    self.doctor.pk, patient.pk)))
        self.assertIsNone(patient.mrn)

    def test_update_patient_success(self):
        self.authenticate_as_doctor()

        patient = PatientFactory.create(doctor=self.doctor)

        patient_data = {
            'first_name': 'first name',
            'last_name': 'first name',
            'sex': SexEnum.MALE,
            'race': RaceEnum.BLACK_OR_AFRICAN_AMERICAN,
            'date_of_birth': '1990-01-01',
            'address': 'address',
            'mrn': 1234567,
            'photo': self.get_sample_image_file('photo.jpg'),
        }

        with self.fake_media():
            resp = self.client.patch(
                '/api/v1/patient/{0}/'.format(patient.pk),
                patient_data)

        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(data['pk'], patient.pk)
        patient.refresh_from_db()

        self.assertEqual(patient.doctor, self.doctor)
        self.assertEqual(patient.first_name, patient_data['first_name'])
        self.assertEqual(patient.last_name, patient_data['last_name'])
        self.assertEqual(patient.sex, patient_data['sex'])
        self.assertEqual(patient.race, patient_data['race'])
        self.assertEqual(patient.address, patient_data['address'])
        self.assertEqual(
            str(patient.date_of_birth), patient_data['date_of_birth'])
        self.assertTrue(
            patient.photo.name.startswith(
                'users/{0}/patients/{1}/'
                'profile_picture/{1}_profile_pic_'.format(
                    self.doctor.pk, patient.pk)))
        self.assertEqual(patient.mrn, 1234567)

    def test_delete_not_allowed(self):
        self.authenticate_as_doctor()

        patient = PatientFactory(doctor=self.doctor)
        resp = self.client.delete(
            '/api/v1/patient/{0}/'.format(patient.pk))
        self.assertNotAllowed(resp)

from apps.main.tests import APITestCase, patch

from ...factories import PatientFactory, DoctorFactory
from ...models import Patient, RaceEnum, SexEnum, DoctorToPatient


class PatientViewSetTest(APITestCase):
    def setUp(self):
        super(PatientViewSetTest, self).setUp()

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

    @patch('apps.moles.tasks.requests')
    def test_get_patients_with_path_pending(self, mock_requests):
        from apps.moles.factories import MoleFactory, MoleImageFactory

        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/patient/', {'path_pending': True})
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 0)

        first_patient_mole = MoleFactory.create(patient=self.first_patient)
        second_patient_mole = MoleFactory.create(patient=self.second_patient)
        first_patient_mole_image = MoleImageFactory(mole=first_patient_mole)
        second_patient_mole_image = MoleImageFactory(mole=second_patient_mole)

        resp = self.client.get('/api/v1/patient/', {'path_pending': True})
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 0)

        first_patient_mole_image.biopsy = True
        first_patient_mole_image.save()

        second_patient_mole_image.biopsy = True
        second_patient_mole_image.save()

        resp = self.client.get('/api/v1/patient/', {'path_pending': True})
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 2)

        first_patient_mole_image.path_diagnosis = 'path'
        first_patient_mole_image.save()

        resp = self.client.get('/api/v1/patient/', {'path_pending': True})
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 1)

        second_patient_mole_image.path_diagnosis = 'path'
        second_patient_mole_image.save()

        resp = self.client.get('/api/v1/patient/', {'path_pending': True})
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 0)

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
            'photo': self.get_sample_image_file(),
            'signature': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0l'
                         'EQVQIHQEEAPv/AP///wX+Av4DfRnGAAAAAElFTkSuQmCC',
            'encrypted_key': 'qwertyuiop',
        }

        with self.fake_media():
            resp = self.client.post('/api/v1/patient/', patient_data)

        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertIsNotNone(data['pk'])
        patient = Patient.objects.get(pk=data['pk'])
        self.assertEqual(patient.consents.count(), 1)

        self.assertTrue(DoctorToPatient.objects.filter(
            doctor=self.doctor, patient=patient).exists())
        self.assertEqual(patient.first_name, patient_data['first_name'])
        self.assertEqual(patient.last_name, patient_data['last_name'])
        self.assertEqual(patient.sex, patient_data['sex'])
        self.assertEqual(patient.race, patient_data['race'])
        self.assertEqual(
            str(patient.date_of_birth), patient_data['date_of_birth'])
        # self.assertTrue(
        #     patient.photo.name.startswith(
        #         'patients/{0}/profile_picture/{0}_profile_pic_'.format(
        #             patient.pk)))
        self.assertIsNone(patient.mrn)
        self.assertIsNone(patient.mrn_hash)

    def test_create_patient_require_coordinator_encrypted_key(self):
        coordinator = DoctorFactory.create(coordinator=True).coordinator_role
        self.doctor.my_coordinator = coordinator
        self.doctor.save()

        self.authenticate_as_doctor()

        patient_data = {
            'first_name': 'first name',
            'last_name': 'first name',
            'sex': SexEnum.MALE,
            'race': RaceEnum.ASIAN,
            'date_of_birth': '1990-01-01',
            'photo': self.get_sample_image_file(),
            'signature': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0l'
                         'EQVQIHQEEAPv/AP///wX+Av4DfRnGAAAAAElFTkSuQmCC',
            'encrypted_key': 'qwertyuiop',
        }

        with self.fake_media():
            resp = self.client.post('/api/v1/patient/', patient_data)
        self.assertBadRequest(resp)

        patient_data['coordinator_encrypted_key'] = 'poiuytrewq'
        patient_data['photo'] = self.get_sample_image_file()

        with self.fake_media():
            resp = self.client.post('/api/v1/patient/', patient_data)
        self.assertSuccessResponse(resp)

    def test_update_patient_success(self):
        self.authenticate_as_doctor()

        patient = PatientFactory.create(doctor=self.doctor)

        patient_data = {
            'first_name': 'first name',
            'last_name': 'first name',
            'sex': SexEnum.MALE,
            'race': RaceEnum.BLACK_OR_AFRICAN_AMERICAN,
            'date_of_birth': '1990-01-01',
            'mrn': '1234567',
            'mrn_hash': '1q2w3e4r',
            'photo': self.get_sample_image_file(),
            'encrypted_key': 'some new key',
        }

        with self.fake_media():
            resp = self.client.patch(
                '/api/v1/patient/{0}/'.format(patient.pk),
                patient_data)

        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(data['pk'], patient.pk)
        patient.refresh_from_db()

        self.assertTrue(DoctorToPatient.objects.filter(
            doctor=self.doctor, patient=patient).exists())
        self.assertEqual(patient.first_name, patient_data['first_name'])
        self.assertEqual(patient.last_name, patient_data['last_name'])
        self.assertEqual(patient.sex, patient_data['sex'])
        self.assertEqual(patient.race, patient_data['race'])
        self.assertEqual(
            str(patient.date_of_birth), patient_data['date_of_birth'])
        # self.assertTrue(
        #     patient.photo.name.startswith(
        #         'users/{0}/profile_picture/{0}_profile_pic_'.format(
        #             patient.pk)))
        self.assertEqual(patient.mrn, '1234567')
        self.assertEqual(patient.mrn_hash, '1q2w3e4r')

        self.assertEqual(
            'some new key',
            DoctorToPatient.objects.filter(
                patient=patient,
                doctor=self.doctor).values_list(
                    'encrypted_key',
                    flat=True).first())

    def test_encrypted_key_is_requred_for_patient_update(self):
        self.authenticate_as_doctor()

        patient = PatientFactory.create(doctor=self.doctor)

        patient_data = {
            'first_name': 'first name',
            'last_name': 'first name',
            'sex': SexEnum.MALE,
            'race': RaceEnum.BLACK_OR_AFRICAN_AMERICAN,
            'date_of_birth': '1990-01-01',
            'mrn': '1234567',
            'mrn_hash': '1q2w3e4r',
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.patch(
                '/api/v1/patient/{0}/'.format(patient.pk),
                patient_data)

        self.assertBadRequest(resp)

    def test_delete_not_allowed(self):
        self.authenticate_as_doctor()

        patient = PatientFactory(doctor=self.doctor)
        resp = self.client.delete(
            '/api/v1/patient/{0}/'.format(patient.pk))
        self.assertNotAllowed(resp)

from django.test import mock

from apps.main.tests import APITestCase, patch
from apps.accounts.factories import PatientFactory
from ..factories import (
    PatientAnatomicalSiteFactory, AnatomicalSiteFactory, MoleFactory)
from ..models import PatientAnatomicalSite, Mole


class ViewSetsTest(APITestCase):
    def setUp(self):
        super(ViewSetsTest, self).setUp()

        self.first_patient = PatientFactory.create(doctor=self.doctor)
        self.another_patient = PatientFactory()

        self.anatomical_site = AnatomicalSiteFactory.create()

        self.first_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.first_patient,
            anatomical_site=self.anatomical_site)
        self.another_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.another_patient,
            anatomical_site=self.anatomical_site)

        self.first_patient_mole = MoleFactory.create(
            patient=self.first_patient,
            anatomical_site=self.anatomical_site)

        self.another_patient_mole = MoleFactory.create(
            patient=self.another_patient,
            anatomical_site=self.anatomical_site)

    def test_get_patient_anatomical_sites_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/anatomical_site/'.format(
                self.first_patient.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_patient_asite.pk)

    def test_get_patient_anatomical_sites_forbidden_for_not_own_patient(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/anatomical_site/'.format(
                self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_anatomical_sites_forbidden_for_unauthorized(self):
        resp = self.client.get(
            '/api/v1/patient/{0}/anatomical_site/'.format(
                self.another_patient.pk))
        self.assertForbidden(resp)

    def test_create_success(self):
        self.authenticate_as_doctor()
        patient_asite_data = {
            'anatomical_site': self.anatomical_site.pk,
            'distant_photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                '/api/v1/patient/{0}/anatomical_site/'.format(
                    self.first_patient.pk), patient_asite_data)
        self.assertSuccessResponse(resp)

        self.assertIsNotNone(resp.data['pk'])
        patient_anatomical_site = PatientAnatomicalSite.objects.get(
            pk=resp.data['pk'])
        self.assertEqual(patient_anatomical_site.patient, self.first_patient)

    def test_update_not_allowed(self):
        self.authenticate_as_doctor()
        resp = self.client.patch(
            '/api/v1/patient/{0}/anatomical_site/{1}/'.format(
                self.first_patient.pk, self.first_patient_asite.pk))
        self.assertNotAllowed(resp)

    def test_delete_not_allowed(self):
        self.authenticate_as_doctor()
        resp = self.client.delete(
            '/api/v1/patient/{0}/anatomical_site/{1}/'.format(
                self.first_patient.pk, self.first_patient_asite.pk))
        self.assertNotAllowed(resp)

    def test_get_patient_moles_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/mole/'.format(self.first_patient.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_patient_mole.pk)

    def test_get_patient_moles_forbidden_for_not_own_patient(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/mole/'.format(self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_moles_forbidden_for_unauthorized(self):
        resp = self.client.get(
            '/api/v1/patient/{0}/mole/'.format(self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_mole_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/mole/{1}/'.format(
                self.first_patient.pk, self.first_patient_mole.pk))
        self.assertSuccessResponse(resp)

    def test_get_not_own_patient_mole_failed(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/patient/{0}/mole/{1}/'.format(
                self.another_patient.pk, self.another_patient_mole.pk))
        self.assertForbidden(resp)

    @patch('apps.moles.tasks.requests')
    def test_create_patient_mole_success(self, mock_requests):
        self.authenticate_as_doctor()

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'position_x': 10,
            'position_y': 20,
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                '/api/v1/patient/{0}/mole/'.format(self.first_patient.pk),
                mole_data)
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertIsNotNone(data['pk'])

        mole = Mole.objects.get(pk=data['pk'])
        self.assertEqual(mole.anatomical_site, self.anatomical_site)
        self.assertEqual(mole.position_x, mole_data['position_x'])
        self.assertEqual(mole.position_y, mole_data['position_y'])
        self.assertEqual(mole.images.count(), 1)

        mole_image = mole.images.first()
        self.assertTrue(mole_image.photo.name.startswith(
            'users/{0}/patients/{1}/skin_images/{2}/{2}_clinical_photo'.format(
                mole.patient.doctor.pk, mole.patient.pk, mole.pk)))

    def test_update_patient_mole_success(self):
        self.authenticate_as_doctor()
        another_anatomical_site = AnatomicalSiteFactory.create()

        mole_data = {
            'anatomical_site': another_anatomical_site.pk,
            'position_x': 10,
            'position_y': 20,
        }

        resp = self.client.patch(
            '/api/v1/patient/{0}/mole/{1}/'.format(
                self.first_patient.pk, self.first_patient_mole.pk),
            mole_data)
        self.assertSuccessResponse(resp)
        mole = self.first_patient_mole
        mole.refresh_from_db()
        self.assertEqual(mole.anatomical_site, another_anatomical_site)
        self.assertEqual(mole.position_x, mole_data['position_x'])
        self.assertEqual(mole.position_y, mole_data['position_y'])

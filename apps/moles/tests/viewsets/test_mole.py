import json
from apps.main.tests import patch
from ...factories import AnatomicalSiteFactory, PatientAnatomicalSiteFactory
from ...models import Mole
from ..moles_test_case import MolesTestCase


class MoleViewSetTest(MolesTestCase):
    def get_url(self, patient_pk, mole_pk=None):
        url = '/api/v1/patient/{0}/mole/'.format(
            patient_pk)

        if mole_pk:
            url += '{0}/'.format(mole_pk)

        return url

    def test_get_patient_moles_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(self.first_patient.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_patient_mole.pk)

    def test_get_patient_moles_forbidden_for_not_own_patient(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_moles_forbidden_for_unauthorized(self):
        resp = self.client.get(self.get_url(self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_mole_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(
                self.first_patient.pk, self.first_patient_mole.pk))
        self.assertSuccessResponse(resp)

    def test_get_not_own_patient_mole_failed(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(
                self.another_patient.pk, self.another_patient_mole.pk))
        self.assertForbidden(resp)

    @patch('apps.moles.tasks.requests')
    def test_create_success(self, mock_requests):
        self.authenticate_as_doctor()

        position_info = {'x': 10, 'y': 10}

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'position_info': json.dumps(position_info),
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                self.get_url(self.first_patient.pk),
                mole_data)
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertIsNotNone(data['pk'])

        mole = Mole.objects.get(pk=data['pk'])
        self.assertEqual(mole.anatomical_site, self.anatomical_site)
        self.assertDictEqual(mole.position_info, position_info)
        self.assertEqual(mole.images.count(), 1)

        mole_image = mole.images.first()
        self.assertTrue(mole_image.photo.name.startswith(
            'patients/{0}/skin_images/{1}/{1}_photo'.format(
                mole.patient.pk, mole.pk)))

    @patch('apps.moles.tasks.requests')
    def test_create_success_with_patient_anatomical_site(self, mock_requests):
        self.authenticate_as_doctor()

        patient_anatomical_site = PatientAnatomicalSiteFactory(
            patient=self.first_patient,
            anatomical_site=self.anatomical_site)

        position_info = {'x': 10, 'y': 10}

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'patient_anatomical_site': patient_anatomical_site.pk,
            'position_info': json.dumps(position_info),
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                self.get_url(self.first_patient.pk),
                mole_data)
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertIsNotNone(data['pk'])

        mole = Mole.objects.get(pk=data['pk'])
        self.assertEqual(mole.anatomical_site, self.anatomical_site)
        self.assertDictEqual(mole.position_info, position_info)
        self.assertEqual(mole.images.count(), 1)

        mole_image = mole.images.first()
        self.assertTrue(mole_image.photo.name.startswith(
            'patients/{0}/skin_images/{1}/{1}_photo'.format(
                mole.patient.pk, mole.pk)))

    def test_create_forbidden_for_wrong_patient_anatomical_site(self):
        self.authenticate_as_doctor()

        patient_anatomical_site = PatientAnatomicalSiteFactory()
        position_info = {'x': 10, 'y': 10}

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'patient_anatomical_site': patient_anatomical_site.pk,
            'position_info': json.dumps(position_info),
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                self.get_url(self.first_patient.pk),
                mole_data)
        self.assertBadRequest(resp)

    def test_create_forbidden_for_wrong_json(self):
        self.authenticate_as_doctor()

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'position_info': 'not valid json',
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(
                self.get_url(self.first_patient.pk),
                mole_data)
        self.assertBadRequest(resp)

    def test_create_forbidden_for_patient_without_valid_consent(self):
        self.authenticate_as_doctor()
        self.first_patient_consent.delete()
        resp = self.client.post(self.get_url(self.first_patient.pk))
        self.assertForbidden(resp)

    def test_update_success(self):
        self.authenticate_as_doctor()
        another_anatomical_site = AnatomicalSiteFactory.create()

        position_info = {'x': 10, 'y': 10}

        mole_data = {
            'anatomical_site': another_anatomical_site.pk,
            'position_info': json.dumps(position_info),
        }

        resp = self.client.patch(
            self.get_url(
                self.first_patient.pk, self.first_patient_mole.pk),
            mole_data,
            format='json')
        self.assertSuccessResponse(resp)
        mole = self.first_patient_mole
        mole.refresh_from_db()
        self.assertEqual(mole.anatomical_site, another_anatomical_site)
        self.assertDictEqual(mole.position_info, position_info)

    def test_update_allow_for_patient_without_valid_consent(self):
        self.authenticate_as_doctor()
        self.first_patient_consent.delete()
        resp = self.client.patch(
            self.get_url(self.first_patient.pk, self.first_patient_mole.pk))
        self.assertSuccessResponse(resp)

    def test_delete_not_allowed(self):
        self.authenticate_as_doctor()

        resp = self.client.delete(self.get_url(
                self.first_patient.pk, self.first_patient_mole.pk))
        self.assertNotAllowed(resp)

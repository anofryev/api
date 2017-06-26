from apps.main.tests import patch
from ...factories import AnatomicalSiteFactory
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

        mole_data = {
            'anatomical_site': self.anatomical_site.pk,
            'position_x': 10,
            'position_y': 20,
            'photo': self.get_sample_image_file(),
        }

        with self.fake_media():
            resp = self.client.post(self.get_url(self.first_patient.pk),
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
            'users/{0}/patients/{1}/skin_images/{2}/{2}_photo'.format(
                mole.patient.doctor.pk, mole.patient.pk, mole.pk)))

    def test_create_forbidden_for_patient_without_valid_consent(self):
        self.authenticate_as_doctor()
        self.first_patient_consent.delete()
        resp = self.client.post(self.get_url(self.first_patient.pk))
        self.assertForbidden(resp)

    def test_update_success(self):
        self.authenticate_as_doctor()
        another_anatomical_site = AnatomicalSiteFactory.create()

        mole_data = {
            'anatomical_site': another_anatomical_site.pk,
            'position_x': 10,
            'position_y': 20,
        }

        resp = self.client.patch(self.get_url(
                self.first_patient.pk, self.first_patient_mole.pk),
            mole_data)
        self.assertSuccessResponse(resp)
        mole = self.first_patient_mole
        mole.refresh_from_db()
        self.assertEqual(mole.anatomical_site, another_anatomical_site)
        self.assertEqual(mole.position_x, mole_data['position_x'])
        self.assertEqual(mole.position_y, mole_data['position_y'])

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


from ...models import PatientAnatomicalSite
from ..moles_test_case import MolesTestCase


class PatientAnatomicalSiteViewSetTest(MolesTestCase):
    def get_url(self, patient_pk, anatomical_site_pk=None):
        url = '/api/v1/patient/{0}/anatomical_site/'.format(
            patient_pk)

        if anatomical_site_pk:
            url += '{0}/'.format(anatomical_site_pk)

        return url

    def test_get_patient_anatomical_sites_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(self.first_patient.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_patient_asite.pk)

    def test_get_patient_anatomical_sites_forbidden_for_not_own_patient(self):
        self.authenticate_as_doctor()

        resp = self.client.get(self.get_url(self.another_patient.pk))
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
            resp = self.client.post(self.get_url(
                    self.first_patient.pk), patient_asite_data)
        self.assertSuccessResponse(resp)

        self.assertIsNotNone(resp.data['pk'])
        patient_anatomical_site = PatientAnatomicalSite.objects.get(
            pk=resp.data['pk'])
        self.assertTrue(patient_anatomical_site.distant_photo.name.startswith(
            'users/{0}/patients/{1}/anatomical_sites/{2}/regional_photo/'
            '{2}_{3}_regional_photo'.format(
                patient_anatomical_site.patient.doctor.pk,
                patient_anatomical_site.patient.pk,
                patient_anatomical_site.pk,
                patient_anatomical_site.anatomical_site.pk
            )))
        self.assertEqual(patient_anatomical_site.patient, self.first_patient)

    def test_create_forbidden_for_patient_without_valid_consent(self):
        self.authenticate_as_doctor()
        self.first_patient_consent.delete()
        resp = self.client.post(self.get_url(self.first_patient.pk))
        self.assertForbidden(resp)

    def test_update_not_allowed(self):
        self.authenticate_as_doctor()
        resp = self.client.patch(self.get_url(
                self.first_patient.pk, self.first_patient_asite.pk))
        self.assertNotAllowed(resp)

    def test_delete_not_allowed(self):
        self.authenticate_as_doctor()
        resp = self.client.delete(self.get_url(
                self.first_patient.pk, self.first_patient_asite.pk))
        self.assertNotAllowed(resp)

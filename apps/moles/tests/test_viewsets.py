from apps.main.tests import APITestCase
from apps.accounts.factories import PatientFactory
from ..factories import PatientAnatomicalSiteFactory


class ViewSetsTest(APITestCase):
    def setUp(self):
        super(ViewSetsTest, self).setUp()
        self.first_patient = PatientFactory.create(doctor=self.doctor)
        self.another_patient = PatientFactory()
        self.first_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.first_patient)
        self.another_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.another_patient)

    def test_get_patient_anatomical_sites_success(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/accounts/patient/{0}/anatomical_site/'.format(
                self.first_patient.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_patient_asite.pk)

    def test_get_patient_anatomical_sites_forbidden_for_not_own_patient(self):
        self.authenticate_as_doctor()

        resp = self.client.get(
            '/api/v1/accounts/patient/{0}/anatomical_site/'.format(
                self.another_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_anatomical_sites_forbidden_for_unauthorized(self):
        resp = self.client.get(
            '/api/v1/accounts/patient/{0}/anatomical_site/'.format(
                self.another_patient.pk))
        self.assertForbidden(resp)

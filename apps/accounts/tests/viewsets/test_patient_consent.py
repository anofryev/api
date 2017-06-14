from apps.main.tests import APITestCase

from ...factories import PatientFactory, PatientConsentFactory
from ...models import PatientConsent


class PatientConsentViewSetTest(APITestCase):
    def get_url(self, patient_pk, consent_pk=None):
        url = '/api/v1/patient/{0}/consent/'.format(patient_pk)

        if consent_pk:
            url += '{0}/'.format(consent_pk)

        return url

    def setUp(self):
        super(PatientConsentViewSetTest, self).setUp()

        self.first_patient = PatientFactory.create(doctor=self.doctor)

    def test_get_patient_consents_failed_for_unauthorized(self):
        resp = self.client.get(self.get_url(self.first_patient.pk))
        self.assertForbidden(resp)

    def test_get_patient_consents_success(self):
        self.authenticate_as_doctor()
        PatientConsentFactory.create(patient=self.first_patient)

        resp = self.client.get(self.get_url(self.first_patient.pk))
        self.assertSuccessResponse(resp)

        self.assertEqual(len(resp.data), 1)

    def test_create_patient_consent_success(self):
        self.authenticate_as_doctor()

        consent_data = {
            'signature': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAD0l'
                          'EQVQIHQEEAPv/AP///wX+Av4DfRnGAAAAAElFTkSuQmCC',
        }

        with self.fake_media():
            resp = self.client.post(
                self.get_url(self.first_patient.pk), consent_data)
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertIsNotNone(data['pk'])
        consent = PatientConsent.objects.get(pk=data['pk'])
        self.assertIsNotNone(consent.date_expired)
        self.assertEqual(consent.patient, self.first_patient)
        self.assertTrue(consent.signature.name.startswith(
            'users/62/patients/63/consent/{0}_signature'.format(consent.pk)))

    def test_detail_not_found(self):
        self.authenticate_as_doctor()
        consent = PatientConsentFactory.create(patient=self.first_patient)

        resp = self.client.get(self.get_url(self.first_patient, consent.pk))
        self.assertNotFound(resp)

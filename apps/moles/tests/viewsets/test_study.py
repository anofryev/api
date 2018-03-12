from apps.main.tests import APITestCase
from apps.accounts.factories import CoordinatorFactory, DoctorFactory, \
    PatientFactory
from apps.moles.factories.study import ConsentDocFactory
from apps.moles.models import Study


class StudyViewSetTest(APITestCase):
    def setUp(self):
        super(StudyViewSetTest, self).setUp()

        CoordinatorFactory.create(
            doctor_ptr=self.doctor
        )
        self.other_doctor = DoctorFactory(password='password')
        self.patient = PatientFactory.create()
        self.consent_doc = ConsentDocFactory.create()

    def get_post_data(self):
        return {
            'title': 'sample study',
            'doctors': [self.doctor.pk],
            'patients': [self.patient.pk],
            'consent_docs': [self.consent_doc.pk]
        }

    def test_create_unauthorized_forbidden(self):
        response = self.client.post('/api/v1/study/', self.get_post_data(),
                                    format='json')
        self.assertForbidden(response)

    def test_create_other_doctor_forbidden(self):
        self.authenticate_as_doctor(self.other_doctor)
        response = self.client.post('/api/v1/study/', self.get_post_data(),
                                    format='json')
        self.assertForbidden(response)

    def test_create_doctor_success(self):
        initial_studies_count = Study.objects.all().count()

        self.authenticate_as_doctor()
        response = self.client.post('/api/v1/study/', self.get_post_data(),
                                    format='json')
        self.assertSuccessResponse(response)
        self.assertEqual(Study.objects.all().count(), initial_studies_count+1)
        data = response.data
        data.pop('id')
        self.assertDictEqual(data, self.get_post_data())

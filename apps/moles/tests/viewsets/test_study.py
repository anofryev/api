from apps.main.tests import APITestCase
from apps.accounts.factories import CoordinatorFactory, DoctorFactory, \
    PatientFactory
from apps.moles.factories.study import ConsentDocFactory, StudyFactory, \
    StudyToPatient
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

    def target_path(self, pk):
        return '/api/v1/study/{0}/'.format(pk)

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
        self.assertTrue(data['pk'] > 0)
        self.assertEqual(data['title'], 'sample study')

    def test_list(self):
        self.authenticate_as_doctor()
        resp = self.client.get('/api/v1/study/', format='json')
        self.assertEqual(len(resp.data), 0)
        StudyFactory.create()
        StudyFactory.create()
        resp = self.client.get('/api/v1/study/', format='json')
        self.assertEqual(len(resp.data), 2)

    def test_list_forbidden(self):
        StudyFactory.create()
        resp = self.client.get('/api/v1/study/', format='json')
        self.assertForbidden(resp)

    def test_retrieve_forbidden(self):
        study = StudyFactory.create()
        resp = self.client.get(self.target_path(study.pk), format='json')
        self.assertForbidden(resp)

    def test_retrieve_get(self):
        study = StudyFactory.create()
        self.authenticate_as_doctor()
        resp = self.client.get(self.target_path(study.pk), format='json')
        self.assertSuccessResponse(resp)

    def test_update_and_check_changes(self):
        study = StudyFactory.create()
        initial_title = study.title
        self.authenticate_as_doctor()
        self.client.put(self.target_path(study.pk),
                        {'title': 'test'}, format='json')
        study.refresh_from_db()
        self.assertNotEqual(initial_title, study.title)

    def test_update_unauthorized(self):
        study = StudyFactory.create()
        resp = self.client.put(self.target_path(study.pk),
                               {'title': 'test'}, format='json')
        self.assertForbidden(resp)

    def test_update_doctor(self):
        study = StudyFactory.create()
        self.authenticate_as_doctor(doctor=self.other_doctor)
        resp = self.client.put(self.target_path(study.pk),
                               {'title': 'test'}, format='json')
        self.assertForbidden(resp)

    def test_delete_unauthorized(self):
        study = StudyFactory.create()
        resp = self.client.delete(self.target_path(study.pk))
        self.assertForbidden(resp)

    def test_delete_doctor(self):
        study = StudyFactory.create()
        self.authenticate_as_doctor(doctor=self.other_doctor)
        resp = self.client.delete(self.target_path(study.pk))
        self.assertForbidden(resp)

    def test_delete_coordinator(self):
        study = StudyFactory.create()
        initial_study_count = Study.objects.all().count()
        self.authenticate_as_doctor()
        self.client.delete(self.target_path(study.pk))
        self.assertNotEqual(initial_study_count, Study.objects.all().count())

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
        self.assertTrue(data['pk'] > 0)
        self.assertEqual(data['title'], 'sample study')

    # Остальные тесты:
    '''
    I. List
    1. Создать 2 Study, сделать GET, посмотреть что они там есть
    2. Создать Study, сделать GET от не авторизованного, убедиться, что forbidden
    
    II. Retrieve
    1. forbidden от не авторизованного
    2. GET от авторизованного
    
    III. Create
    Все есть, добавить в тесте где success проверку, что создастся моделька StudyToPatient,
    и что в ней будет patient_consent = None
    
    IV. Update
    Обновлять может только координатор
    1. Создать study, сделать PUT, посмотреть, что данные изменятся
    2. Создать study, задать в StudyToPatient patient_consent, сделать PUT, проверить, что останется подписанной
    3. Forbidden тест на неавторизованного
    4. Forbidden тест на доктора
    
    V. Delete
    Удалять может только координатор
    1. Forbidden unauthorized
    2. Forbidden doctor
    3. Создать study, сделать запрос на удаление, проверить, что удалится, проверить, что связка StudyToPatient тоже
    '''
from apps.main.tests import APITestCase
from apps.accounts.factories import CoordinatorFactory, DoctorFactory, \
    PatientFactory, ParticipantFactory
from apps.moles.factories.study import ConsentDocFactory, StudyFactory
from apps.moles.factories.study_invitation import StudyInvitationFactory
from apps.moles.models import Study, StudyInvitation


class StudyViewSetTest(APITestCase):
    def setUp(self):
        super(StudyViewSetTest, self).setUp()

        self.coordinator = CoordinatorFactory.create(
            doctor_ptr=self.doctor
        )
        self.other_doctor = DoctorFactory(password='password')
        self.patient = PatientFactory.create()
        self.consent_doc = ConsentDocFactory.create()

    def get_post_data(self):
        return {
            'title': 'sample study',
            'consent_docs': [self.consent_doc.pk]
        }

    def get_post_for_create_doctor(self, doctor_pk, emails):
        return {
            'doctor_pk': doctor_pk,
            'emails': emails
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

    def test_add_doctor(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        self.authenticate_as_doctor()
        emails = [doctor.email, self.doctor.email,
                  patient.email, 'test@test.com']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': doctor.pk,
                'emails': emails
            },
            format='json')
        self.assertSuccessResponse(resp)
        invitations = StudyInvitation.objects.all()
        self.assertEqual(len(invitations), 2)
        self.assertSetEqual(set(invitations.values_list('email', flat=True)),
                            {'test@test.com', patient.email})
        self.assertSetEqual(set(resp.data['fail_emails']),
                            {doctor.email, self.doctor.email})

    def test_add_doctor_forbidden(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        emails = [doctor.email, self.doctor.email,
                  patient.email, 'test@test.com']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': doctor.pk,
                'emails': emails
            },
            format='json')
        self.assertForbidden(resp)

    def test_add_doctor_bad_emails(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        self.authenticate_as_doctor()
        emails = [doctor.email, self.doctor.email,
                  patient.email, 'test@test.com', 'bad_email']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': doctor.pk,
                'emails': emails
            },
            format='json')
        self.assertBadRequest(resp)

    def test_add_doctor_bad_doctor_pk(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        self.authenticate_as_doctor()
        emails = [doctor.email, self.doctor.email,
                  patient.email, 'test@test.com']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': 999999,
                'emails': emails
            },
            format='json')
        self.assertNotFound(resp)

    def test_add_doctor_already_in_study(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        study.doctors.add(doctor)
        study.save()

        self.authenticate_as_doctor()
        emails = [doctor.email, self.doctor.email,
                  patient.email, 'test@test.com']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': doctor.pk,
                'emails': emails
            },
            format='json')
        self.assertBadRequest(resp)

    def test_add_doctor_invited_email(self):
        study = StudyFactory.create()
        doctor = DoctorFactory.create(my_coordinator=self.coordinator)
        patient = DoctorFactory.create()
        ParticipantFactory.create(
            doctor_ptr=patient
        )
        self.authenticate_as_doctor()

        StudyInvitationFactory.create(
            email='test@test.com',
            study=study
        )
        emails = ['test@test.com']
        resp = self.client.post(
            '/api/v1/study/{0}/add_doctor/'.format(study.pk),
            {
                'doctor_pk': doctor.pk,
                'emails': emails
            },
            format='json')
        self.assertSuccessResponse(resp)
        self.assertSetEqual(set(resp.data['fail_emails']),
                            {'test@test.com'})

from apps.accounts.factories import PatientConsentFactory, CoordinatorFactory
from apps.main.tests import APITestCase
from apps.moles.factories.study import StudyFactory
from apps.moles.models import StudyToPatient
from apps.moles.models.study_invitation import StudyInvitation, \
    StudyInvitationStatus
from apps.accounts.models import DoctorToPatient
from apps.accounts.factories.doctor import DoctorFactory
from apps.accounts.factories.participant import ParticipantFactory
from apps.accounts.factories.patient import PatientFactory
from apps.moles.factories.study_invitation import StudyInvitationFactory


class StudyInvitationViewSetTest(APITestCase):
    def setUp(self):
        super(StudyInvitationViewSetTest, self).setUp()

    def test_permission(self):
        resp = self.client.get('/api/v1/study/invites/')
        self.assertForbidden(resp)
        self.authenticate_as_doctor()
        resp = self.client.get('/api/v1/study/invites/')
        self.assertForbidden(resp)

    def test_list(self):
        StudyInvitationFactory.create()
        StudyInvitationFactory.create()
        self.assertEqual(len(StudyInvitation.objects.all()), 2)

    def test_approve(self):
        coordinator = DoctorFactory.create()
        coordinator_ptr = CoordinatorFactory.create(doctor_ptr=coordinator)
        doctor = DoctorFactory.create(my_coordinator=coordinator_ptr)
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        patient = PatientFactory.create(doctor=participant)
        study = StudyFactory.create()
        study_invitation = StudyInvitationFactory.create(
            study=study,
            email=participant.email,
            doctor=doctor)
        self.authenticate_as_doctor(doctor=participant)
        consent = PatientConsentFactory.create(patient=patient)
        resp = self.client.post(
            '/api/v1/study/invites/{0}/approve/'.format(study_invitation.pk), {
                'doctor_encryption_key': 'qwertyuiop',
                'coordinator_encryption_key': 'iqwjgipwqjeg',
                'consent_pk': consent.pk
            },
            format='json')
        self.assertSuccessResponse(resp)
        study.refresh_from_db()
        study_invitation.refresh_from_db()
        self.assertEqual(study_invitation.status,
                         StudyInvitationStatus.ACCEPTED)

        doc_to_patient = DoctorToPatient.objects.get(
            doctor=doctor,
            patient=patient)
        self.assertEqual(doc_to_patient.encrypted_key, 'qwertyuiop')

        coordinator_to_patient = DoctorToPatient.objects.get(
            doctor=coordinator,
            patient=patient)
        self.assertEqual(coordinator_to_patient.encrypted_key, 'iqwjgipwqjeg')

        study_to_patient = StudyToPatient.objects.get(
            study=study,
            patient=patient
        )
        self.assertEqual(study_to_patient.patient_consent.pk, consent.pk)
        self.assertListEqual(list(study.patients.all()), [patient])

    def test_approve_with_invalid_id(self):
        doctor = DoctorFactory.create()
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        PatientFactory.create(doctor=participant)
        study_invitation = StudyInvitationFactory.create(
            email=participant.email,
            doctor=doctor)
        consent = PatientConsentFactory.create()
        self.authenticate_as_doctor(doctor=participant)
        resp = self.client.post(
            '/api/v1/study/invites/{0}/approve/'.format(study_invitation.pk), {
                'doctor_encryption_key': 'qwertyuiop',
                'consent_pk': consent.pk
            },
            format='json')
        self.assertBadRequest(resp)

    def test_approve_invalid_consent(self):
        doctor = DoctorFactory.create()
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        PatientFactory.create(doctor=participant)
        study = StudyFactory.create()
        study_invitation = StudyInvitationFactory.create(
            study=study,
            email=participant.email,
            doctor=doctor)
        self.authenticate_as_doctor(doctor=participant)
        consent = PatientConsentFactory.create()
        resp = self.client.post(
            '/api/v1/study/invites/{0}/approve/'.format(study_invitation.pk), {
                'doctor_encryption_key': 'qwertyuiop',
                'consent_pk': consent.pk
            },
            format='json')
        self.assertBadRequest(resp)

    def test_decline(self):
        doctor = DoctorFactory.create()
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        study_invitation = StudyInvitationFactory.create(
            email=participant.email,
            doctor=doctor)
        self.authenticate_as_doctor(doctor=participant)
        resp = self.client.post('/api/v1/study/invites/{0}/decline/'
                                .format(study_invitation.pk),
                                format='json')
        self.assertSuccessResponse(resp)
        self.assertEqual(StudyInvitation.objects.all().first().status,
                         StudyInvitationStatus.DECLINED)

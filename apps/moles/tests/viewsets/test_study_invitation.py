from apps.main.tests import APITestCase
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

    def get_post_data(self, ek):
        return

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
        doctor = DoctorFactory.create()
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        patient = PatientFactory.create(doctor=participant)
        study_invitation = StudyInvitationFactory.create(
            email=participant.email,
            doctor=doctor)
        self.authenticate_as_doctor(doctor=participant)
        resp = self.client.post(
            '/api/v1/study/invites/{0}/approve/'.format(study_invitation.pk), {
                'encryption_keys': {doctor.pk: 'qwertyuiop'}
            },
            format='json')
        self.assertSuccessResponse(resp)
        study_invitation.refresh_from_db()
        self.assertEqual(study_invitation.status,
                         StudyInvitationStatus.ACCEPTED)
        doc_to_patient = DoctorToPatient.objects.get(doctor=doctor,
                                                     patient=patient)
        self.assertEqual(doc_to_patient.encrypted_key, 'qwertyuiop')


    def test_approve_with_invalid_id(self):
        doctor = DoctorFactory.create()
        participant = DoctorFactory.create()
        ParticipantFactory.create(doctor_ptr=participant)
        PatientFactory.create(doctor=participant)
        study_invitation = StudyInvitationFactory.create(
            email=participant.email,
            doctor=doctor)
        self.authenticate_as_doctor(doctor=participant)
        resp = self.client.post(
            '/api/v1/study/invites/{0}/approve/'.format(study_invitation.pk), {
                'encryption_keys': {20: 'qwertyuiop'}
            },
            format='json')
        self.assertEqual(["You doesn't not pass encryption key of doctor"],
                         resp.data)

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

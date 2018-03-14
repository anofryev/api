import json

from apps.main.tests import APITestCase
from apps.moles.models.study_invitation import StudyInvitation, \
    StudyInvitationStatus
from apps.accounts.models.doctor import Doctor
from apps.accounts.factories.doctor import DoctorFactory
from apps.accounts.factories.participant import ParticipantFactory
from apps.moles.factories.study_invitation import StudyInvitationFactory


class StudyInvitationViewSetTest(APITestCase):
    def setUp(self):
        super(StudyInvitationViewSetTest, self).setUp()

    def get_post_data(self, ek):
        return {
            'encryption_keys': ek
        }

    def test_list(self):
        StudyInvitationFactory.create()
        StudyInvitationFactory.create()
        self.assertEqual(len(StudyInvitation.objects.all()), 2)

    def test_approve(self):
        pass
        # TODO: discuss this test with Sasha P.
        # doctor = DoctorFactory.create()
        # participant = DoctorFactory.create()
        # ParticipantFactory.create(doctor_ptr=participant)
        #
        # study_invitation = StudyInvitationFactory.create(
        #     email=participant.email,
        #     doctor=doctor)
        # encryption_keys = {study_invitation.doctor.pk: 'qwertyuiop'}
        # self.authenticate_as_doctor(doctor=participant)
        # resp = self.client.post('/api/v1/study/invites/{0}/approve/'
        #                  .format(study_invitation.pk),
        #                  self.get_post_data(ek=encryption_keys),
        #                  format='json')
        # self.assertSuccessResponse(resp)
        # self.assertEqual(StudyInvitation.objects.all().first().status,
        #                  StudyInvitationStatus.ACCEPTED)

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

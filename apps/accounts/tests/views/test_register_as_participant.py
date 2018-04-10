from apps.main.tests import APITestCase
from apps.accounts.factories.doctor import DoctorFactory


class RegisterAsParticipantViewTest(APITestCase):
    def test_success(self):
        resp = self.client.post('/api/v1/auth/register_as_participant/', {
            'email': 'test@test.com',
            'password': 'qwertyuiop',
        })
        self.assertSuccessResponse(resp)

    def test_existed_email_fail(self):
        doctor = DoctorFactory.create()
        resp = self.client.post('/api/v1/auth/register_as_participant/', {
            'email': doctor.email,
            'password': 'qwertyuiop',
        })
        self.assertBadRequest(resp)

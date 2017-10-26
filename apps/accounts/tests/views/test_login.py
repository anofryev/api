from apps.main.tests import APITestCase
from ...factories import DoctorFactory


class LoginViewTest(APITestCase):
    def test_login_as_doctor_success(self):
        doctor = DoctorFactory.create(password='qwertyuiop')

        resp = self.client.post('/api/v1/auth/login/', {
            'username': doctor.username,
            'password': 'qwertyuiop',
        })
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertIsNotNone(data.get('token', None))
        self.assertIsNotNone(data.get('doctor', None))
        self.assertEqual(data['doctor']['pk'], doctor.pk)

from ..factories import DoctorFactory, PatientFactory
from .api_test_case import APITestCase


class ViewsTest(APITestCase):
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

    def test_login_as_patient_success(self):
        patient = PatientFactory.create(password='qwertyuiop')

        resp = self.client.post('/api/v1/auth/login/', {
            'username': patient.username,
            'password': 'qwertyuiop',
        })
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertIsNotNone(data.get('token', None))
        self.assertIsNone(data.get('doctor', None))

    def test_authenticate_success(self):
        resp = self.client.get('/api/v1/accounts/patient/')
        self.assertIsNone(resp.wsgi_request.user.pk)

        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/accounts/patient/')
        self.assertEqual(resp.wsgi_request.user.pk, self.doctor.pk)

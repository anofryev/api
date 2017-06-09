from apps.main.tests import APITestCase
from ...factories import DoctorFactory, PatientFactory
from ...models import UnitsOfLengthEnum


class CurrentUserViewTest(APITestCase):
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
        resp = self.client.get('/api/v1/patient/')
        self.assertIsNone(resp.wsgi_request.user.pk)

        self.authenticate_as_doctor()

        resp = self.client.get('/api/v1/patient/')
        self.assertEqual(resp.wsgi_request.user.pk, self.doctor.pk)

    def test_get_current_user_for_unauthorized_failed(self):
        resp = self.client.get('/api/v1/auth/current_user/')
        self.assertForbidden(resp)

    def test_get_current_user_success(self):
        self.authenticate_as_doctor()
        resp = self.client.get('/api/v1/auth/current_user/')
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(data['pk'], self.doctor.pk)

    def test_update_current_user_for_unauthorized_failed(self):
        resp = self.client.patch('/api/v1/auth/current_user/')
        self.assertForbidden(resp)

    def test_update_current_user_success(self):
        self.authenticate_as_doctor()
        doctor_data = {
            'first_name': 'new',
            'last_name': 'new',
            'email': 'new@email.com',
            'units_of_length': UnitsOfLengthEnum.CENTIMETER,
            'degree': 'new',
            'department': 'new',
        }
        resp = self.client.patch('/api/v1/auth/current_user/', doctor_data)
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(data['pk'], self.doctor.pk)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.first_name, doctor_data['first_name'])
        self.assertEqual(self.doctor.last_name, doctor_data['last_name'])
        self.assertEqual(self.doctor.email, doctor_data['email'])
        self.assertEqual(self.doctor.username, doctor_data['email'])
        self.assertEqual(self.doctor.units_of_length,
                         doctor_data['units_of_length'])
        self.assertEqual(self.doctor.degree, doctor_data['degree'])
        self.assertEqual(self.doctor.department, doctor_data['department'])
        self.assertTrue(self.doctor.check_password('password'))

    def test_update_password_success(self):
        self.authenticate_as_doctor()
        doctor_data = {
            'password': 'newpassword',
        }
        resp = self.client.patch(
            '/api/v1/auth/current_user/', doctor_data)
        self.assertSuccessResponse(resp)
        self.doctor.refresh_from_db()
        self.assertTrue(self.doctor.check_password(doctor_data['password']))

    def test_update_password_to_empty_bad_request(self):
        self.authenticate_as_doctor()
        doctor_data = {
            'password': '',
        }
        resp = self.client.patch(
            '/api/v1/auth/current_user/', doctor_data)
        self.assertBadRequest(resp)

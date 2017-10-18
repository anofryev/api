from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework import status

from apps.accounts.factories import DoctorFactory
from .mixins import FileTestMixin


class APITestCase(FileTestMixin, BaseAPITestCase):
    def setUp(self):
        super(APITestCase, self).setUp()

        self.doctor = DoctorFactory(password='password')

    def assertSuccessResponse(self, resp):
        if resp.status_code not in range(200, 300):
            raise self.failureException(
                'Response status is not success. Status code: {0}\n'
                'Response data is:\n{1}'.format(resp.status_code, resp.data))

    def assertNotAllowed(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def assertBadRequest(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def assertUnauthorized(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def get_token(self, doctor=None):
        doctor = doctor or self.doctor
        resp = self.client.post('/api/v1/auth/login/', {
            'username': doctor.username,
            'password': 'password',
        })
        self.assertSuccessResponse(resp)
        return resp.data['token']

    def authenticate_as_doctor(self, doctor=None):
        token = self.get_token(doctor)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token)
        )

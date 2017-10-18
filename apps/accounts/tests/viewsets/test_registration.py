from factory import Faker
from apps.main.tests import APITestCase

from ...factories import SiteFactory, UserFactory
from ...models import (
    User, Coordinator, Doctor, SiteJoinRequest,
    SiteJoinRequest, JoinStateEnum, )


class RegistrationTest(APITestCase):
    def setUp(self):
        super(RegistrationTest, self).setUp()
        self.coordinator = Coordinator.objects.create(doctor_ptr=self.doctor)
        self.site = SiteFactory.create(site_coordinator=self.coordinator)

    def do_login(self, credentials):
        return self.client.post('/api/v1/auth/login/', {
            'username': credentials['username'],
            'password': credentials['password'],
        })

    def assertCanLogin(self, credentials):
        resp = self.do_login(credentials)
        self.assertSuccessResponse(resp)
        self.assertIsNotNone(resp.data['token'])

    def assertCanNotLogin(self, credentials):
        resp = self.do_login(credentials)
        self.assertBadRequest(resp)

    def test_that_doctor_can_register_individual(self):
        data = {
            'first_name': Faker('first_name').generate({}),
            'last_name': Faker('last_name').generate({}),
            'email': Faker('email').generate({}),
            'password': Faker('password').generate({}),
        }
        resp = self.client.post('/api/v1/auth/register/', data)
        self.assertSuccessResponse(resp)

        credentials = {
            'username': data['email'],
            'password': data['password'],
        }

        self.assertCanNotLogin(credentials)

        # Activating user
        User.objects.filter(id=resp.data['pk']).update(is_active=True)

        self.assertCanLogin(credentials)

    def test_that_doctor_can_register_as_part_of_the_group(self):
        data = {
            'first_name': Faker('first_name').generate({}),
            'last_name': Faker('last_name').generate({}),
            'email': Faker('email').generate({}),
            'password': Faker('password').generate({}),
            'site': self.site.id,
        }
        resp = self.client.post('/api/v1/auth/register/', data)
        self.assertSuccessResponse(resp)

        credentials = {
            'username': data['email'],
            'password': data['password'],
        }

        self.assertCanNotLogin(credentials)

        # Activating user
        User.objects.filter(id=resp.data['pk']).update(is_active=True)
        self.assertTrue(
            SiteJoinRequest.objects.filter(
                state=JoinStateEnum.NEW,
                doctor_id=resp.data['pk'],
                site=self.site).exists())

        self.assertCanLogin(credentials)

    def test_that_reqular_admin_user_can_login(self):
        password = Faker('password').generate({})
        user = UserFactory.create(is_staff=True, password=password)
        self.assertTrue(
            self.client.login(username=user.username, password=password))

from factory import fuzzy
from django.core import urlresolvers
from django.test import TestCase

from ...factories import DoctorFactory


class DoctorAdminTest(TestCase):
    def setUp(self):
        self.password = fuzzy.FuzzyText().fuzz()
        self.superuser = DoctorFactory.create(
            password=self.password, is_superuser=True, is_staff=True)

    def test_doctor_edit(self):
        DoctorFactory.create(coordinator=True)
        self.client.login(
            username=self.superuser.username, password=self.password)

        response = self.client.get(
            urlresolvers.reverse(
                'admin:accounts_doctor_change', args=[self.superuser.pk]))

        # We just need to check that Doctor get_from override don't raise
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            len(response.context['adminform'].form.fields.values()) > 0)

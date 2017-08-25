from factory import fuzzy
from django.core import urlresolvers
from django.test import TestCase

from ...factories import DoctorFactory


class CoordinatorAdminTest(TestCase):
    def setUp(self):
        self.password = fuzzy.FuzzyText().fuzz()
        self.superuser = DoctorFactory.create(
            password=self.password, is_superuser=True, is_staff=True)

    def test_coordinator_change_list(self):
        self.client.login(
            username=self.superuser.username, password=self.password)

        responce = self.client.get(
            urlresolvers.reverse('admin:accounts_coordinator_changelist'))
        self.assertEqual(responce.context['cl'].result_count, 0)

        DoctorFactory.create(coordinator=True)

        responce = self.client.get(
            urlresolvers.reverse('admin:accounts_coordinator_changelist'))
        self.assertEqual(responce.context['cl'].result_count, 1)

    def test_coordinator_add(self):
        self.client.login(
            username=self.superuser.username, password=self.password)

        responce = self.client.get(
            urlresolvers.reverse('admin:accounts_coordinator_add'))
        self.assertEqual(responce.context['adminform'].form.fields.get(
            'doctor_ptr').queryset.count(), 1)

        DoctorFactory.create()
        DoctorFactory.create(coordinator=True)

        responce = self.client.get(
            urlresolvers.reverse('admin:accounts_coordinator_add'))
        self.assertEqual(responce.context['adminform'].form.fields.get(
            'doctor_ptr').queryset.count(), 2)

    def test_coordinator_edit(self):
        coordinator = DoctorFactory.create(coordinator=True)
        self.client.login(
            username=self.superuser.username, password=self.password)

        responce = self.client.get(
            urlresolvers.reverse(
                'admin:accounts_coordinator_change', args=[coordinator.pk]))

        self.assertEqual(
            len(responce.context['adminform'].form.fields.values()), 0)

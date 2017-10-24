from django.test import TestCase

from templated_mail.mail import BaseEmailMessage

from ..models.site_join_request import GetProtocolFromSettingsMixin


class SomeMail(GetProtocolFromSettingsMixin, BaseEmailMessage):
    pass


class GetProtocolFromSettingsMixinTestCase(TestCase):
    def test_that_context_contain_protocol(self):
        email = SomeMail()
        self.assertEqual(
            email.get_context_data()['protocol'], 'http')

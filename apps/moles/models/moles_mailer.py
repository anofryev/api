from django.conf import settings

from templated_mail.mail import BaseEmailMessage


class GetProtocolFromSettingsMixin:
    def get_context_data(self):
        context = super(GetProtocolFromSettingsMixin,
                        self).get_context_data()
        context['protocol'] = settings.PROTOCOL
        return context


class AddParticipantNotification(GetProtocolFromSettingsMixin,
                                          BaseEmailMessage):
    template_name = 'email/participant_notification.html'

    def get_context_data(self):
        context = super(AddParticipantNotification,
                        self).get_context_data()
        context['url'] = "{}://{}#/doctor-registration-requests".format(
            context['protocol'], settings.DOMAIN)
        return context

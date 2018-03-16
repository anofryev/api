from django.conf import settings

from templated_mail.mail import BaseEmailMessage


class AddParticipantNotification(BaseEmailMessage):
    template_name = 'email/participant_notification.html'

    def get_context_data(self):
        context = super(AddParticipantNotification,
                        self).get_context_data()
        context['url'] = "{}://{}#/doctor-registration-requests".format(
            context['protocol'], settings.DOMAIN)
        return context

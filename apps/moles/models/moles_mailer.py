from django.conf import settings

from templated_mail.mail import BaseEmailMessage


class AddParticipantNotification(BaseEmailMessage):
    template_name = 'email/participant_notification.html'

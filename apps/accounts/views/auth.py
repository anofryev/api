from django.conf import settings

from djoser.views import PasswordResetConfirmView, RegistrationView

from rest_framework import serializers
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from templated_mail.mail import BaseEmailMessage

from ..models import Doctor


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        errors = []
        if Doctor.objects.filter(
                username=attrs.get('username', None),
                approved_by_coordinator=False).exists():
            errors.append("Account is not approved by your coordinator")
        if Doctor.objects.filter(
                username=attrs.get('username', None),
                is_active=False).exists():
            errors.append("Account is not activated")

        if errors != []:
            raise serializers.ValidationError(errors)

        return super(CustomJSONWebTokenSerializer, self).validate(attrs)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def _action(self, serializer):
        result = super(MyPasswordResetConfirmView, self)._action(serializer)
        doctor = serializer.user.doctor
        doctor.private_key = ''
        doctor.save()
        return result


reset_confirmation_view = MyPasswordResetConfirmView.as_view()


class CoordinatorRegistrationNotification(BaseEmailMessage):
    template_name = 'email/coordnator_notification.html'

    def set_context_data(self):
        super(CoordinatorRegistrationNotification, self).set_context_data()
        self.context['url'] = "{}#/doctor-registration-requests".format(
            settings.DJOSER['DOMAIN'])


class MyRegistrationView(RegistrationView):
    def perform_create(self, serializer):
        result = super(MyRegistrationView, self).perform_create(serializer)
        doctor = serializer.instance
        if doctor.my_coordinator_id:
            to = [Doctor.objects.get(id=doctor.my_coordinator_id).email]
            CoordinatorRegistrationNotification(
                self.request,
                {'doctor': "{0} {1}".format(
                    doctor.first_name,
                    doctor.last_name)}).send(to)
        return result


registration_view = MyRegistrationView.as_view()

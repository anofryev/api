from django.contrib.auth.backends import ModelBackend
from .models import Doctor


class AuthenticationBackend(ModelBackend):
    def user_can_authenticate(self, user):
        doctor = Doctor.objects.filter(id=user.id).first()
        if doctor:
            return doctor.approved_by_coordinator and user.is_active
        else:
            return user.is_active

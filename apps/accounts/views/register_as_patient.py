from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny

from ..serializers import DoctorFullSerializer


class RegisterAsPatientView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = None

    def get_serializer_class(self):
        user = self.request.user

        if hasattr(user, 'doctor_role'):
            return DoctorFullSerializer

        raise NotImplementedError

    def create(self, request, *args, **kwargs):
        pass
        # takes:
        # 1. doctor registration params (see RegisterDoctorSerializer)
        # 2. encryption keys
        # creates patient and doctor-to-patient for this doctor
        # and for all doctors in invites


register_as_patient_view = RegisterAsPatientView.as_view()

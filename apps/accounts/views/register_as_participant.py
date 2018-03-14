from rest_framework import generics
from rest_framework.permissions import AllowAny

from ..serializers import RegisterParticipantSerializer


class RegisterAsParticipantView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterParticipantSerializer


register_as_participant_view = RegisterAsParticipantView.as_view()

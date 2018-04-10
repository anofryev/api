from djoser.views import UserCreateView
from rest_framework.permissions import AllowAny

from ..serializers import RegisterParticipantSerializer


class RegisterAsParticipantView(UserCreateView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterParticipantSerializer


register_as_participant_view = RegisterAsParticipantView.as_view()

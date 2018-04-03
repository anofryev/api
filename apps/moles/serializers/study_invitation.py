from rest_framework import serializers

from apps.accounts.serializers import DoctorWithKeysSerializer
from .study import StudyListSerializer
from ..models import StudyInvitation


class StudyInvitationSerializer(serializers.ModelSerializer):
    doctor = DoctorWithKeysSerializer()
    study = StudyListSerializer()

    class Meta:
        model = StudyInvitation
        fields = ('pk', 'email', 'study', 'doctor', 'status')

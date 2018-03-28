from rest_framework import serializers

from apps.accounts.serializers import DoctorSerializer
from .study import StudyListSerializer
from ..models import StudyInvitation


class StudyInvitationSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    study = StudyListSerializer()

    class Meta:
        model = StudyInvitation
        fields = ('pk', 'email', 'study', 'doctor', 'status')

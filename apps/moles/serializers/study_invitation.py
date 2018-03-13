from rest_framework import serializers

from ..models import StudyInvitation


class StudyInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyInvitation
        fields = ('pk', 'email', 'study', 'doctor', 'status')

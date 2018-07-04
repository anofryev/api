from rest_framework import serializers

from apps.accounts.models import Doctor
from apps.accounts.serializers import DoctorWithKeysSerializer, \
    DoctorKeySerializer
from .study import StudyListSerializer
from ..models import StudyInvitation


class StudyInvitationSerializer(serializers.ModelSerializer):
    doctor = DoctorWithKeysSerializer()
    study = StudyListSerializer()

    class Meta:
        model = StudyInvitation
        fields = ('pk', 'email', 'study', 'doctor', 'status')


class StudyInvitationForDoctorSerializer(StudyInvitationSerializer):
    participant = serializers.SerializerMethodField()

    def get_participant(self, obj):
        participant = Doctor.objects.filter(
            participant_role__isnull=False,
            email=obj.email
        ).first()
        if not participant:
            return None

        return DoctorKeySerializer(participant).data

    class Meta(StudyInvitationSerializer.Meta):
        fields = StudyInvitationSerializer.Meta.fields + ('participant',)

from rest_framework import serializers

from apps.accounts.models import Doctor
from apps.accounts.serializers import DoctorWithKeysSerializer, \
    DoctorKeySerializer
from .study import StudyListSerializer
from ..models import StudyInvitation


class StudyInvitationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyInvitation
        fields = ('pk', 'email', 'study', 'doctor', 'status', 'patient')


class StudyInvitationSerializer(StudyInvitationBaseSerializer):
    doctor = DoctorWithKeysSerializer()
    study = StudyListSerializer()

    class Meta(StudyInvitationBaseSerializer.Meta):
        pass


class StudyInvitationForDoctorSerializer(StudyInvitationSerializer):
    participant = serializers.SerializerMethodField()

    def get_participant(self, obj):
        participant = Doctor.objects.filter(
            participant_role__isnull=False,
            email=obj.email
        ).first()
        if not participant:
            return None

        return DoctorKeySerializer(participant, context=self.context).data

    class Meta(StudyInvitationSerializer.Meta):
        fields = StudyInvitationSerializer.Meta.fields + ('participant',)

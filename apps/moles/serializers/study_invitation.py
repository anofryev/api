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
        fields = ('pk', 'email', 'study', 'doctor', 'status', 'patient')


class StudyInvitationForDoctorSerializer(StudyInvitationSerializer):
    participant = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()  # To avoid cross imports

    def get_participant(self, obj):
        participant = Doctor.objects.filter(
            participant_role__isnull=False,
            email=obj.email
        ).first()
        if not participant:
            return None

        return DoctorKeySerializer(participant).data

    def get_patient(self, obj):
        from apps.accounts.serializers.patient import PatientSerializer
        return PatientSerializer(obj.patient).data

    class Meta(StudyInvitationSerializer.Meta):
        fields = StudyInvitationSerializer.Meta.fields + ('participant',)

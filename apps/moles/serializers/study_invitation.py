from rest_framework import serializers

from apps.accounts.models import Doctor
from apps.accounts.serializers import DoctorWithKeysSerializer, \
    DoctorKeySerializer
from .study import StudyListSerializer
from ..models import StudyInvitation


class StudyInvitationBaseSerializer(serializers.ModelSerializer):
    def validate(self, validated_data):
        email = validated_data['email']
        study = validated_data['study']
        doctor = validated_data['doctor']

        if StudyInvitation.objects.filter(
                email=email,
                study=study,
                doctor=doctor).exists():
            raise serializers.ValidationError(
                '{0} already invited to {1} by {2}'.format(
                    email, study, doctor))

        return validated_data

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
    patient = serializers.SerializerMethodField()  # To avoid cross import

    def get_participant(self, obj):
        participant = Doctor.objects.filter(
            participant_role__isnull=False,
            email=obj.email
        ).first()
        if not participant:
            return None

        return DoctorKeySerializer(participant, context=self.context).data

    def get_patient(self, obj):
        from apps.accounts.serializers.patient import PatientSerializer
        return PatientSerializer(obj.patient, context=self.context).data

    class Meta(StudyInvitationSerializer.Meta):
        fields = StudyInvitationSerializer.Meta.fields + ('participant',)

from rest_framework import serializers

from apps.accounts.models import Doctor, DoctorToPatient
from apps.accounts.serializers import DoctorSerializer
from apps.moles.models import StudyToPatient
from ..models import ConsentDoc, Study


class ConsentDocSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = ConsentDoc
        fields = ('pk', 'file', 'thumbnail', 'original_filename')


class StudyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ('pk', 'title', 'consent_docs')


class StudyLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ('pk', 'title', 'consent_docs', 'author')


class StudyListSerializer(serializers.ModelSerializer):
    consent_docs = ConsentDocSerializer(many=True)
    doctors = DoctorSerializer(many=True)
    consents_validity = serializers.SerializerMethodField()

    class Meta(StudyBaseSerializer.Meta):
        fields = ('pk', 'title', 'doctors', 'patients',
                  'consent_docs', 'consents_validity')

    def get_consents_validity(self, obj):
        from apps.accounts.serializers import PatientConsentSerializer

        doctor = self.context['request'].user.doctor_role

        study_to_patients = StudyToPatient.objects.filter(
            study=obj,
            patient_id__in=DoctorToPatient.objects.filter(
                doctor=doctor).values_list('patient_id', flat=True))

        result = {}
        for study_to_patient in study_to_patients:
            result[study_to_patient.patient_id] = PatientConsentSerializer(
                study_to_patient.patient_consent).data

        return result


class AddDoctorSerializer(serializers.Serializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_pk = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        required=True)
    emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False)

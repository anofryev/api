from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Patient, DoctorToPatient
from .patient_consent import PatientConsentSerializer


class PatientSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    valid_consent = PatientConsentSerializer(allow_null=True, read_only=True)
    encrypted_key = serializers.SerializerMethodField()

    # Fields from aggregation
    last_upload = serializers.DateTimeField(read_only=True)
    moles_images_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn',
                  'date_of_birth', 'mrn_hash',
                  'sex', 'race', 'photo', 'last_upload',
                  'moles_images_count', 'valid_consent',
                  'encrypted_key', )

    def get_encrypted_key(self, patient):
        doctor = self.context['request'].user.doctor_role
        return DoctorToPatient.objects.filter(
            doctor=doctor,
            patient=patient).values_list(
                'encrypted_key', flat=True).first()


class CreatePatientSerializer(PatientSerializer):
    signature = Base64ImageField(required=True)
    encrypted_key = serializers.CharField(required=True)
    coordinator_encrypted_key = serializers.CharField(required=False)

    def validate(self, data):
        doctor = self.context['request'].user.doctor_role
        if doctor.my_coordinator_id is not None \
           and 'coordinator_encrypted_key' not in data:
            raise serializers.ValidationError(
                "Coordinator encrypted key "
                "is required for doctor with coordinator"
            )
        return data

    def create(self, validated_data):
        doctor = self.context['request'].user.doctor_role

        signature = validated_data.pop(
            'signature')
        encrypted_key = validated_data.pop(
            'encrypted_key')
        coordinator_encrypted_key = validated_data.pop(
            'coordinator_encrypted_key', None)

        patient = super(CreatePatientSerializer, self).create(validated_data)
        patient.consents.create(signature=signature)
        DoctorToPatient.objects.create(
            patient=patient,
            doctor=doctor,
            encrypted_key=encrypted_key)
        if doctor.my_coordinator_id:
            DoctorToPatient.objects.create(
                patient=patient,
                doctor_id=doctor.my_coordinator_id,
                encrypted_key=coordinator_encrypted_key)
        return patient

    class Meta:
        model = Patient
        fields = PatientSerializer.Meta.fields + (
            'signature', 'coordinator_encrypted_key', )

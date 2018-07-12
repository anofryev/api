import json
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from versatileimagefield.serializers import VersatileImageFieldSerializer

from apps.moles.serializers import StudyBaseSerializer
from apps.moles.models import StudyInvitation, StudyToPatient

from ..models import Patient, DoctorToPatient
from .patient_consent import PatientConsentSerializer


class IntDict(serializers.DictField):
    def to_internal_value(self, data):
        dict = super(IntDict, self).to_internal_value(json.loads(data))
        return {int(k): v for k, v in dict.items()}


class PatientSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    valid_consent = PatientConsentSerializer(allow_null=True, read_only=True)
    encrypted_key = serializers.SerializerMethodField()
    doctors = serializers.SerializerMethodField()
    encryption_keys = IntDict(child=serializers.CharField(), write_only=True)

    # Fields from aggregation
    moles_count = serializers.IntegerField(read_only=True)
    moles_images_count = serializers.IntegerField(read_only=True)
    last_upload = serializers.DateTimeField(read_only=True)
    moles_images_with_clinical_diagnosis_required = serializers.IntegerField(
        read_only=True)
    moles_images_with_pathological_diagnosis_required =\
        serializers.IntegerField(read_only=True)
    moles_images_biopsy_count = serializers.IntegerField(read_only=True)
    moles_images_approve_required = serializers.IntegerField(
        read_only=True)
    studies = StudyBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn',
                  'date_of_birth', 'mrn_hash', 'valid_consent',
                  'sex', 'race', 'photo', 'studies',
                  'encrypted_key', 'encryption_keys', 'doctors',
                  'moles_count',
                  'moles_images_count', 'last_upload',
                  'moles_images_with_clinical_diagnosis_required',
                  'moles_images_with_pathological_diagnosis_required',
                  'moles_images_biopsy_count',
                  'moles_images_approve_required', )

    def validate(self, data):
        doctor = self.context['request'].user.doctor_role
        encryption_keys = data.get('encryption_keys', {})
        if doctor.pk not in encryption_keys:
            raise serializers.ValidationError(
                "Your encrypted key is required"
            )

        if doctor.my_coordinator_id is not None \
           and doctor.my_coordinator_id not in encryption_keys:
            raise serializers.ValidationError(
                "Coordinator encrypted key "
                "is required for doctor with coordinator"
            )

        for rel in DoctorToPatient.objects.filter(
                patient=self.instance).select_related(
                    'doctor'):
            doctor = rel.doctor
            if doctor.id not in encryption_keys:
                raise serializers.ValidationError(
                    "Doctor encrypted key "
                    "is required for {0}".format(doctor)
                )

        return data

    def get_encrypted_key(self, patient):
        doctor = self.context['request'].user.doctor_role
        return DoctorToPatient.objects.filter(
            doctor=doctor,
            patient=patient).values_list(
                'encrypted_key', flat=True).first()

    def get_doctors(self, patient):
        return DoctorToPatient.objects.filter(patient=patient).values_list(
            'doctor_id',
            flat=True)

    def create(self, validated_data):
        encryption_keys = validated_data.pop('encryption_keys')
        patient = super(PatientSerializer, self).create(validated_data)
        self.update_relations(patient, encryption_keys)
        return patient

    def update(self, instance, validated_data):
        encryption_keys = validated_data.pop('encryption_keys')
        patient = super(PatientSerializer, self).update(instance,
                                                        validated_data)
        self.update_relations(patient, encryption_keys)
        return patient

    def update_relations(self, patient, encryption_keys):
        for doctor_id, encrypted_key in encryption_keys.items():
            DoctorToPatient.objects.update_or_create(
                doctor_id=doctor_id,
                patient=patient,
                defaults={'encrypted_key': encrypted_key})


class CreatePatientSerializer(PatientSerializer):
    signature = Base64ImageField(required=True)
    email = serializers.EmailField(required=False)
    study = serializers.IntegerField(required=False)

    def create(self, validated_data):
        signature = validated_data.pop('signature')
        email = validated_data.pop('email', None)
        study_pk = validated_data.pop('study', None)

        patient = super(CreatePatientSerializer, self).create(validated_data)
        patient.consents.create(signature=signature)

        if email and study_pk:
            doctor = self.context['request'].user.doctor_role
            StudyInvitation.objects.create(
                email=email,
                study_id=study_pk,
                doctor=doctor,
                patient=patient)

            StudyToPatient.objects.create(
                study_id=study_pk,
                patient=patient)

        return patient

    class Meta:
        model = Patient
        fields = PatientSerializer.Meta.fields + ('signature', 'email', 'study')

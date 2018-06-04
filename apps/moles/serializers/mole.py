import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from apps.moles.models import Study, StudyToPatient
from ..models import Mole, MoleImage
from .anatomical_site import AnatomicalSiteSerializer
from .patient_anatomical_site import PatientAnatomicalSiteSerializer
from .mole_image import MoleImageListSerializer


class MoleSerializer(serializers.ModelSerializer):
    anatomical_sites = AnatomicalSiteSerializer(many=True, read_only=True)
    position_info = serializers.JSONField()
    studies = serializers.ListField()

    class Meta:
        model = Mole


class MoleListSerializer(MoleSerializer):
    last_image = serializers.SerializerMethodField()
    images_count = serializers.IntegerField(
        read_only=True)
    images_with_pathological_diagnosis_required = serializers.IntegerField(
        read_only=True)
    images_with_clinical_diagnosis_required = serializers.IntegerField(
        read_only=True)
    images_biopsy_count = serializers.IntegerField(
        read_only=True)
    images_approve_required = serializers.IntegerField(
        read_only=True)

    def get_last_image(self, obj):
        study = self.context.get('study')
        try:
            image = obj.images.filter(study=study).latest('date_created')
            return MoleImageListSerializer(image, context=self.context).data
        except ObjectDoesNotExist:
            return None

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'last_image', 'images_count',
                  'position_info', 'patient_anatomical_site',
                  'images_with_clinical_diagnosis_required',
                  'images_with_pathological_diagnosis_required',
                  'images_biopsy_count',
                  'images_approve_required', 'studies')


class MoleDetailSerializer(MoleSerializer):
    patient_anatomical_site = PatientAnatomicalSiteSerializer(read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        study = self.context.get('study')
        images = obj.images.filter(study=study)
        return MoleImageListSerializer(
            images, context=self.context, many=True).data

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'patient_anatomical_site',
                  'position_info', 'images', 'studies')


def validate_position_info(self, value):
    try:
        return json.loads(value)
    except Exception as err:
        raise serializers.ValidationError(str(err))


def validate(self, data):
    if data.get('study', None):
        study_to_patient = StudyToPatient.objects.filter(
            study=data['study'],
            patient=self.context['view'].kwargs['patient_pk']
        ).first()
        if study_to_patient:
            consent = study_to_patient.patient_consent
            if consent and not consent.is_valid():
                raise serializers.ValidationError(
                    "Need to update study consent for patient")

    if data.get('patient_anatomical_site') is None or \
            data['patient_anatomical_site'].anatomical_site.pk \
            == data['anatomical_site'].pk:
        return data
    else:
        raise serializers.ValidationError(
            "Distant photo anatomical site missmatch mole's anatomical site")


class MoleCreateSerializer(MoleSerializer):
    photo = VersatileImageFieldSerializer(
        sizes='main_set', required=True, write_only=True)
    age = serializers.IntegerField(
        required=False,
        allow_null=True)
    study = serializers.PrimaryKeyRelatedField(
        queryset=Study.objects.all(),
        write_only=True,
        required=False)

    class Meta(MoleSerializer.Meta):
        fields = ('anatomical_site', 'patient_anatomical_site',
                  'position_info', 'photo', 'age', 'study')

    validate_position_info = validate_position_info
    validate = validate

    def create(self, validated_data):
        photo = validated_data.pop('photo')
        age = validated_data.pop('age', None)
        study = validated_data.pop('study', None)

        mole = super(MoleCreateSerializer, self).create(validated_data)

        MoleImage.objects.create(mole=mole, photo=photo, age=age, study=study)

        return mole


class MoleUpdateSerializer(MoleSerializer):
    validate_position_info = validate_position_info
    validate = validate

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_site',
                  'patient_anatomical_site', 'position_info', )

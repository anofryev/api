import json
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from apps.accounts.models import Coordinator
from apps.moles.serializers.study import StudyLiteSerializer

from ..models import MoleImage
from .utils import validate_study_consent_for_patient


class MoleImageSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=True)

    class Meta:
        model = MoleImage
        fields = ('pk', 'date_created', 'date_modified', 'path_diagnosis',
                  'clinical_diagnosis', 'prediction', 'prediction_accuracy',
                  'photo', 'biopsy', 'biopsy_data', 'approved', 'age', 'study')
        extra_kwargs = {
            'age': {
                'read_only': True,
            },
        }

    def validate_biopsy_data(self, biopsy_data):
        if isinstance(biopsy_data, str):
            return json.loads(biopsy_data)
        return biopsy_data

    def validate_approved(self, data):
        if data != self.instance.approved and \
                not Coordinator.objects.filter(
                    doctor_ptr_id=self.context['request'].user.id).exists():
            raise serializers.ValidationError(
                "Only coordinator can approve images")
        return data

    def validate_study(self, study):
        validate_study_consent_for_patient(
            study, self.context['view'].kwargs['patient_pk'])
        return study


class MoleImageListSerializer(MoleImageSerializer):
    study = StudyLiteSerializer()

    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'date_created', 'date_modified', 'path_diagnosis',
                  'clinical_diagnosis', 'prediction', 'prediction_accuracy',
                  'photo', 'biopsy', 'biopsy_data', 'approved', 'age', 'study')


class MoleImageCreateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'photo', 'age', 'study',)
        extra_kwargs = {
            'age': {
                'read_only': False,
            },
        }


class MoleImageUpdateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'path_diagnosis', 'clinical_diagnosis', 'biopsy',
                  'biopsy_data', 'approved', 'study',)

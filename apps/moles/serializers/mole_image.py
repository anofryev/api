from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from apps.accounts.models import Coordinator

from ..models import MoleImage


class MoleImageSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=True)

    class Meta:
        model = MoleImage
        fields = ('pk', 'date_created', 'date_modified', 'path_diagnosis',
                  'clinical_diagnosis', 'prediction', 'prediction_accuracy',
                  'photo', 'biopsy', 'biopsy_data', 'approved', )

    def validate_approved(self, data):
        if data != self.instance.approved \
           and not Coordinator.objects.filter(
               doctor_ptr_id=self.context['request'].user.id).exists():
            raise serializers.ValidationError(
                "Only coordinator can approve images")
        return data


class MoleImageCreateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'photo', )


class MoleImageUpdateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'path_diagnosis', 'clinical_diagnosis', 'biopsy',
                  'biopsy_data', 'approved')

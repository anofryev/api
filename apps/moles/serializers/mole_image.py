from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import MoleImage


class MoleImageSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=True)

    class Meta:
        model = MoleImage
        fields = ('pk', 'date_created', 'date_modified', 'path_diagnosis',
                  'clinical_diagnosis', 'prediction', 'prediction_accuracy',
                  'photo', 'biopsy', 'biopsy_data', )


class MoleImageCreateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('photo', )


class MoleImageUpdateSerializer(MoleImageSerializer):
    class Meta(MoleImageSerializer.Meta):
        fields = ('pk', 'path_diagnosis', 'clinical_diagnosis', 'biopsy',
                  'biopsy_data',  )

from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import MoleImage


class MoleImageSerializer(serializers.ModelSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)

    class Meta:
        model = MoleImage
        fields = ('pk', 'date_created', 'date_modified', 'path_diagnosis',
                  'clinical_diagnosis', 'prediction', 'prediction_accuracy',
                  'photo', 'biopsy', )

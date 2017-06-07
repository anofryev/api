from rest_framework import serializers

from ..models import Mole
from .anatomical_site import AnatomicalSiteSerializer
from .patient_anatomical_site import PatientAnatomicalSiteSerializer
from .mole_image import MoleImageSerializer


class MoleSerializer(serializers.ModelSerializer):
    anatomical_sites = AnatomicalSiteSerializer(many=True, read_only=True)

    class Meta:
        model = Mole


class MoleListSerializer(MoleSerializer):
    last_image = MoleImageSerializer(read_only=True)

    images_count = serializers.IntegerField(
        source='images.count', read_only=True)

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'last_image', 'images_count', )


class MoleDetailSerializer(MoleSerializer):
    patient_anatomical_site = PatientAnatomicalSiteSerializer(read_only=True)
    images = MoleImageSerializer(many=True, read_only=True)

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'patient_anatomical_site',
                  'position_x', 'position_y', 'images', )

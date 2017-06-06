from rest_framework import serializers

from ..models import Mole
from .patient_anatomical_site import PatientAnatomicalSiteSerializer
from .mole_image import MoleImageSerializer


class MoleSerializer(serializers.ModelSerializer):
    anatomical_sites = serializers.SerializerMethodField()
    patient_anatomical_site = PatientAnatomicalSiteSerializer()
    last_image = MoleImageSerializer()

    class Meta:
        model = Mole
        fields = ('pk', 'actual_image', 'anatomical_sites', 'position_x',
                  'position_y', )

    def get_anatomical_sites(self, obj):
        return list(obj.anatomical_site.get_ancestors()) + [obj.anatomical_site]

from rest_framework import serializers

from ..models import Mole
from .anatomical_site import AnatomicalSiteSerializer
from .patient_anatomical_site import PatientAnatomicalSiteSerializer
from .mole_image import MoleImageSerializer


class MoleSerializer(serializers.ModelSerializer):
    anatomical_sites = AnatomicalSiteSerializer(many=True)
    patient_anatomical_site = PatientAnatomicalSiteSerializer()
    last_image = MoleImageSerializer()

    class Meta:
        model = Mole
        fields = ('pk', 'anatomical_sites', 'patient_anatomical_site',
                  'position_x', 'position_y', 'last_image', )

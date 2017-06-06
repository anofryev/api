from rest_framework import serializers

from ..models import Mole
from .patient_anatomical_site import PatientAnatomicalSiteSerializer


class MoleSerializer(serializers.ModelSerializer):
    patient_anatomical_site = PatientAnatomicalSiteSerializer()

    class Meta:
        model = Mole
        fields = ('pk', 'anatomical_site', 'position_x', 'position_y', )

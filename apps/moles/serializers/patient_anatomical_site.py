from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import PatientAnatomicalSite


class PatientAnatomicalSiteSerializer(serializers.ModelSerializer):
    distant_photo = VersatileImageFieldSerializer(
        sizes='main_set', required=True)

    class Meta:
        model = PatientAnatomicalSite
        fields = ('pk', 'patient', 'anatomical_site', 'distant_photo', )
        extra_kwargs = {
            'patient': {
                'read_only': True,
            },
        }

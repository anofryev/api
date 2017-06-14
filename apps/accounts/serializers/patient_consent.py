from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import PatientConsent

class PatientConsentSerializer(serializers.ModelSerializer):
    signature = Base64ImageField(required=True)

    class Meta:
        model = PatientConsent
        fields = ('pk', 'date_created', 'date_expired', 'signature', )

        extra_kwargs = {
            'date_created': {
                'read_only': True,
            },
            'date_expired': {
                'read_only': True,
            },
        }

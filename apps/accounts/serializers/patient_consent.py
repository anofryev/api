from rest_framework import serializers

from ..models import PatientConsent


class PatientConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientConsent
        fields = ('pk', 'date_created', 'date_expired', 'signature', )

        extra_kwargs = {
            'signature': {
                'required': True,
            },
            'date_created': {
                'read_only': True,
            },
            'date_expired': {
                'read_only': True,
            },
        }

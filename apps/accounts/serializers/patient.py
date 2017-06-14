from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Patient
from .user import UserSerializer
from .patient_consent import PatientConsentSerializer


class PatientSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    valid_consent = PatientConsentSerializer(allow_null=True, read_only=True)

    # Fields from aggregation
    last_upload = serializers.DateTimeField(read_only=True)
    moles_images_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn', 'date_of_birth',
                  'sex', 'race', 'photo', 'last_upload',
                  'moles_images_count', 'valid_consent', )

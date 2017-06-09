from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Patient
from .user import UserSerializer


class PatientSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)

    # Fields from aggregation
    last_upload = serializers.DateTimeField(read_only=True)
    moles_images_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn', 'date_of_birth',
                  'sex', 'race', 'address', 'photo', 'last_upload',
                  'moles_images_count', )

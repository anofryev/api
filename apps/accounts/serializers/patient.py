from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Patient
from .user import UserSerializer


class PatientSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn', 'date_of_birth',
                  'sex', 'race', 'address', 'last_visit', 'photo', )

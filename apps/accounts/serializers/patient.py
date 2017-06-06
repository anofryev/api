from versatileimagefield.serializers import VersatileImageFieldSerializer

from apps.moles.serializers import MoleSerializer
from ..models import Patient
from .user import UserSerializer


class PatientSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    moles = MoleSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ('pk', 'first_name', 'last_name', 'mrn', 'date_of_birth',
                  'sex', 'race', 'address', 'last_visit', 'photo', 'moles',)

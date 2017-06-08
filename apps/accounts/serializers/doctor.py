from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Doctor
from .user import UserSerializer


class DoctorSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email', 'degree',
                  'department', 'photo', 'units_of_length', )

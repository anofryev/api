from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Doctor
from .user import UserSerializer


class DoctorSerializer(UserSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    coordinator_public_key = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email', 'degree',
                  'department', 'photo', 'units_of_length', 'password',
                  'can_see_prediction',
                  'public_key', 'private_key', 'coordinator_public_key', )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
            },
            'private_key': {
                'allow_blank': True,
            },
        }

    def get_coordinator_public_key(self, doctor):
        if doctor.my_coordinator_id:
            return Doctor.objects.filter(
                id=doctor.my_coordinator_id).values_list(
                    'public_key', flat=True).first()
        return None

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super(DoctorSerializer, self).update(instance, validated_data)

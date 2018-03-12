from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Doctor, Coordinator, SiteJoinRequest, Site
from .user import UserSerializer


class RegisterDoctorSerializer(UserSerializer):
    site = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.all(),
        required=False,
        allow_null=True,
        write_only=True)

    def create(self, validated_data):
        site = validated_data.pop('site', None)
        password = validated_data.pop('password')
        doctor = super(RegisterDoctorSerializer,
                       self).create(validated_data)
        doctor.is_active = False
        doctor.set_password(password)
        doctor.save()
        if site:
            SiteJoinRequest.objects.create(
                doctor=doctor, site=site)
        return doctor

    class Meta:
        model = Doctor
        fields = ('pk', 'date_created', 'first_name', 'last_name',
                  'email', 'password', 'site', )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }


class DoctorLiteSerializer(UserSerializer):
    is_coordinator = serializers.SerializerMethodField()

    def get_is_coordinator(self, doctor):
        return Coordinator.objects.filter(doctor_ptr=doctor).exists()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email',
                  'degree', 'department', 'photo', 'units_of_length',
                  'is_coordinator', 'date_created',)


class DoctorSerializer(DoctorLiteSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    coordinator_public_key = serializers.SerializerMethodField()
    my_doctors_public_keys = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email', 'password',
                  'degree', 'department', 'photo', 'units_of_length',
                  'can_see_prediction',
                  'public_key', 'private_key', 'coordinator_public_key',
                  'my_coordinator_id', 'my_doctors_public_keys',
                  'is_coordinator', 'date_created',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
            },
            'private_key': {
                'allow_blank': True,
            },
            'date_created': {
                'read_only': True,
            },
        }

    def get_my_doctors_public_keys(self, doctor):
        coordinator = Coordinator.objects.filter(doctor_ptr=doctor).first()
        if coordinator:
            return {d['id']: d['public_key'] for d in
                    coordinator.doctors.values('id', 'public_key')}
        return None

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

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from apps.accounts.models import DoctorToPatient
from apps.accounts.models.participant import get_participant_patient, \
    is_participant
from ..models import Doctor, Coordinator, Participant, SiteJoinRequest, Site
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


class DoctorSerializer(UserSerializer):
    is_coordinator = serializers.SerializerMethodField()
    is_participant = serializers.SerializerMethodField()

    def get_is_coordinator(self, doctor):
        return Coordinator.objects.filter(doctor_ptr=doctor).exists()

    def get_is_participant(self, doctor):
        return Participant.objects.filter(doctor_ptr=doctor).exists()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email',
                  'degree', 'department', 'photo', 'units_of_length',
                  'is_coordinator', 'is_participant', 'date_created',)


class DoctorWithSitesSerializer(DoctorSerializer):
    sites = serializers.ListField()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email', 'sites',
                  'degree', 'department', 'photo', 'units_of_length',
                  'is_coordinator', 'is_participant', 'date_created',)


class DoctorWithKeysSerializer(DoctorSerializer):
    coordinator_public_key = serializers.SerializerMethodField()

    def get_coordinator_public_key(self, doctor):
        if doctor.my_coordinator_id:
            return Doctor.objects.filter(
                id=doctor.my_coordinator_id).values_list(
                    'public_key', flat=True).first()
        return None

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email',
                  'degree', 'department', 'photo', 'units_of_length',
                  'is_coordinator', 'is_participant', 'date_created',
                  'public_key', 'coordinator_public_key')


class DoctorFullSerializer(DoctorWithKeysSerializer):
    photo = VersatileImageFieldSerializer(sizes='main_set', required=False)
    my_doctors_public_keys = serializers.SerializerMethodField()
    coordinator_of_site = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ('pk', 'first_name', 'last_name', 'email', 'password',
                  'degree', 'department', 'photo', 'units_of_length',
                  'can_see_prediction', 'coordinator_of_site',
                  'public_key', 'private_key', 'coordinator_public_key',
                  'my_coordinator_id', 'my_doctors_public_keys',
                  'is_coordinator', 'is_participant', 'date_created',)
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

        if is_participant(doctor):
            patient = get_participant_patient(doctor)
            if patient:
                return {d['id']: d['public_key'] for d in
                        Doctor.objects.filter(
                            pk__in=DoctorToPatient.objects.filter(
                                patient=patient
                            ).values_list('doctor_id', flat=True)
                        ).values('id', 'public_key')}

        return None

    def get_coordinator_of_site(self, doctor):
        result = Site.objects.filter(
            site_coordinator__doctor_ptr=doctor).first()
        return result.pk if result else None

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super(DoctorFullSerializer, self).update(instance, validated_data)

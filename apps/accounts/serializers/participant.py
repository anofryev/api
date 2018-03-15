from apps.accounts.serializers import UserSerializer
from ..models import Doctor, Participant


class RegisterParticipantSerializer(UserSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        doctor = super(RegisterParticipantSerializer,
                       self).create(validated_data)
        doctor.is_active = False
        doctor.set_password(password)
        doctor.save()

        Participant.objects.create(doctor_ptr=doctor)

        return doctor

    class Meta:
        model = Doctor
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

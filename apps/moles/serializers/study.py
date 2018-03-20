from rest_framework import serializers

from apps.accounts.models import Doctor
from apps.accounts.serializers import DoctorSerializer
from ..models import ConsentDoc, Study


class ConsentDocSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = ConsentDoc
        fields = ('pk', 'file', 'thumbnail', 'original_filename')


class StudyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ('pk', 'title', 'consent_docs')


class StudyListSerializer(serializers.ModelSerializer):
    consent_docs = ConsentDocSerializer(many=True)
    doctors = DoctorSerializer(many=True)

    class Meta(StudyBaseSerializer.Meta):
        fields = ('pk', 'title', 'doctors', 'patients', 'consent_docs')


class AddDoctorSerializer(serializers.Serializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_pk = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        required=True)
    emails = serializers.ListField(
        child=serializers.EmailField())

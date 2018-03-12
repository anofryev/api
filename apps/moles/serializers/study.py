from rest_framework import serializers

from apps.accounts.serializers import PatientSerializer, DoctorLiteSerializer
from ..models import ConsentDoc, Study, StudyToPatient


class ConsentDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentDoc
        fields = '__all__'


class StudyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'


class StudySerializer(StudyBaseSerializer):
    def create(self, validated_data):
        instance = super(StudySerializer, self).create(validated_data)
        self.update_relations(instance)
        return instance

    def update(self, instance, validated_data):
        instance = super(StudySerializer, self).update(instance, validated_data)
        self.update_relations(instance)
        return instance

    def update_relations(self, study):
        for patient_pk in self.initial_data.get('patients', []):
            StudyToPatient.objects.update_or_create(
                study=study,
                patient_id=patient_pk
            )

    class Meta(StudyBaseSerializer.Meta):
        pass


class StudyListSerializer(serializers.ModelSerializer):
    patients = PatientSerializer(many=True)
    doctors = DoctorLiteSerializer(many=True)

    class Meta(StudyBaseSerializer.Meta):
        pass

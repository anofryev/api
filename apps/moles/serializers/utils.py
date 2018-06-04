from rest_framework import serializers

from apps.moles.models import StudyToPatient


def validate_study_consent_for_patient(study, patient):
    if study:
        study_to_patient = StudyToPatient.objects.filter(
            study=study,
            patient=patient
        ).first()
        if study_to_patient:
            consent = study_to_patient.patient_consent
            if consent and not consent.is_valid():
                raise serializers.ValidationError(
                    "Need to update study consent for patient")

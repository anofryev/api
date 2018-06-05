from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from rest_framework import serializers

from apps.accounts.factories import PatientFactory, PatientConsentFactory
from apps.moles.factories.study import StudyFactory
from apps.moles.models import StudyToPatient

from ..models.utils import validate_study_consent_for_patient


class UtilsTest(TestCase):
    def test_validate_study_consent(self):
        study = StudyFactory.create()
        patient = PatientFactory.create()
        expired = timezone.now() - timedelta(days=1)
        consent = PatientConsentFactory.create(
            patient=patient,
            date_expired=expired)
        consent.date_expired = expired
        consent.save()

        StudyToPatient.objects.create(
            study=study,
            patient=patient,
            patient_consent=consent)

        with self.assertRaises(serializers.ValidationError):
            validate_study_consent_for_patient(study, patient)

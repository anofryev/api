from django.db import models

from apps.moles.models.upload_paths import study_consent_docs_path


class Study(models.Model):
    title = models.CharField(
        max_length=120
    )
    doctors = models.ManyToManyField(
        'accounts.Doctor',
        blank=True,
        related_name='studies',
    )
    patients = models.ManyToManyField(
        'accounts.Patient',
        blank=True,
        related_name='studies',
        through='StudyToPatient'
    )
    consent_forms = models.ManyToManyField(
        'ConsentDoc',
        blank=True,
        related_name='studies',
    )

    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'


class ConsentDoc(models.Model):
    title = models.CharField(
        max_length=240
    )
    pdf = models.FileField(
        verbose_name='PDF file',
        upload_to=study_consent_docs_path,
    )

    class Meta:
        verbose_name = 'Consent doc'
        verbose_name_plural = 'Consent docs'


class StudyToPatient(models.Model):
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        verbose_name='Study'
    )
    patient = models.ForeignKey(
        'accounts.Patient',
        on_delete=models.CASCADE,
        verbose_name='Patient'
    )
    patient_consent = models.ForeignKey(
        'accounts.PatientConsent'
    )

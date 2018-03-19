from django.db import models

from apps.main.models.mixins.thumbnail import ThumbnailMixin
from apps.main.storages import private_storage
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
    consent_docs = models.ManyToManyField(
        'ConsentDoc',
        blank=True,
        related_name='studies',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'


class ConsentDoc(models.Model, ThumbnailMixin):
    ATTACHMENT_FIELD_NAME = 'file'

    file = models.FileField(
        verbose_name='Document file',
        upload_to=study_consent_docs_path,
        storage=private_storage,
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
        'accounts.PatientConsent',
        blank=True, null=True
    )

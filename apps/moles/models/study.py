from django.db import models
from django.utils import timezone

from apps.accounts.models import Coordinator
from apps.main.models.mixins.thumbnail import ThumbnailMixin
from apps.main.storages import private_storage
from apps.moles.models.upload_paths import study_consent_docs_path


class Study(models.Model):
    author = models.ForeignKey(
        Coordinator,
        related_name='studies',
        blank=True, null=True)
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

    def _invalidate_consents(self):
        for study_to_patient in StudyToPatient.objects.filter(study=self):
            if study_to_patient.patient_consent:
                study_to_patient.patient_consent.date_expired = timezone.now()
                study_to_patient.patient_consent.save()

    def _check_update_consents(self, previous_docs):
        current_docs = self.consent_docs.all().values_list(
            'pk', flat=True)
        if set(previous_docs) != set(current_docs):
            self._invalidate_consents()

    def save(self, *args, **kwargs):
        previous_docs = self.consent_docs.all().values_list('pk', flat=True)
        super(Study, self).save(*args, **kwargs)
        if previous_docs:
            self._check_update_consents(previous_docs)

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
    original_filename = models.CharField(
        max_length=250,
        blank=True, null=True)

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

    def __str__(self):
        return '%s - %s' % (self.study, self.patient)

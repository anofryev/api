from datetime import timedelta

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from constance import config

from apps.main.storages import private_storage
from apps.main.models.mixins import DelayedSaveFilesMixin
from .patient import Patient
from .upload_paths import patient_consent_signature_path


class PatientConsentQuerySet(models.QuerySet):
    def valid(self):
        return self.filter(date_expired__gt=timezone.now())


class PatientConsent(DelayedSaveFilesMixin, models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created on'
    )
    date_expired = models.DateTimeField(
        blank=True,
        verbose_name='Valid until'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consents',
        verbose_name='Patient'
    )
    signature = models.ImageField(
        upload_to=patient_consent_signature_path,
        storage=private_storage,
        null=True,
        blank=True,
        verbose_name='Signature'
    )

    objects = PatientConsentQuerySet.as_manager()

    class Meta:
        verbose_name = 'Patient consent'
        verbose_name_plural = 'Patient consents'
        ordering = ('-date_expired', )

    def __str__(self):
        return '{0}: {1}'.format(self.patient, self.date_expired)


@receiver(pre_save, sender=PatientConsent)
def set_up_date_expired(sender, instance, **kwargs):
    if not instance.pk:
        instance.date_expired = timezone.now() + timedelta(
            days=config.CONSENT_VALID_DAYS)

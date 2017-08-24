from django.db import models
from django.db.models import Count, Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField

from skiniq.utils import get_timestamp
from apps.main.storages import private_storage
from apps.main.models.mixins import DelayedSaveFilesMixin
from .user import User
from .doctor import Doctor
from .upload_paths import patient_photo_path
from .enums import SexEnum, RaceEnum


class PatientQuerySet(DelayedSaveFilesMixin, models.QuerySet):
    def annotate_moles_images_count(self):
        return self.annotate(
            moles_images_count=Count('moles__images'))

    def annotate_last_upload(self):
        return self.annotate(
            last_upload=Max('moles__images__date_created'))


class Patient(models.Model):
    first_name = models.TextField(
        verbose_name='Encrypted first name'
    )
    last_name = models.TextField(
        verbose_name='Encrypted last name'
    )
    date_of_birth = models.TextField(
        verbose_name='Encrypted date of birth',
        blank=True, null=True
    )
    mrn = models.TextField(
        null=True,
        blank=True,
        verbose_name='Encrypted Medical Record Number'
    )
    mrn_hash = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Hash of Medical Record Number'
    )
    photo = VersatileImageField(
        verbose_name='Profile Picture',
        upload_to=patient_photo_path,
        storage=private_storage,
        max_length=300,
        null=True,
        blank=True
    )
    sex = models.CharField(
        max_length=1,
        choices=SexEnum.CHOICES,
        verbose_name='Sex',
        blank=True, null=True
    )
    race = models.SmallIntegerField(
        choices=RaceEnum.CHOICES,
        verbose_name='Race',
        blank=True, null=True
    )
    doctors = models.ManyToManyField(
        Doctor,
        related_name="patients",
        through='DoctorToPatient'
    )
    objects = PatientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    @property
    def valid_consent(self):
        return self.consents.valid().first()

    def __str__(self):
        return "Patient: {0} ({1},{2})".format(
            self.pk,
            self.get_race_display(),
            self.get_sex_display())


class DoctorToPatient(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name='Patient'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name='Doctor'
    )

    encrypted_key = models.TextField(
        verbose_name='Encrypted key for patient data',
    )

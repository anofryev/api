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


class Patient(User):
    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='patient_role'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patients',
        verbose_name='Doctor'
    )
    photo = VersatileImageField(
        verbose_name='Profile Picture',
        upload_to=patient_photo_path,
        storage=private_storage,
        max_length=300,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(
        verbose_name='Date of birth',
        blank=True, null=True
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
    mrn = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Medical Record Number'
    )

    objects = PatientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ('last_name', 'first_name', )

    def has_valid_consent(self):
        return self.consents.filter(date_expired__gt=timezone.now()).exists()


@receiver(pre_save, sender=Patient)
def set_up_username(sender, instance, *args, **kwargs):
    if instance.mrn:
        instance.username = str(instance.mrn)
    else:
        instance.username = slugify('{0}_{1}_{2}'.format(
            instance.first_name, instance.last_name, get_timestamp()))

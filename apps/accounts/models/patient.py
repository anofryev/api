from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField

from skiniq.utils import get_timestamp
from .user import User
from .doctor import Doctor
from .upload_paths import patient_photo_path


class SexEnum(object):
    MALE = 'm'
    FEMALE = 'f'

    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )


class RaceEnum(object):
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = 1
    ASIAN = 2
    BLACK_OR_AFRICAN_AMERICAN = 3
    HISPANIC_OR_LATINO = 4
    NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER = 5
    WHITE = 6

    CHOICES = (
        (
            AMERICAN_INDIAN_OR_ALASKA_NATIVE,
            'American Indian/Alaska Native'
        ),
        (
            ASIAN,
            'Asian'
        ),
        (
            BLACK_OR_AFRICAN_AMERICAN,
            'Black/African American'
        ),
        (
            HISPANIC_OR_LATINO, 'Hispanic/Latino'
        ),
        (
            NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            'Native Hawaiian/Pacific Islander'
        ),
        (
            WHITE,
            'White'
        ),
    )


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
        default='tmp/images/default_profile.jpeg',
        max_length=300,
        null=True,
        blank=True)
    date_of_birth = models.DateField(
        verbose_name='Date of birth'
    )
    sex = models.CharField(
        max_length=1,
        choices=SexEnum.CHOICES,
        verbose_name='Sex'
    )
    race = models.SmallIntegerField(
        choices=RaceEnum.CHOICES,
        verbose_name='Race'
    )
    mrn = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Medical Record Number'
    )
    address = models.TextField(
        verbose_name='Address'
    )

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


@receiver(pre_save, sender=Patient)
def set_up(sender, instance, *args, **kwargs):
    if instance.mrn:
        instance.username = str(instance.mrn)
    else:
        instance.username = slugify('{0}_{1}_{2}'.format(
            instance.first_name, instance.last_name, get_timestamp()))

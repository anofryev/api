from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField

from apps.main.storages import public_storage
from apps.main.models.mixins import DelayedSaveFilesMixin
from .user import User
from .upload_paths import doctor_photo_path
from .enums import UnitsOfLengthEnum


class Doctor(DelayedSaveFilesMixin, User):
    user_ptr = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='doctor_role'
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='Email address',
    )
    photo = VersatileImageField(
        verbose_name='Profile Picture',
        upload_to=doctor_photo_path,
        storage=public_storage,
        max_length=300,
        null=True,
        blank=True
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Department'
    )
    degree = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Doctoral degree',
    )
    units_of_length = models.CharField(
        max_length=2,
        choices=UnitsOfLengthEnum.CHOICES,
        default=UnitsOfLengthEnum.INCH,
        verbose_name='Units of length'
    )
    can_see_prediction = models.BooleanField(
        default=False,
    )
    public_key = models.TextField(
        default=''
    )
    private_key = models.TextField(
        default=''
    )
    my_coordinator = models.ForeignKey(
        'accounts.Coordinator',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='doctors'
    )
    approved_by_coordinator = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


@receiver(pre_save, sender=Doctor)
def set_up_username(sender, instance, *args, **kwargs):
    instance.username = instance.email

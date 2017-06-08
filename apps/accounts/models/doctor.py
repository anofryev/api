from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from storages.backends.s3boto import S3BotoStorage
from versatileimagefield.fields import VersatileImageField

from .user import User
from .upload_paths import doctor_photo_path


class Doctor(User):
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
        # storage=S3BotoStorage(
        #     bucket='skin-api-dev-public', querystring_auth=False),
        max_length=300,
        null=True,
        blank=True
    )
    department = models.CharField(
        max_length=100,
        verbose_name='Department'
    )
    degree = models.CharField(
        max_length=20,
        verbose_name='Doctoral degree',
    )

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


@receiver(pre_save, sender=Doctor)
def set_up(sender, instance, *args, **kwargs):
    instance.username = instance.email

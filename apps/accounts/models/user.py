from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.db import models
from storages.backends.s3boto import S3BotoStorage
from versatileimagefield.fields import VersatileImageField

from .upload_paths import photo_filepath


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')
        # Ensure that first and last names are set
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='email address',)
    first_name = models.CharField(
        max_length=100)
    last_name = models.CharField(
        max_length=100)
    photo = VersatileImageField(
        verbose_name='Profile Picture',
        upload_to=photo_filepath,
        storage=S3BotoStorage(
            bucket='skin-api-dev-public', querystring_auth=False),
        default='tmp/images/default_profile.jpeg',
        max_length=300,
        blank=True)
    is_staff = models.BooleanField(
        'Staff status',
        default=False,
    )
    is_active = models.BooleanField(
        'Active',
        default=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

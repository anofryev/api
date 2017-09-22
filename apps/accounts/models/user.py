from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        # Ensure that an username is set
        if not username:
            raise ValueError('Users must have an username')
        # Ensure that first and last names are set
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username, first_name, last_name, password)
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

    username = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name='Username'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='First name'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Last name'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Staff status'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    last_active = models.DateTimeField(
        verbose_name='Last active',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    @property
    def doctor_role__email(self):
        return self.doctor_role.email

    @staticmethod
    def get_email_field_name():
        return 'doctor_role__email'

from django.db.models.signals import post_save
from django.dispatch import receiver
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from .models import MoleImage, PatientAnatomicalSite


@receiver(post_save, sender=MoleImage)
def warm_mole_image_photo(sender, instance, **kwargs):
    """Prepare photos"""
    VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='main_set',
        image_attr='photo').warm()


@receiver(post_save, sender=PatientAnatomicalSite)
def warm_patient_anatomical_site_distant_photo(sender, instance, **kwargs):
    """Prepare photos"""
    VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='main_set',
        image_attr='distant_photo').warm()

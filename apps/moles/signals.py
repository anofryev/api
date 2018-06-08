from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from .models import MoleImage, PatientAnatomicalSite, Study


@receiver(post_save, sender=MoleImage)
def warm_mole_image_photo(sender, instance, **kwargs):
    """Prepare photos"""
    if instance.photo:
        VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='main_set',
            image_attr='photo').warm()


@receiver(post_save, sender=PatientAnatomicalSite)
def warm_patient_anatomical_site_distant_photo(sender, instance, **kwargs):
    """Prepare photos"""
    if instance.distant_photo:
        VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='main_set',
            image_attr='distant_photo').warm()


def consent_docs_changes(sender, instance, action, **kwargs):
    if action == 'post_add':
        instance.invalidate_consents()


m2m_changed.connect(consent_docs_changes, sender=Study.consent_docs.through)

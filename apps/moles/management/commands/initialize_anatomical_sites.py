from django.core.management import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from ...models import AnatomicalSite


ANATOMICAL_SITES = (
    ('Head', (
        'Occipital scalp',
        ('Face', (
            'Right cheek',
            'Left cheek',
            'Chin',
            ('Right ear', (
                'Right ear helix',
                'Right earlobe',
            )),
            ('Left ear', (
                'Left ear helix',
                'Left earlobe',
            )),
            ('Right eye', (
                'Right eyelashes',
            )),
            ('Left eye', (
                'Left eyelashes',
            )),
            'Right eyebrow',
            'Left eyebrow',
            'Forehead',
            'Hair',
            'Right jaw',
            'Left jaw',
            ('Mouth', (
                'Lower lip',
                'Upper lip',
            )),
            ('Nose', (
                'Right nostril',
                'Left nostril',
            )),
            'Right temple',
            'Left temple',
        )),
    )),
    ('Arms', (
        ('Right arm', (
            'Right anterior shoulder',
            'Right anterior upper arm',
            'Right antecubital fossa',
            'Right anterior forearm',
            'Right palm',
            'Right posterior shoulder',
            'Right posterior upper arm',
            'Right elbow',
            'Right posterior forearm',
            'Right dorsal hand',
        )),
        ('Left arm', (
            'Left anterior shoulder',
            'Left anterior upper arm',
            'Left antecubital fossa',
            'Left anterior forearm',
            'Left palm',
            'Left posterior shoulder',
            'Left posterior upper arm',
            'Left elbow',
            'Left posterior forearm',
            'Left dorsal hand',
        )),
    )),
    ('Trunk', (
        'Anterior neck',
        'Posterior neck',
        'Middle chest',
        'Right upper chest',
        'Left upper chest',
        'Right upper abdomen',
        'Right lower abdomen',
        'Left upper abdomen',
        'Left lower abdomen',
        'Right upper back',
        'Right lower back',
        'Left upper back',
        'Left lower back',
        'Right buttock',
        'Left buttock',
    )),
    ('Legs', (
        ('Right leg', (
            'Right posterior thigh',
            'Right popliteal fossa',
            'Right proximal calf',
            'Right distal calf',
            'Right heel',
            'Right anterior thigh',
            'Right knee',
            'Right proximal lower leg',
            'Right distal lower leg',
            'Right dorsal foot',
        )),
        ('Left leg', (
            'Left posterior thigh',
            'Left popliteal fossa',
            'Left proximal calf',
            'Left distal calf',
            'Left heel',
            'Left anterior thigh',
            'Left knee',
            'Left proximal lower leg',
            'Left distal lower leg',
            'Left dorsal foot',
        ))
    ))
)


def initialize_anatomical_sites(parent, item):
    if isinstance(item, tuple):
        name, children = item
    else:
        name = item
        children = []

    slug = slugify(name)

    try:
        anatomical_site = AnatomicalSite.objects.get(slug=slug)
        anatomical_site.move_to(parent, 'last-child')
    except:
        anatomical_site = AnatomicalSite.objects.create(
            slug=slug, name=name, parent=parent)

    result = [anatomical_site]

    for child in children:
        result.extend(initialize_anatomical_sites(anatomical_site, child))

    return result


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, **options):
        initialized_anatomical_sites = []
        for item in ANATOMICAL_SITES:
            initialized_anatomical_sites.extend(
                initialize_anatomical_sites(None, item))

        # Remove old anatomical sites but save existing patient anatomical sites
        old_anatomical_sites = AnatomicalSite.objects.exclude(
            slug__in=[
                anatomical_site.slug
                for anatomical_site in initialized_anatomical_sites
            ]
        ).order_by('-level')

        for anatomical_site in old_anatomical_sites:
            anatomical_site.patientanatomicalsite_set.update(
                anatomical_site=anatomical_site.parent)

        old_anatomical_sites.delete()

from django.core.management import BaseCommand

from ...models import AnatomicalSite


ANATOMICAL_SITES = (
    ('Head', (
        'Face',
        'Occipital scalp',
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
            'Right dorsal hand'
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
            'Left dorsal hand'
        )),
    )),
    ('Neck', (
        'Anterior neck and middle chest',
        'Posterior neck',
    )),
    ('Chest', (
        'Right upper chest',
        'Left upper chest',
    )),
    ('Abdomen', (
        'Right upper abdomen',
        'Right lower abdomen',
        'Left upper abdomen',
        'Left lower abdomen',
    )),
    ('Back', (
        'Right upper back',
        'Right lower back',
        'Left upper back',
        'Left lower back',
    )),
    ('Legs', (
        ('Right leg', (
            'Right buttock',
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
            'Left buttock',
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


def create_anatomical_sites(parent, item):
    if isinstance(item, tuple):
        name, children = item
    else:
        name = item
        children = []

    anatomical_site, _ = AnatomicalSite.objects.get_or_create(
        parent=parent, name=name)

    for child in children:
        create_anatomical_sites(anatomical_site, child)


class Command(BaseCommand):
     def handle(self, **options):
         for item in ANATOMICAL_SITES:
             create_anatomical_sites(None, item)

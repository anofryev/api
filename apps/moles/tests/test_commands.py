from django.core.management import call_command
from django.test import TestCase

from ..models import AnatomicalSite
from ..management.commands.initialize_anatomical_sites import ANATOMICAL_SITES


class CommandsTest(TestCase):
    def test_initialize_anatomical_sites(self):
        call_command('initialize_anatomical_sites')

        self.assertTrue(AnatomicalSite.objects.exists())
        for name, children in ANATOMICAL_SITES:
            asite = AnatomicalSite.objects.get(name=name)
            self.assertEqual(asite.children.count(), len(children))

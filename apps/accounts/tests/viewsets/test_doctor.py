import json
from apps.main.tests import APITestCase

from ...factories import PatientFactory, DoctorFactory
from ...models import Patient, RaceEnum, SexEnum, DoctorToPatient


class DoctorViewSetTest(APITestCase):
    def setUp(self):
        super(DoctorViewSetTest, self).setUp()

    def test_this(self):
        pass
        # TODO test me!

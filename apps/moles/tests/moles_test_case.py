from apps.main.tests import APITestCase
from apps.accounts.factories import PatientFactory
from ..factories import (
    PatientAnatomicalSiteFactory, AnatomicalSiteFactory, MoleFactory)


class MolesTestCase(APITestCase):
    def setUp(self):
        super(MolesTestCase, self).setUp()

        self.first_patient = PatientFactory.create(doctor=self.doctor)
        self.another_patient = PatientFactory()

        self.anatomical_site = AnatomicalSiteFactory.create()

        self.first_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.first_patient,
            anatomical_site=self.anatomical_site)
        self.another_patient_asite = PatientAnatomicalSiteFactory.create(
            patient=self.another_patient,
            anatomical_site=self.anatomical_site)

        self.first_patient_mole = MoleFactory.create(
            patient=self.first_patient,
            anatomical_site=self.anatomical_site)

        self.another_patient_mole = MoleFactory.create(
            patient=self.another_patient,
            anatomical_site=self.anatomical_site)

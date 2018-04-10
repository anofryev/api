from apps.accounts.factories import DoctorFactory, CoordinatorFactory, \
    SiteFactory
from apps.accounts.models import SiteJoinRequest, JoinStateEnum
from apps.main.tests import APITestCase


class DoctorViewSetTest(APITestCase):
    def setUp(self):
        super(DoctorViewSetTest, self).setUp()
        self.other_doctor = DoctorFactory.create()
        self.coordinator = DoctorFactory.create()
        self.coordinator_ptr = CoordinatorFactory.create(
            doctor_ptr=self.coordinator)

    def test_forbidden_unauthorized(self):
        resp = self.client.get('/api/v1/doctor/')
        self.assertForbidden(resp)

    def test_forbidden_doctor(self):
        self.authenticate_as_doctor()
        resp = self.client.get('/api/v1/doctor/')
        self.assertForbidden(resp)

    def test_list_coordinator(self):
        self.authenticate_as_doctor(self.coordinator)
        resp = self.client.get('/api/v1/doctor/')
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 2)
        self.assertSetEqual(
            set([item['pk'] for item in resp.data]),
            {self.doctor.pk, self.other_doctor.pk}
        )

    def test_list_with_sites(self):
        site = SiteFactory.create(site_coordinator=self.coordinator_ptr)
        SiteJoinRequest.objects.create(
            doctor=self.other_doctor,
            site=site)
        SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=site,
            state=JoinStateEnum.CONFIRMED)
        self.authenticate_as_doctor(self.coordinator)
        resp = self.client.get('/api/v1/doctor/')
        self.assertSuccessResponse(resp)

        for doctor in resp.data:
            if doctor['pk'] == self.other_doctor.pk:
                self.assertListEqual(doctor['sites'], [])

            if doctor['pk'] == self.doctor.pk:
                self.assertListEqual(doctor['sites'], [site.pk])

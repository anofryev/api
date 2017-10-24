import random

from apps.main.tests import APITestCase

from ...factories import SiteFactory, DoctorFactory, PatientFactory
from ...models import (
    User, Coordinator, Doctor, SiteJoinRequest,
    SiteJoinRequest, JoinStateEnum, )


class SiteJoinRequestTest(APITestCase):
    def setUp(self):
        super(SiteJoinRequestTest, self).setUp()
        self.coordinator = Coordinator.objects.create(
            doctor_ptr=DoctorFactory.create(password='password'))
        self.site = SiteFactory.create(site_coordinator=self.coordinator)

    def test_that_doctor_can_send_join_request(self):
        data = {
            'site': self.site.id,
        }
        self.authenticate_as_doctor()
        resp = self.client.post('/api/v1/site_join_requests/', data)
        self.assertSuccessResponse(resp)
        self.assertTrue(
            SiteJoinRequest.objects.filter(
                state=JoinStateEnum.NEW,
                doctor=self.doctor,
                site=self.site).exists())

    def test_that_doctor_cant_send_request_twise(self):
        data = {
            'site': self.site.id,
        }
        self.authenticate_as_doctor()
        resp = self.client.post('/api/v1/site_join_requests/', data)
        self.assertSuccessResponse(resp)
        resp = self.client.post('/api/v1/site_join_requests/', data)
        self.assertBadRequest(resp)

    def test_that_coordinator_can_approve(self):
        PatientFactory.create(doctor=self.doctor)
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site)

        self.authenticate_as_doctor(
            self.coordinator.doctor_ptr)

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/approve/'.format(jr.id))
        self.assertSuccessResponse(resp)
        jr.refresh_from_db()
        self.assertEqual(jr.state, JoinStateEnum.APPROVED)

    def test_that_doctor_without_patients_get_confirmed_state(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site)

        self.authenticate_as_doctor(
            self.coordinator.doctor_ptr)

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/approve/'.format(jr.id))
        self.assertSuccessResponse(resp)
        jr.refresh_from_db()
        self.assertEqual(jr.state, JoinStateEnum.CONFIRMED)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.my_coordinator_id,
                         jr.site.site_coordinator_id)


    def test_that_coordinator_can_reject(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site)

        self.authenticate_as_doctor(
            self.coordinator.doctor_ptr)

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/reject/'.format(jr.id))
        self.assertSuccessResponse(resp)
        jr.refresh_from_db()
        self.assertEqual(jr.state, JoinStateEnum.REJECTED)

    def test_doctor_cant_approve_herself(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site)

        self.authenticate_as_doctor()

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/approve/'.format(jr.id))
        self.assertBadRequest(resp)

    def test_doctor_cant_reject_herself(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site)

        self.authenticate_as_doctor()

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/reject/'.format(jr.id))
        self.assertBadRequest(resp)

    def test_doctor_without_patinets_can_confirm_joining(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site,
            state=JoinStateEnum.APPROVED)

        self.authenticate_as_doctor()

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/confirm/'.format(jr.id),
            {'encrypted_keys': {}},
            format='json')
        self.assertSuccessResponse(resp)
        jr.refresh_from_db()
        self.assertEqual(jr.state, JoinStateEnum.CONFIRMED)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.my_coordinator_id,
                         jr.site.site_coordinator_id)


    def test_doctor_with_patinets_can_confirm_joining(self):
        for _index in range(random.randint(1, 10)):
            PatientFactory.create(doctor=self.doctor)

        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site,
            state=JoinStateEnum.APPROVED)

        self.authenticate_as_doctor()

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/confirm/'.format(jr.id),
            {'encrypted_keys': {p.id: 'key' for p in
                                self.doctor.patients.all()}},
            format='json')
        self.assertSuccessResponse(resp)
        jr.refresh_from_db()
        self.assertEqual(jr.state, JoinStateEnum.CONFIRMED)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.my_coordinator_id,
                         jr.site.site_coordinator_id)

    def test_doctor_with_patinets_cant_confirm_joining_if_dont_provide_enought_keys(self):
        for _index in range(random.randint(1, 10)):
            PatientFactory.create(doctor=self.doctor)

        patient_to_exclude = PatientFactory.create(doctor=self.doctor)

        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site,
            state=JoinStateEnum.APPROVED)

        self.authenticate_as_doctor()

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/confirm/'.format(jr.id),
            {'encrypted_keys': {p.id: 'key' for p in
                                self.doctor.patients.all()
                                if p != patient_to_exclude}},
            format='json')
        self.assertBadRequest(resp)

    def test_coordinator_cant_confirm_joining(self):
        jr = SiteJoinRequest.objects.create(
            doctor=self.doctor,
            site=self.site,
            state=JoinStateEnum.APPROVED)

        self.authenticate_as_doctor(
            self.coordinator.doctor_ptr)

        resp = self.client.post(
            '/api/v1/site_join_requests/{0}/confirm/'.format(jr.id),
            {'encrypted_keys': {}},
            format='json')
        self.assertBadRequest(resp)

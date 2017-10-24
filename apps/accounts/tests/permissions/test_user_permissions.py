from django.test import TestCase, mock
from apps.accounts.permissions import (IsCoordinator, IsDoctor,
                                       IsDoctorOfPatient)
from ...factories import (DoctorFactory, CoordinatorFactory, UserFactory,
                          PatientFactory)


class FakeRequest:
    def __init__(self, user):
        self.user = user


class FakeView:
    def __init__(self, kwargs=None):
        self.kwargs = kwargs


view = FakeView()


class UserPermissionTestCase(TestCase):
    def setUp(self):
        self.doctor = DoctorFactory.create()
        self.userRequest = FakeRequest(UserFactory.create())
        self.doctorRequest = FakeRequest(self.doctor.user_ptr)
        self.coordinatorRequest = FakeRequest(CoordinatorFactory.create()
                                              .doctor_ptr.user_ptr)

    def test_is_doctor(self):
        permission = IsDoctor()
        self.assertFalse(permission.has_permission(self.userRequest, view))
        self.assertTrue(permission.has_permission(self.doctorRequest, view))
        self.assertTrue(
            permission.has_permission(self.coordinatorRequest, view))

    def test_is_coordinator(self):
        permission = IsCoordinator()
        self.assertFalse(permission.has_permission(self.userRequest, view))
        self.assertFalse(permission.has_permission(self.doctorRequest, view))
        self.assertTrue(
            permission.has_permission(self.coordinatorRequest, view))

    def test_is_doctor_of_patient(self):
        patient_view = FakeView({'patient_pk': -1})

        patient = PatientFactory.create(doctor=self.doctor)

        permission = IsDoctorOfPatient()
        self.assertFalse(
            permission.has_permission(self.userRequest, patient_view))
        self.assertFalse(
            permission.has_permission(self.doctorRequest, patient_view))

        self.assertTrue(
            permission.has_permission(self.doctorRequest,
                                      FakeView({
                                          'patient_pk': patient.pk
                                      })))

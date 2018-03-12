from apps.main.tests import APITestCase
from apps.accounts.factories import CoordinatorFactory, DoctorFactory


class ConsentDocViewSetTest(APITestCase):
    def setUp(self):
        super(ConsentDocViewSetTest, self).setUp()

        CoordinatorFactory.create(
            doctor_ptr=self.doctor
        )
        self.other_doctor = DoctorFactory(password='password')

    def post_doc(self):
        return self.client.post('/api/v1/study/consent_doc/', {
            'file': self.get_sample_file('pdf_doc.pdf')
        })

    def test_forbidden_unauthorized(self):
        response = self.post_doc()
        self.assertForbidden(response)

    def test_forbidden_other_doctor(self):
        self.authenticate_as_doctor(self.other_doctor)
        response = self.post_doc()
        self.assertForbidden(response)

    def test_success_doctor(self):
        self.authenticate_as_doctor()
        response = self.post_doc()
        self.assertSuccessResponse(response)

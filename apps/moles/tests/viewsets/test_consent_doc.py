from apps.main.models import FlatBlock
from apps.main.tests import APITestCase
from apps.accounts.factories import CoordinatorFactory, DoctorFactory
from apps.moles.factories.study import ConsentDocFactory


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

    def post_image_doc(self):
        return self.client.post('/api/v1/study/consent_doc/', {
            'file': self.get_sample_image_file('image_doc.png')
        })

    def test_forbidden_unauthorized(self):
        response = self.post_doc()
        self.assertUnauthorized(response)

    def test_forbidden_other_doctor(self):
        self.authenticate_as_doctor(self.other_doctor)
        response = self.post_doc()
        self.assertForbidden(response)

    def test_success_doctor(self):
        self.authenticate_as_doctor()
        response = self.post_doc()
        self.assertSuccessResponse(response)
        self.assertTrue(response.data['pk'] > 0)
        self.assertTrue(len(response.data['file']) > 0)

    def test_thumbnail_success(self):
        self.authenticate_as_doctor()
        response = self.post_image_doc()
        self.assertIsNotNone(response.data['thumbnail'])
        self.assertEqual(response.data['original_filename'], 'image_doc.png')

    def test_default_consent_docs(self):
        with self.fake_media():
            doc1 = ConsentDocFactory.create(
                is_default_consent=True,
                file=self.get_sample_image_file())
            doc2 = ConsentDocFactory.create(
                is_default_consent=True,
                file=self.get_sample_image_file())

        self.authenticate_as_doctor()
        resp = self.client.get('/api/v1/study/consent_doc/default/')
        self.assertTrue(len(resp.data['page']) > 0)
        self.assertSetEqual(
            {doc1.pk, doc2.pk},
            set([item['pk'] for item in resp.data['docs']]))

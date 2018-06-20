from datetime import timedelta

from django.test import TestCase, TransactionTestCase, mock
from django.utils import timezone

from apps.accounts.factories import DoctorFactory, PatientFactory, \
    PatientConsentFactory, CoordinatorFactory, ParticipantFactory
from apps.accounts.models import DoctorToPatient
from apps.main.tests import patch
from apps.main.tests.mixins import FileTestMixin
from apps.moles.factories.study import StudyFactory, ConsentDocFactory
from apps.moles.models import StudyToPatient
from ..factories import MoleImageFactory


class MoleImageTest(FileTestMixin, TransactionTestCase):
    @patch('apps.moles.tasks.requests', new_callable=mock.MagicMock)
    def test_set_up(self, mock_requests):
        post_mock = mock.MagicMock()
        post_mock.json.return_value = {
            'status': 'success',
            'probability': 0.567,
            'prediction': 'Seems benign',
        }
        mock_requests.post.return_value = post_mock
        with self.fake_media():
            MoleImageFactory.create(photo=self.get_sample_image_file())

        self.assertTrue(mock_requests.post.called)


class StudyTest(FileTestMixin, TestCase):
    def setUp(self):
        self.doctor = DoctorFactory.create()
        self.patient = PatientFactory.create()
        self.study = StudyFactory.create(
            author=CoordinatorFactory.create()
        )
        self.study.doctors.add(self.doctor)
        self.study.save()

        DoctorToPatient.objects.create(
            doctor=self.doctor,
            patient=self.patient)
        consent = PatientConsentFactory.create(
            patient=self.patient)
        self.study_to_patient = StudyToPatient.objects.create(
            study=self.study,
            patient=self.patient,
            patient_consent=consent)

    @patch('apps.moles.models.study.Study.invalidate_consents')
    def test_update_consent_without_changing_docs(
            self, mock_invalidate_consents):
        self.study.title = 'Changed name'
        self.study.save()
        self.study.refresh_from_db()
        self.assertEqual(self.study.title, 'Changed name')
        self.assertFalse(mock_invalidate_consents.called)

    @patch('apps.moles.models.study.DoctorNotificationDocConsentUpdate.send')
    @patch('apps.moles.models.study.ParticipantNotificationDocConsentUpdate.send')
    def test_update_consent_docs(self,
                                 mock_participant_notification,
                                 mock_doc_notification):
        self.assertTrue(self.study_to_patient.patient_consent.is_valid())

        # Make out doctor participant (self.doctor in doctors and in patients)
        ParticipantFactory.create(doctor_ptr=self.doctor)

        yesterday_date = timezone.now() - timedelta(days=1)
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = yesterday_date

            with self.fake_media():
                new_doc = ConsentDocFactory.create(
                    file=self.get_sample_image_file())

            self.study.consent_docs.add(new_doc)
            self.study.save()
            self.study_to_patient.patient_consent.refresh_from_db()
            self.assertFalse(self.study_to_patient.patient_consent.is_valid())

        self.assertTrue(mock_doc_notification.called)
        self.assertTrue(mock_participant_notification.called)

    @patch('apps.moles.models.study.DoctorNotificationDocConsentUpdate.send')
    @patch('apps.moles.models.study.ParticipantNotificationDocConsentUpdate.send')
    def test_update_consent_docs_without_consent(self,
                                                 mock_participant_notification,
                                                 mock_doc_notification):
        self.assertTrue(self.study_to_patient.patient_consent.is_valid())

        self.study_to_patient.patient_consent = None
        self.study_to_patient.save()

        with self.fake_media():
            new_doc = ConsentDocFactory.create(
                file=self.get_sample_image_file())

        self.study.consent_docs.add(new_doc)
        self.study.save()

        self.assertTrue(mock_doc_notification.called)
        self.assertFalse(mock_participant_notification.called)

    @patch('apps.moles.models.study.DoctorNotificationDocConsentUpdate.send')
    @patch('apps.moles.models.study.ParticipantNotificationDocConsentUpdate.send')
    def test_update_consent_docs_without_participant_doctor(
            self,
            mock_participant_notification,
            mock_doc_notification):
        self.assertTrue(self.study_to_patient.patient_consent.is_valid())

        new_doc = ConsentDocFactory.create()
        self.study.consent_docs.add(new_doc)
        self.study.save()

        self.assertTrue(mock_doc_notification.called)
        self.assertFalse(mock_participant_notification.called)

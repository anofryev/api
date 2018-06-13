from django.test import TransactionTestCase, mock
from apps.main.tests import patch
from apps.main.tests.mixins import FileTestMixin
from ..factories import MoleImageFactory
from ..tasks import GetPredictionError


class TasksTest(FileTestMixin, TransactionTestCase):
    @patch('apps.moles.tasks.requests', new_callable=mock.MagicMock)
    def test_get_mole_image_prediction_success(self, mock_requests):
        post_mock = mock.MagicMock()
        post_mock.json.return_value = {
            'status': 'success',
            'probability': 0.567,
            'prediction': 'Seems benign',
        }
        mock_requests.post.return_value = post_mock

        # Task `get_mole_image_prediction` runs automatically on post save
        # signal
        with self.fake_media():
            mole_image = MoleImageFactory.create(
                photo=self.get_sample_image_file())

        mole_image.refresh_from_db()
        self.assertEqual(mole_image.prediction, 'Seems benign')
        self.assertAlmostEqual(float(mole_image.prediction_accuracy), 0.567)

    @patch('apps.moles.tasks.requests', new_callable=mock.MagicMock)
    def test_get_mole_image_prediction_failed(self, mock_requests):
        post_mock = mock.MagicMock()
        post_mock.json.return_value = {
            'status': 'error',
        }
        mock_requests.post.return_value = post_mock

        # Task `get_mole_image_prediction` runs automatically on post save
        # signal
        with self.fake_media(), self.assertRaises(GetPredictionError):
            MoleImageFactory.create(
                photo=self.get_sample_image_file())

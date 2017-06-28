from django.test import TransactionTestCase, mock

from apps.main.tests import patch
from apps.main.tests.mixins import FileTestMixin
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

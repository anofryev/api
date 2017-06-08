from django.test import TestCase, mock

from apps.main.tests import patch
from apps.main.tests.mixins import FileTestMixin
from ..factories import MoleImageFactory


class MoleImageTest(FileTestMixin, TestCase):
    @patch('apps.moles.tasks.requests')
    def test_set_up(self, mock_requests):
        with self.fake_media():
            MoleImageFactory.create(photo=self.get_sample_image_file())

        self.assertTrue(mock_requests.post.called)

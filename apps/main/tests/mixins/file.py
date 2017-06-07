import shutil
import tempfile
import errno

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings


class FileTestMixin(object):
    def fake_media(self):
        tmp_dir = tempfile.mkdtemp()

        try:
            return override_settings(MEDIA_ROOT=tmp_dir)
        finally:
            try:
                shutil.rmtree(tmp_dir)
            except OSError as e:
                # Reraise unless ENOENT: No such file or directory
                # (ok if directory has already been deleted)
                if e.errno != errno.ENOENT:
                    raise

    def get_sample_file(self, name, content=b'*'):
        with tempfile.NamedTemporaryFile() as tf:
            tf.file.write(content)
            tf.file.seek(0)
            return SimpleUploadedFile(name, tf.file.read())

    def get_sample_image_file(self, name='photo.png'):
        return self.get_sample_file(
            name,
            content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00'
                    b'\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00'
                    b'\x0fIDAT\x08\x1d\x01\x04\x00\xfb\xff\x00\xff\xff\xff\x05'
                    b'\xfe\x02\xfe\x03}\x19\xc6\x00\x00\x00\x00IEND\xaeB`\x82')

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from s3file.middleware import S3FileMiddleware
from s3file.storages import storage


class TestS3FileMiddleware:

    def test_get_files_from_storage(self):
        content = b'test_get_files_from_storage'
        name = storage.save('test_get_files_from_storage', ContentFile(content))
        files = S3FileMiddleware.get_files_from_storage([name])
        file = next(files)
        assert file.read() == content

    def test_process_request(self, rf):
        uploaded_file = SimpleUploadedFile('uploaded_file.txt', b'uploaded')
        request = rf.post('/', data={'file': uploaded_file})
        S3FileMiddleware(lambda x: None)(request)
        assert request.FILES.getlist('file')
        assert request.FILES.get('file').read() == b'uploaded'

        storage.save('s3_file.txt', ContentFile(b's3file'))
        request = rf.post('/', data={
            'file': '["custom/location/s3_file.txt"]', 's3file': '["file"]'
        })
        S3FileMiddleware(lambda x: None)(request)
        assert request.FILES.getlist('file')
        assert request.FILES.get('file').read() == b's3file'

    def test_process_request__no_file(self, rf, caplog):
        request = rf.post(
            '/',
            data={'file': '["does_not_exist.txt"]', 's3file': '["file"]'}
        )
        S3FileMiddleware(lambda x: None)(request)
        assert not request.FILES.getlist('file')
        assert 'File not found: does_not_exist.txt' in caplog.text

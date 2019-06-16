from django.core.checks import Error
from django.core.files.storage import default_storage

from . import storages


def storage_check(app_configs, **kwargs):
    errors = []
    if isinstance(default_storage, storages.DummyS3Boto3Storage):
        errors.append(
            Error(
                'DummyS3Boto3Storage should not be used in a production setup.',
                hint='Please use S3Boto3Storage in your production environment',
                obj=storages.DummyS3Boto3Storage,
                id='s3file.W001',
            )
        )
    return errors

import pytest
from django.core.management import call_command
from django.core.management.base import SystemCheckError


def test_storage_check():
    call_command('check')

    with pytest.raises(SystemCheckError) as e:
        call_command('check', '--deploy')

    assert 'DummyS3Boto3Storage should not be used' in str(e.value)

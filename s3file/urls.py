from django.urls import path

from . import views

app_name = 's3file'

urlpatterns = [
    path(r'_s3_dummy_endpoint/', views.S3MockView.as_view(), name='s3mock'),
]

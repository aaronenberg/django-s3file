from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.ExampleFormView.as_view(), name='upload'),
    path('_s3_dummy/', include('s3file.urls'))
]

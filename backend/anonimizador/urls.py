from django.urls import path
from .views import AnonymizePreview, AnonymizeRun

urlpatterns = [
    path('preview/', AnonymizePreview.as_view(), name='anonymize-preview'),
    path('', AnonymizeRun.as_view(), name='anonymize-run'),
]
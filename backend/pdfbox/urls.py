
from django.urls import path
from .views import CompressPDFView, SplitPDFView

urlpatterns = [
    path('compress/', CompressPDFView.as_view(), name='compress_pdf'),
    path('split/', SplitPDFView.as_view(), name='split_pdf'),
]

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views.pdf_views import PDFViewSet
from .views.excel_views import AnonymizeNameView
from .views.anonimization_views import AnonymizePreview, AnonymizeRun

app_name = "pdfbox"

router = SimpleRouter()
router.register(r"pdf", PDFViewSet, basename="pdf")

urlpatterns = [
    path("", include(router.urls)),
    path("excel/anonymize/name/", AnonymizeNameView.as_view(), name="excel-anonymize-name"),
    path('anonymize/preview/', AnonymizePreview.as_view(), name='anonymize-preview'),
    path('anonymize/', AnonymizeRun.as_view(), name='anonymize-run'),
]

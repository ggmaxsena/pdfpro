# pdf_tools/urls.py
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views.pdf_views import PDFViewSet

router = SimpleRouter()
router.register(r"pdf", PDFViewSet, basename="pdf")

urlpatterns = [
    path("", include(router.urls)),
]

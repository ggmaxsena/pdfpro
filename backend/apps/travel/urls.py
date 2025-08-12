from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .interfaces.views import CalculateDiariasView, TravelRequestViewSet, TravelerViewSet #, GeneratePdfView

router = DefaultRouter()
router.register(r'travel-requests', TravelRequestViewSet)
router.register(r'travelers', TravelerViewSet)

urlpatterns = [
    path('diarias/calculate', CalculateDiariasView.as_view(), name='calculate_diarias'),
    # path('generate-pdf/', GeneratePdfView.as_view(), name='generate_pdf'),
    path('', include(router.urls)),
]
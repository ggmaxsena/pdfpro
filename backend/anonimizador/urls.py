
from django.urls import path
from .views import AnonymizeView

urlpatterns = [
    path('', AnonymizeView.as_view(), name='anonimize'),
]

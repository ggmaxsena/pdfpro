from django.urls import path
from .views.excel_views import AnonymizeNameView

app_name = "excel_tools"

urlpatterns = [
    path(
        "anonymize/name/",
        AnonymizeNameView.as_view(),
        name="excel-anonymize-name",
    ),
]

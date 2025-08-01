
from typing import List, Union
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver
from django.conf import settings
from django.conf.urls.static import static

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth.urls')),
    path('api/anonimize/', include('apps.anonimizador.urls')),
    path('api/pdf/', include('apps.pdf_tools.urls')),
    path('api/excel/', include('apps.excel_tools.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

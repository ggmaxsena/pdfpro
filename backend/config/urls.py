
from typing import List, Union
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth.urls')),
    path('api/anonimize/', include('apps.anonimizador.urls')),
    path('api/pdf/', include('apps.pdf_tools.urls')),
    path('api/excel/', include('apps.excel_tools.urls')),
    path('api/travel/', include('apps.travel.urls')),
    path('api/travel/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/travel/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

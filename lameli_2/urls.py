from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from lameli_2 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('apps.product.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
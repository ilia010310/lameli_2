from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.product.sitemaps import ProductSitemap
from lameli_2 import settings

sitemaps = {
    'posts': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about_us/', TemplateView.as_view(template_name='products/about_us.html'),
            name='about_us'),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('apps.product.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

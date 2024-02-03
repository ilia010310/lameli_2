from django.urls import path
from .views import ProductListView, ProductDetailView, ProductFromCategory

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', ProductFromCategory.as_view(), name="product_by_category"),
]
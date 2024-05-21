import logging

from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from ..cart.cart import Cart
from ..cart.forms import CartAddProductForm

logger = logging.getLogger(__name__)


class ProductListView(ListView):
    model = Product
    cart_item_form = CartAddProductForm()
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mr Vidergold'
        context['cart_item_form'] = self.cart_item_form
        cart = Cart(self.request)
        context['cart_count'] = len(cart)

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    cart_item_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['cart_item_form'] = self.cart_item_form
        context['images'] = self.object.images.all()
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context


class ProductFromCategory(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    cart_item_form = CartAddProductForm()
    category = None
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        cache_key = f'product_list_{self.category.slug}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Product.objects.filter(category__slug=self.category.slug)
            if not queryset:
                sub_cat = Category.objects.filter(parent=self.category)
                queryset = Product.objects.filter(category__in=sub_cat)
            queryset = queryset.select_related('category')
            cache.set(cache_key, queryset, timeout=60)  # Кэшировать на 60 секунд
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Категория: {self.category.title}'
        context['cart_item_form'] = self.cart_item_form
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    logger.warning('Кто то переходит на несуществующую страницу')
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    logger.error('Ошибка на сервере')
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message':
            'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    logger.error('Ошибка доступа: 403')
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })

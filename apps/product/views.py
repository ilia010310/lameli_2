from django.views.generic import ListView, DetailView
from .models import Product, Category
from ..cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    cart_item_form = CartAddProductForm()
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 16
    queryset = Product.custom.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cart_item_form'] = self.cart_item_form
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

class ProductFromCategory(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    category = None
    paginate_by = 1
    queryset = Product.custom.all()

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Product.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Product.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Товары категории: {self.category.title}'
        return context

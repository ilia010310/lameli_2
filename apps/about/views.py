from django.views.generic import TemplateView

from apps.cart.cart import Cart


class AboutUsView(TemplateView):
    template_name = 'products/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context

class ContactsView(TemplateView):
    template_name = 'products/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        return context

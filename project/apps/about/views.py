from django.shortcuts import render
from django.views.generic import TemplateView
from apps.about.forms import CallBackForm
from apps.about.models import CallBack
from apps.cart.cart import Cart
from django.core.cache import cache
from apps.order.tasks import send_salesman_email


class AboutUsView(TemplateView):
    template_name = 'products/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart_count'] = len(cart)
        context['title'] = 'О компании'
        return context


class ContactsView(TemplateView):
    template_name = 'products/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['title'] = 'Контакты'
        context['cart_count'] = len(cart)
        return context


def call_back(request):
    cart = len(cache.get_or_set('cached_cart', Cart(request)))

    if request.method == 'POST':
        form = CallBackForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            del form_data['recaptcha']

            final_call = CallBack(**form_data)
            final_call.save()

            name = form_data['name']
            phone = form_data['number']

            message = f"Имя покупателя: {name}.\n\n" \
                      f'Телефон: {phone}\n\n' \
                      f'Запросил обратный звонок'

            send_salesman_email.delay(message)
            return render(request, 'products/success.html', {'name': name,
                                                             'cart_count': cart,
                                                             'title': 'Успешно'})
        else:
            form_errors = form.errors.as_text()
            return render(request, 'products/call_back.html', {'form': form,
                                                               'cart_count': cart,
                                                               'title': 'Обраная связь', 'form_errors': form_errors})
    form = CallBackForm()
    return render(request, 'products/call_back.html', {'form': form,
                                                       'cart_count': cart,
                                                       'title': 'Обратный звонок'})

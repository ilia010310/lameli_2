from django.core.cache import cache
from django.shortcuts import render
from apps.cart.cart import Cart
from apps.order.forms import OrderForm
from apps.order.models import Order, ProductsInOrder
from apps.product.models import Product
from .tasks import send_customer_email, send_salesman_email


def order(request):
    cart = len(cache.get_or_set('cached_cart', Cart(request)))
    if not Cart(request):
        return render(request, 'cart/empty_cart.html', {'cart_count': cart,
                                                        'title': 'Упс...'})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['total_price'] = Cart(request).get_total_price()
            del form_data['recaptcha']

            final_order = Order(**form_data)

            final_order.save()
            products_in_answer = 'Товары: \n\n'
            for item in Cart(request):
                product = Product.objects.get(name=item['product'])
                quantity = item['quantity']
                price = item['price']
                total_price = quantity * price
                products_in_answer += (f'{product.name}\nКоличество: {quantity} шт.\n'
                                       f'Цена за штуку: {price} руб. \n\n ')
                final_product_in_order = {'quantity': quantity,
                                          'price_per_product': price,
                                          'order': final_order,
                                          'product': product,
                                          'total_price': total_price,
                                          }
                one_product_in_total_order = ProductsInOrder(**final_product_in_order)
                one_product_in_total_order.save()

            name = form_data['customer_name']
            recipient = form_data['customer_email']
            send_customer_email.delay(name, recipient)

            message = f"Имя покупателя: {name}.\n\n" \
                      f"Email: {form_data['customer_email']}\n\n" \
                      f'Телефон: {form_data["customer_phone"]}\n\n' \
                      f'ИНН: {form_data["customer_inn"]}\n\n' \
                      f'Комментарий: {form_data["comments"]}\n\n' \
                      f'{products_in_answer}\n\n' \
                      f'Итого: {form_data["total_price"]} руб.'
            send_salesman_email.delay(message)
            Cart(request).clear()
            cache.delete('cached_cart')
            return render(request, 'cart/solution.html', {'name': name,
                                                          'cart_count': cart,
                                                          'title': 'Заказ'})
        else:
            form_errors = form.errors.as_text()
            return render(request, 'cart/order.html', {'form': form,
                                                       'cart_count': cart,
                                                       'title': 'Заказ', 'form_errors': form_errors})
    form = OrderForm()
    return render(request, 'cart/order.html', {'form': form,
                                               'cart_count': cart,
                                               'title': 'Заказ'})

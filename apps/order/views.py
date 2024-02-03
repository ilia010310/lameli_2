from django.shortcuts import render
from apps.cart.cart import Cart
from django.http import HttpResponse
from lameli_2 import settings
from apps.order.forms import OrderForm
from apps.order.models import Order, ProductsInOrder
from apps.product.models import Product
from django.core.mail import send_mail


def order(request):
    if not Cart(request):
        return render(request, 'empty_cart.html')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['total_price'] = Cart(request).get_total_price()

            final_order = Order(**form_data)

            final_order.save()
            products_in_answer = 'Товары: \n\n'
            for product in Cart(request):

                product = Product.objects.get(name=product['product'])
                quantity = Product['quantity']
                price = product['price']
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

            subject = f"{name}, спасибо за заказ!"
            message = f"Ваш заказ уже принят в обработку.\n\n" \
                      f"Скоро с Вами свяжется наш менеджер."
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [form_data['customer_email']])

            subject = f"Новый заказ!"

            message = f"Имя покупателя: {name}.\n\n" \
                      f"Email: {form_data['customer_email']}\n\n" \
                      f'Телефон: {form_data["customer_phone"]}\n\n' \
                      f'ИНН: {form_data["customer_inn"]}\n\n' \
                      f'Комментарий: {form_data["comments"]}\n\n' \
                      f'{products_in_answer}\n\n' \
                      f'Итого: {form_data["total_price"]} руб.'
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      ['theilyaboyarintsev@gmail.com'])
            print(form_data)
            print(Cart(request))
            return render(request, 'solution.html', {'name': name})

    else:
        form = OrderForm()
        return render(request, 'order.html', {'form': form})

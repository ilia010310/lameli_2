from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
import re

from apps.order.models import Order
from lameli_2 import settings


class DebugReCaptchaField(ReCaptchaField):
    """
    Дочерняя Капча для работы в DEBUG режиме,
    так как для ReCaptchaField нужен SSL сертификат.
    """
    def clean(self, values):
        if settings.DEBUG:
            if len(values) > 0:
                return values[0]
        return super().clean(values)
def validate_phone_number(value):
    if not re.match(r'^(\+7|8)\d{10}$', value):
        raise ValidationError(
            'Неправильный формат номера телефона. Используйте формат +7XXXXXXXXXX или 8XXXXXXXXXX.'
        )





class OrderForm(forms.ModelForm):
    recaptcha = DebugReCaptchaField()
    customer_name = forms.CharField(required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control",
                                                                  'placeholder': 'Контактное лицо',
                                                                  'style': 'width: 300px;'}))
    customer_email = forms.EmailField(required=True,
                                      widget=forms.EmailInput(attrs={"class": "form-control",
                                                                     'placeholder': 'Email', 'style': 'width: 300px;'}))
    customer_phone = forms.CharField(required=True,
                                        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Телефон',
                                                                      'style': 'width: 300px;'}))
    customer_inn = forms.CharField(required=False,
                                   widget=forms.TextInput(
                                       attrs={"class": "form-control", 'placeholder': 'ИНН (для юр. лиц)',
                                              'style': 'width: 300px;'}))
    comments = forms.CharField(required=False,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", 'placeholder': 'Комментарий к заказу',
                                          'style': 'width: 300px; height: 100px;'}))

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone',
                  'customer_inn', 'comments', 'recaptcha']


import logging

from django.core.mail import send_mail
from apps.product.celery import app
from lameli_2 import settings

logger = logging.getLogger(__name__)


@app.task
def send_customer_email(name, recipient):
    try:
        subject = f"{name}, спасибо за заказ!"
        message = f"Ваш заказ уже принят в обработку.\n\n" \
                  f"Скоро с Вами свяжется наш менеджер."
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [recipient])
    except Exception as e:
        logger.warning('Отправка сообщения покупателю не удалась')


@app.task
def send_salesman_email(message):
    try:
        subject = f"Новый заказ!"

        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  ['v9127165074@gmail.com'])
    except Exception as e:
        logger.warning('Отправка сообщения продавцу не удалась')

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lameli_2.settings')
app = Celery('apps.product', broker_connection_retry=False,
             broker_connection_retry_on_startup=True, )
app.config_from_object('django.conf:settings')
broker_connection_retry = False

app.autodiscover_tasks()
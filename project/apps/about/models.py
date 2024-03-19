from django.db import models


class CallBack(models.Model):
    number = models.BigIntegerField(verbose_name='Телефон')
    name = models.CharField(max_length=40, verbose_name='Имя')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Звонок'
        verbose_name_plural = 'Звонки'

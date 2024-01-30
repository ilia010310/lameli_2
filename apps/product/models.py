from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Product(models.Model):
    STATUS_OPTIONS = (
        ('YES', 'В наличии'),
        ('NO', 'Скоро на складе')
    )

    name = models.CharField(max_length=55, verbose_name='Название')
    slug = models.SlugField(max_length=55, verbose_name='Артикул', unique=True)
    avatar = models.ImageField(default='default.png',
                                  verbose_name='Главная фотография',
                                  blank=True,
                                  upload_to='images/avatars/',
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
                                  )
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(choices=STATUS_OPTIONS, default='YES', verbose_name='Статус товара', max_length=10)
    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Колличество')
    price = models.DecimalField(default=1990, verbose_name='Цена', decimal_places=0, max_digits=8)
    publish = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        ordering = ['id']
        indexes = [models.Index(fields=['name', '-publish', 'status'])] #индексация для ускорения БД
        db_table = 'product'  #название в БД

    def __str__(self):
        return self.name


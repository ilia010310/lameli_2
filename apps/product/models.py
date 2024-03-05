import os

from PIL import Image
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from apps.service.utils import unique_slugify
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from lameli_2 import settings


class ProductManager(models.Manager):
    """
    Кастомный менеджер для модели товаров
    """

    def all(self):
        return self.get_queryset().select_related('category').filter(status='YES')


class Product(models.Model):
    STATUS_OPTIONS = (
        ('YES', 'В наличии'),
        ('NO', 'Не в наличии')
    )

    name = models.CharField(max_length=46, verbose_name='Название')
    slug = models.SlugField(verbose_name='Артикул', max_length=255, blank=True)
    avatar = models.ImageField(default='default.png',
                               verbose_name='Главная фотография',
                               upload_to='images/avatars/',
                               validators=[
                                   FileExtensionValidator(
                                       allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif', 'webp'))]
                               )
    description = models.TextField(verbose_name='Описание')
    category = TreeForeignKey('Category', on_delete=models.PROTECT,
                              related_name='products', verbose_name='Категория', default=1)
    status = models.CharField(choices=STATUS_OPTIONS, default='YES', verbose_name='Статус товара', max_length=10)
    price = models.DecimalField(default=1990, verbose_name='Цена', decimal_places=0, max_digits=8)
    publish = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    objects = models.Manager()
    custom = ProductManager()

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        ordering = ['id']
        indexes = [models.Index(fields=['name', '-publish', 'status'])]  # индексация для ускорения БД
        db_table = 'product'  # название в БД

    def __str__(self):
        return self.name


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('product_by_category', kwargs={'slug': self.slug})


class ProductImages(models.Model):
    product = models.ForeignKey(Product,
                                blank=True,
                                null=True, default=None,
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='item_images/',
                              verbose_name='Картинка')


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, signal, *args, **kwargs):
    abs_image_path = os.path.join(settings.BASE_DIR, instance.avatar.url[1:])
    try:
        with Image.open(abs_image_path) as img:
            new_img = img.crop((0, 0, img.width, img.width))
            new_img.save(abs_image_path)
    except Exception as e:
        print(f"An error occurred: {e}")


@receiver(post_save, sender=ProductImages)
def product_post_save_images(sender, instance, signal, *args, **kwargs):
    abs_image_path = os.path.join(settings.BASE_DIR, instance.image.url[1:])
    try:
        with Image.open(abs_image_path) as img:
            new_img = img.crop((0, 0, img.width, img.width))
            new_img.save(abs_image_path)
    except Exception as e:
        print(f"An error occurred: {e}")

# @receiver(pre_delete, sender=Product)
# def pre_delete_cart_item(sender, instance, **kwargs):
